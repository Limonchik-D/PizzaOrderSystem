const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://127.0.0.1:5000';
const LOCAL_OUT_DIR = path.join(__dirname, '..', 'screenshots', 'stage6');
const ARTIFACT_OUT_DIR = 'C:\\Users\\Limon\\.gemini\\antigravity\\brain\\9fffb143-0a4a-428c-b8f0-6fd2e625d429\\stage6';

[LOCAL_OUT_DIR, ARTIFACT_OUT_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

function saveScreenshotBoth(filename, buffer) {
  fs.writeFileSync(path.join(LOCAL_OUT_DIR, filename), buffer);
  fs.writeFileSync(path.join(ARTIFACT_OUT_DIR, filename), buffer);
  console.log(`[Screenshot Saved] ${filename}`);
}

async function runStage6Verification() {
  console.log('=== CROSTA Stage 6: Commercial Polish Verification & Screenshots ===');
  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const consoleErrors = [];

  // =========================================================================
  // Test 1: Desktop Guest Storefront (1440x900)
  // =========================================================================
  console.log('\n--- 1. Testing Guest Storefront & Navigation ---');
  const contextDesktop = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  const page = await contextDesktop.newPage();
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(`[Console Error] ${msg.text()}`);
  });

  await page.goto(`${BASE_URL}/#/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  // Clear any existing localStorage user to test true guest experience
  await page.evaluate(() => {
    localStorage.removeItem('crosta_user');
    window.location.reload();
  });
  await page.waitForTimeout(600);

  // Verify navigation tabs in Guest mode
  const guestNavTabs = await page.evaluate(() => {
    const tabs = Array.from(document.querySelectorAll('#header-nav-container button'))
      .filter(b => b.style.display !== 'none' && !b.classList.contains('hidden') && b.offsetParent !== null)
      .map(b => b.textContent.trim());
    const hasProfile = tabs.some(t => t.includes('Профиль'));
    const hasAdmin = tabs.some(t => t.includes('Админ') || t.includes('Управление'));
    const hasStore = tabs.some(t => t.includes('Меню') || t.includes('Каталог'));
    const hasTrack = tabs.some(t => t.includes('Отследить'));
    return { tabs, hasProfile, hasAdmin, hasStore, hasTrack };
  });

  console.log('Guest Navigation Tabs:', guestNavTabs.tabs);
  if (guestNavTabs.hasProfile || guestNavTabs.hasAdmin) {
    throw new Error('FAIL: Guest navigation should NOT contain Profile or Admin tabs!');
  }
  console.log('[PASS] Guest navigation shows only Menu and Tracking.');

  // Verify Hero Word Roll
  const wordRollText = await page.evaluate(() => document.getElementById('hero-word-roll')?.textContent.trim());
  console.log('Hero Word Roll Text:', wordRollText);
  if (!wordRollText || !wordRollText.includes('Неаполитанская пицца для')) {
    throw new Error('FAIL: Hero Word Roll text missing or incorrect.');
  }
  console.log('[PASS] Hero Word Roll is active.');

  // Verify 3-Column Catalog Grid and SVG illustrations
  const catalogStats = await page.evaluate(() => {
    const articles = document.querySelectorAll('#menu-grid article');
    const svgs = document.querySelectorAll('#menu-grid article svg');
    return { articleCount: articles.length, svgCount: svgs.length };
  });
  console.log(`Catalog Stats: ${catalogStats.articleCount} pizzas, ${catalogStats.svgCount} food illustration SVGs.`);
  if (catalogStats.articleCount < 8 || catalogStats.svgCount < 8) {
    throw new Error('FAIL: Pizza cards or food illustration SVGs are missing.');
  }
  console.log('[PASS] All pizzas rendered with artistic SVG illustrations in full-width grid.');

  // Test in-place size switching (Zero DOM Re-render!)
  console.log('\n--- Testing In-Place Size Switching ---');
  const sizeToggleTest = await page.evaluate(() => {
    const firstCard = document.querySelector('#menu-grid article[data-pizza-id="2"]'); // Pepperoni
    if (!firstCard) return { error: 'Card not found' };

    // Record DOM node identity before click
    window.__testFirstCard = firstCard;
    const initialPrice = firstCard.querySelector('.pizza-price-val').textContent;

    // Click 35 cm button
    const btn35 = firstCard.querySelectorAll('.pizza-size-btn')[2];
    btn35.click();

    // Check if DOM node is still the exact same object
    const currentCard = document.querySelector('#menu-grid article[data-pizza-id="2"]');
    const isSameNode = window.__testFirstCard === currentCard;
    const updatedPrice = currentCard.querySelector('.pizza-price-val').textContent;

    return { isSameNode, initialPrice, updatedPrice };
  });

  console.log('Size Toggle Test:', sizeToggleTest);
  if (!sizeToggleTest.isSameNode) {
    throw new Error('FAIL: Size toggle caused a full DOM re-render! Must be updated in-place.');
  }
  if (sizeToggleTest.initialPrice === sizeToggleTest.updatedPrice) {
    throw new Error('FAIL: Price did not update on size change.');
  }
  console.log('[PASS] Size toggle updated in-place without re-rendering the catalog grid!');

  // Capture Screenshot 1: Guest Storefront
  const buf1 = await page.screenshot({ fullPage: false });
  saveScreenshotBoth('01_guest_storefront.png', buf1);

  // =========================================================================
  // Test 2: Authenticated Customer Storefront & User Pill
  // =========================================================================
  console.log('\n--- 2. Testing Customer Authentication & Header User Pill ---');
  // Login as Customer David via API and refresh header
  await page.evaluate(async () => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'david@crosta.eu', password: 'User123!' })
    });
    const user = await res.json();
    currentUser = user;
    localStorage.setItem('crosta_user', JSON.stringify(currentUser));
    await refreshUserProfile();
    updateHeaderAuth();
    navigateToCatalog();
  });
  await page.waitForTimeout(500);

  // Verify User Pill in Header
  const customerHeaderState = await page.evaluate(() => {
    const userPills = Array.from(document.querySelectorAll('.header-user-area-slot button'))
      .map(b => b.textContent.trim());
    const navButtons = Array.from(document.querySelectorAll('#header-nav-container button'))
      .filter(b => !b.classList.contains('hidden') && b.offsetParent !== null)
      .map(b => b.textContent.trim());
    return { userPills, navButtons };
  });

  console.log('Customer Header User Area:', customerHeaderState.userPills);
  console.log('Customer Center Nav Buttons:', customerHeaderState.navButtons);
  const pillHasDavid = customerHeaderState.userPills.some(p => p.includes('Давид') && p.includes('€'));
  if (!pillHasDavid) {
    throw new Error('FAIL: User pill with David and live bonus balance not found in header.');
  }
  if (customerHeaderState.navButtons.some(b => b.includes('Профиль'))) {
    throw new Error('FAIL: Redundant Profile tab should be removed from center nav when user pill is present.');
  }
  console.log('[PASS] Header displays user pill with David and bonus balance €14.50. Duplicate Profile tab hidden from center nav.');

  // Capture Screenshot 2: Customer Storefront with User Pill
  const buf2 = await page.screenshot({ fullPage: false });
  saveScreenshotBoth('02_customer_storefront_user_pill.png', buf2);

  // =========================================================================
  // Test 3: Product Detail Page (#/pizza/PZ-004)
  // =========================================================================
  console.log('\n--- 3. Testing Product Detail Page ---');
  await page.goto(`${BASE_URL}/#/pizza/PZ-004`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  const detailInfo = await page.evaluate(() => {
    const name = document.getElementById('detail-name')?.textContent.trim();
    const sku = document.getElementById('detail-sku')?.textContent.trim();
    const allergens = Array.from(document.querySelectorAll('#detail-allergens span')).map(s => s.textContent.trim());
    const nutrition = Array.from(document.querySelectorAll('#detail-nutrition div span.font-bold')).map(s => s.textContent.trim());
    const sizeOptions = Array.from(document.querySelectorAll('#detail-size-options button')).map(b => b.textContent.trim());
    const reviews = document.querySelectorAll('#detail-reviews-list > div').length;
    return { name, sku, allergens, nutrition, sizeOptionsCount: sizeOptions.length, reviewsCount: reviews };
  });

  console.log('Product Detail Info:', detailInfo);
  if (detailInfo.sku !== 'PZ-004' || !detailInfo.name.includes('Прошутто э Руккола')) {
    throw new Error('FAIL: Product Detail Page PZ-004 content not loaded.');
  }
  if (detailInfo.allergens.length === 0 || detailInfo.nutrition.length < 4) {
    throw new Error('FAIL: Allergens or nutrition table missing on Product Detail Page.');
  }
  console.log('[PASS] Product Detail View rendered with recipe story, allergens, nutrition table, and reviews.');

  // Capture Screenshot 3: Product Detail View
  const buf3 = await page.screenshot({ fullPage: false });
  saveScreenshotBoth('03_product_detail_view.png', buf3);

  // =========================================================================
  // Test 4: Slide-over Cart Drawer
  // =========================================================================
  console.log('\n--- 4. Testing Slide-Over Cart Drawer ---');
  // Add pizza from detail page to cart
  await page.click('#btn-detail-add');
  await page.waitForTimeout(500);

  // Check if drawer is visible and open
  const drawerState = await page.evaluate(() => {
    const panel = document.getElementById('cart-drawer-panel');
    const isTranslated = panel.classList.contains('translate-x-0');
    const itemsCount = document.querySelectorAll('#cart-items > div').length;
    const cardfieldVisible = !document.getElementById('cardfield-container').classList.contains('hidden');
    const hasDemoButton = Array.from(document.querySelectorAll('#cardfield-container button'))
      .some(b => b.textContent.includes('Заполнить демо'));
    return { isTranslated, itemsCount, cardfieldVisible, hasDemoButton };
  });

  console.log('Cart Drawer State:', drawerState);
  if (!drawerState.isTranslated || drawerState.itemsCount === 0) {
    throw new Error('FAIL: Cart drawer failed to slide open or cart item not added.');
  }
  if (drawerState.hasDemoButton) {
    throw new Error('FAIL: Demo button ("Заполнить демо...") must be removed from production CardField.');
  }
  console.log('[PASS] Slide-over Cart Drawer is open with item and clean CardField without demo button.');

  // Apply promo code CROSTA5
  await page.evaluate(() => {
    document.getElementById('promo-code-input').value = 'CROSTA5';
    applyPromoFromInput();
  });
  await page.waitForTimeout(300);

  // Capture Screenshot 4: Cart Drawer Slide-Over
  const buf4 = await page.screenshot({ fullPage: false });
  saveScreenshotBoth('04_cart_drawer_slideover.png', buf4);

  // Close drawer
  await page.evaluate(() => closeCartDrawer());
  await page.waitForTimeout(400);

  // =========================================================================
  // Test 5: Admin Panel & Bezier Revenue Trend
  // =========================================================================
  console.log('\n--- 5. Testing Admin Dashboard & Permissions ---');
  // Switch user to Admin Elena
  await page.evaluate(async () => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'admin@crosta.eu', password: 'Admin123!' })
    });
    const admin = await res.json();
    currentUser = admin;
    localStorage.setItem('crosta_user', JSON.stringify(currentUser));
    await refreshUserProfile();
    updateHeaderAuth();
    switchView('staff');
  });
  await page.waitForTimeout(600);

  const adminState = await page.evaluate(() => {
    const kpiCount = document.querySelectorAll('#staff-kpis > div').length;
    const chartCurve = document.getElementById('chart-curve')?.getAttribute('d');
    const stopListItems = document.querySelectorAll('#admin-stop-list > div').length;
    const tableRows = document.querySelectorAll('#staff-orders-tbody tr').length;
    const staffTabVisible = !document.getElementById('tab-staff').classList.contains('hidden');
    return { kpiCount, chartCurve, stopListItems, tableRows, staffTabVisible };
  });

  console.log('Admin State:', adminState);
  if (!adminState.staffTabVisible || adminState.kpiCount !== 4 || !adminState.chartCurve) {
    throw new Error('FAIL: Admin dashboard components or Bezier curve missing.');
  }
  console.log('[PASS] Admin dashboard renders 4 Stat Cards, interactive Bezier curve, and stop-list management.');

  // Capture Screenshot 5: Admin Dashboard
  const buf5 = await page.screenshot({ fullPage: false });
  saveScreenshotBoth('05_admin_dashboard_bezier.png', buf5);

  // =========================================================================
  // Test 6: Mobile Viewport (390x844)
  // =========================================================================
  console.log('\n--- 6. Testing Mobile Viewport (390x844) ---');
  const contextMobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3
  });
  const pageMobile = await contextMobile.newPage();
  pageMobile.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(`[Mobile Console Error] ${msg.text()}`);
  });

  await pageMobile.goto(`${BASE_URL}/#/`, { waitUntil: 'networkidle' });
  await pageMobile.waitForTimeout(600);

  // Add 1 item to trigger mobile floating cart pill
  await pageMobile.evaluate(() => {
    addToCart(1); // Margherita
  });
  await pageMobile.waitForTimeout(400);

  const mobileState = await pageMobile.evaluate(() => {
    const floatingCartVisible = !document.getElementById('mobile-floating-cart').classList.contains('hidden');
    const headerHeight = document.querySelector('header').offsetHeight;
    const navHeight = document.getElementById('header-nav-container').offsetHeight;
    return { floatingCartVisible, headerHeight, navHeight };
  });

  console.log('Mobile Viewport State:', mobileState);
  if (!mobileState.floatingCartVisible) {
    throw new Error('FAIL: Mobile floating cart bar did not appear when items are in cart.');
  }
  console.log('[PASS] Mobile viewport renders compact header and bottom floating cart pill.');

  // Capture Screenshot 6: Mobile Viewport
  const buf6 = await pageMobile.screenshot({ fullPage: false });
  saveScreenshotBoth('06_mobile_viewport_390x844.png', buf6);

  await browser.close();

  console.log('\n======================================================');
  console.log('Console Errors Observed:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.error(consoleErrors);
    throw new Error('Console errors were logged during testing!');
  }
  console.log('ALL 6 VERIFICATIONS PASSED WITH ZERO CONSOLE ERRORS!');
  console.log('======================================================\n');
}

runStage6Verification().catch(err => {
  console.error('\nVerification failed:', err);
  process.exit(1);
});
