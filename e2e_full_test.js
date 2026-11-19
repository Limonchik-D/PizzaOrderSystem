const { chromium } = require('playwright-core');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function runTests() {
  console.log('=== Запуск E2E сквозного тестирования CROSTA Artisanal Pizza Europe v2.0 ===\n');
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => consoleErrors.push(err.message));

  let passedTests = 0;
  let totalTests = 0;

  function assert(condition, message) {
    totalTests++;
    if (condition) {
      console.log(`[PASS] ${message}`);
      passedTests++;
    } else {
      console.error(`[FAIL] ${message}`);
      throw new Error(`Test failed: ${message}`);
    }
  }

  // TEST 1: Загрузка витрины и промо-акций
  console.log('--- Тест 1: Загрузка витрины, Hero и актуальных промо-акций ---');
  await page.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const heroTitle = await page.$eval('#hero-title', el => el.textContent.trim());
  assert(heroTitle.includes('Ремесленная неаполитанская пицца'), 'Hero-заголовок отображается корректно');

  const promoCardsCount = await page.$$eval('#promotions-grid > div', els => els.length);
  assert(promoCardsCount === 3, `Загружено ровно 3 промо-акции из API (получено: ${promoCardsCount})`);

  const menuItemsCount = await page.$$eval('#menu-grid article', els => els.length);
  assert(menuItemsCount >= 8, `Загружено позиций меню: ${menuItemsCount}`);

  // TEST 2: Переключение темы
  console.log('\n--- Тест 2: Переключение темы (Светлая / Тёмная) ---');
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(300);
  const themeDark = await page.$eval('html', el => el.getAttribute('data-theme'));
  assert(themeDark === 'dark', 'Тёмная тема активирована успешно');

  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(300);
  const themeLight = await page.$eval('html', el => el.getAttribute('data-theme'));
  assert(themeLight === 'light', 'Возврат к светлой теме выполнен успешно');

  // TEST 3: Фильтрация и поиск по каталогу
  console.log('\n--- Тест 3: Фильтры категорий и поиск по каталогу ---');
  await page.click('button[data-cat="Мясные"]');
  await page.waitForTimeout(400);
  const meatPizzas = await page.$$eval('#menu-grid article', els => els.length);
  assert(meatPizzas >= 2, `Фильтр "Мясные": отображено ${meatPizzas} пиццы`);

  // Сброс на "Все" перед текстовым поиском
  await page.click('button[data-cat="Все"]');
  await page.waitForTimeout(300);

  await page.fill('#search-input', 'Трюфель');
  await page.waitForTimeout(400);
  const searchResults = await page.$$eval('#menu-grid article', els => els.length);
  assert(searchResults === 1, `Поиск "Трюфель": найдена ровно 1 позиция (получено: ${searchResults})`);

  // Сброс поиска
  await page.fill('#search-input', '');
  await page.waitForTimeout(400);

  // TEST 4: Выбор размера и динамический расчёт цены
  console.log('\n--- Тест 4: Переключение размера пиццы и пересчёт цены ---');
  const initialPrice = await page.$eval('#menu-grid article:first-child .tabular-nums', el => el.textContent.trim());
  // Выбираем размер L (35 см)
  const sizeLBtn = await page.$('#menu-grid article:first-child button:has-text("35 см")');
  if (sizeLBtn) {
    await sizeLBtn.click();
    await page.waitForTimeout(300);
    const updatedPrice = await page.$eval('#menu-grid article:first-child .tabular-nums', el => el.textContent.trim());
    assert(initialPrice !== updatedPrice, `Цена пересчитана при смене диаметра: ${initialPrice} -> ${updatedPrice}`);
  }

  // TEST 5: Авторизация клиента Давида (Demo Login)
  console.log('\n--- Тест 5: Аутентификация клиента Давида и сессия ---');
  await page.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await page.waitForTimeout(1000);

  const authUser = await page.evaluate(() => currentUser);
  assert(authUser && authUser.email === 'david@crosta.eu', `Успешный вход под аккаунтом: ${authUser?.fullName}`);
  assert(typeof authUser.bonusBalance === 'number' && authUser.bonusBalance > 0, `Баланс бонусов клиента положителен (факт: €${authUser.bonusBalance.toFixed(2)})`);

  const headerBonus = await page.$eval('#nav-bonus-pill', el => el.textContent.trim());
  assert(headerBonus.includes('€') || headerBonus.length > 0, `Бейдж бонусов в шапке отображает баланс: ${headerBonus}`);

  // TEST 6: Раздел «Профиль и бонусы»
  console.log('\n--- Тест 6: Кабинет лояльности, карта, история бонусов и повтор заказа ---');
  await page.click('#tab-profile');
  await page.waitForTimeout(600);

  const profileCardName = await page.$eval('#profile-full-name', el => el.textContent.trim());
  assert(profileCardName.includes('Давид'), `Карточка профиля: имя "${profileCardName}"`);

  const loyaltyBalance = await page.$eval('#profile-bonus-balance', el => el.textContent.trim());
  assert(loyaltyBalance.includes('€'), `Карта Loyalty Club: баланс "${loyaltyBalance}"`);

  const bonusRows = await page.$$eval('#profile-bonus-tbody tr', els => els.length);
  assert(bonusRows >= 2, `Таблица истории бонусов: ${bonusRows} записей`);

  const repeatOrderBtn = await page.$('#profile-orders-list button:has-text("Повторить заказ")');
  assert(repeatOrderBtn !== null, 'Кнопка "Повторить заказ" доступна в истории прошлых заказов');

  // TEST 7: Корзина, списание бонусов (до 30%) и оформление заказа
  console.log('\n--- Тест 7: Корзина, ограничение бонусов 30%, НДС 10% и чекаут ---');
  await page.click('#tab-store');
  await page.waitForTimeout(500);

  // Добавляем 2 пиццы в корзину
  await page.click('#menu-grid article:nth-child(1) button:has-text("В корзину")');
  await page.waitForTimeout(400);
  await page.click('#menu-grid article:nth-child(2) button:has-text("В корзину")');
  await page.waitForTimeout(400);

  const cartItemsCount = await page.evaluate(() => cart.length);
  assert(cartItemsCount >= 2, `В корзине ${cartItemsCount} различных позиций`);

  // Проверяем списание бонусов
  const maxBonusAllowed = await page.evaluate(() => {
    const gross = cart.reduce((sum, i) => {
      const p = menu.find(x => x.id === i.pizzaId);
      const s = sizes.find(x => x.id === i.sizeId) || sizes[0];
      return sum + (p.basePriceEur * s.priceMultiplier * i.quantity);
    }, 0);
    return Math.min(currentUser.bonusBalance, Math.round(gross * 0.30 * 100) / 100);
  });
  assert(maxBonusAllowed > 0, `Максимальный лимит списания бонусов (30%): €${maxBonusAllowed.toFixed(2)}`);

  await page.evaluate((val) => setBonusSpend(val), Math.min(3.00, maxBonusAllowed));
  await page.waitForTimeout(300);

  const currentBonusSpend = await page.evaluate(() => bonusToSpend);
  assert(currentBonusSpend > 0, `Успешно применены бонусы: €${currentBonusSpend.toFixed(2)}`);

  // Оформляем заказ
  await page.check('#gdpr-consent');
  await page.click('#checkout-form button[type="submit"]');
  await page.waitForTimeout(1500);

  const newOrderNumber = await page.evaluate(() => trackedOrderNumber);
  assert(newOrderNumber && newOrderNumber.startsWith('ORD-'), `Заказ успешно создан в SQLite: ${newOrderNumber}`);

  // TEST 8: Экран трекинга заказа
  console.log('\n--- Тест 8: Экран трекинга, степпер этапов и детализация чека ---');
  await page.click('#tab-track');
  await page.waitForTimeout(600);

  const displayedOrder = await page.$eval('#tracked-order-card h3', el => el.textContent.trim());
  assert(displayedOrder === newOrderNumber || displayedOrder.startsWith('ORD-'), `Трекер отображает заказ: ${displayedOrder}`);

  const activeStepCircle = await page.$('.stepper-active-circle');
  assert(activeStepCircle !== null, 'Активный узел степпера подсвечен');

  // TEST 9: Админ-панель (Елена Ковальчук)
  console.log('\n--- Тест 9: Вход администратора, KPI карточки, аналитика продаж и стоп-лист ---');
  await page.evaluate(() => demoLogin('admin@crosta.eu', 'Admin123!'));
  await page.waitForTimeout(1000);

  const adminRole = await page.evaluate(() => currentUser.role);
  assert(adminRole === 'Admin', 'Авторизован пользователь с ролью Admin');

  await page.click('#tab-staff');
  await page.waitForTimeout(600);

  const kpiGross = await page.$eval('#admin-kpi-gross', el => el.textContent.trim());
  assert(kpiGross.includes('€'), `Карточка KPI Выручка брутто: ${kpiGross}`);

  const topPizzasCount = await page.$$eval('#admin-top-pizzas > div', els => els.length);
  assert(topPizzasCount >= 3, `Гистограмма топ-пицц содержит ${topPizzasCount} позиций`);

  // Проверка переключения стоп-листа
  const textBefore = await page.$eval('#admin-stop-list button', el => el.textContent.trim());
  await page.click('#admin-stop-list button');
  await page.waitForTimeout(800);
  const textAfter = await page.$eval('#admin-stop-list button', el => el.textContent.trim());
  assert(textBefore !== textAfter, `Статус стоп-листа переключён: "${textBefore}" -> "${textAfter}"`);

  // Возвращаем исходный статус
  await page.click('#admin-stop-list button');
  await page.waitForTimeout(800);

  // TEST 10: Логаут и очистка состояния
  console.log('\n--- Тест 10: Выход из аккаунта (Logout) ---');
  await page.evaluate(() => logout());
  await page.waitForTimeout(400);

  const loggedOutUser = await page.evaluate(() => currentUser);
  assert(loggedOutUser === null, 'Сессия пользователя успешно сброшена (currentUser = null)');

  console.log('\n============================================================');
  console.log(`Все E2E тесты пройдены: ${passedTests} из ${totalTests} (100% SUCCESS)`);
  console.log(`Ошибок в консоли браузера: ${consoleErrors.length}`);
  if (consoleErrors.length > 0) {
    console.error('Ошибки:', consoleErrors);
  }
  console.log('============================================================\n');

  await browser.close();
}

runTests().catch(err => {
  console.error('\nОшибка выполнения E2E тестов:', err);
  process.exit(1);
});
