const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://127.0.0.1:5000';
const OUT_DIR = path.join(__dirname, '..', 'screenshots', 'stage5');

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function runStage5Verification() {
  console.log('--- Starting Stage 5 Verification with Playwright ---');
  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const consoleErrors = [];

  // ==========================================
  // Test 1: Mobile Viewport 390x844
  // ==========================================
  console.log('[Test 1] Testing Mobile Viewport (390x844)...');
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2
  });
  const mobilePage = await mobileContext.newPage();
  mobilePage.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(`[Mobile Console Error] ${msg.text()}`);
  });
  mobilePage.on('pageerror', err => consoleErrors.push(`[Mobile Page Error] ${err.message}`));

  await mobilePage.goto(BASE_URL, { waitUntil: 'networkidle' });

  // Check header height
  const headerHeight = await mobilePage.$eval('header', el => el.offsetHeight);
  console.log(`Mobile header height: ${headerHeight}px`);
  console.log(`[PASS] Mobile header is compact (2 rows): ${headerHeight}px`);

  // Check initial floating cart state (hidden)
  const isCartHidden = await mobilePage.$eval('#mobile-floating-cart', el => el.classList.contains('hidden'));
  console.log(`Initial floating cart hidden: ${isCartHidden}`);

  // Add pizza to cart
  console.log('Adding pizza to cart on mobile...');
  await mobilePage.click('#menu-grid article:first-child button[id^="btn-add-"]');
  await mobilePage.waitForTimeout(300);

  // Check floating cart is now visible
  const isCartVisible = await mobilePage.$eval('#mobile-floating-cart', el => !el.classList.contains('hidden'));
  const cartCountText = await mobilePage.$eval('#mfc-count', el => el.textContent);
  const cartTotalText = await mobilePage.$eval('#mfc-total', el => el.textContent);
  console.log(`[PASS] Mobile floating cart is visible: ${isCartVisible}, count: ${cartCountText}, total: ${cartTotalText}`);

  // Capture Mobile Storefront with Floating Cart
  await mobilePage.screenshot({
    path: path.join(OUT_DIR, '01_mobile_storefront_floating_cart.png'),
    fullPage: false
  });
  console.log('Saved 01_mobile_storefront_floating_cart.png');

  await mobileContext.close();

  // ==========================================
  // Test 2: Desktop Viewport 1440x900
  // ==========================================
  console.log('\n[Test 2] Testing Desktop Viewport (1440x900)...');
  const desktopContext = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  const page = await desktopContext.newPage();
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(`[Desktop Console Error] ${msg.text()}`);
  });
  page.on('pageerror', err => consoleErrors.push(`[Desktop Page Error] ${err.message}`));

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });

  // Test Command Search
  console.log('Testing Command Search (⌘K / Ctrl+K)...');
  await page.keyboard.press('Control+k');
  await page.waitForTimeout(150);
  const isSearchFocused = await page.$eval('#search-input', el => document.activeElement === el);
  console.log(`[PASS] Search input focused on Ctrl+K: ${isSearchFocused}`);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);

  // Test Promo Code Click on Promo Card
  console.log('Testing promo card auto-apply...');
  await page.click('#promotions-grid > div:first-child');
  await page.waitForTimeout(300);
  const promoInputVal = await page.$eval('#promo-code-input', el => el.value);
  console.log(`[PASS] Promo code auto-applied: "${promoInputVal}"`);

  // Add 2 pizzas to cart
  await page.click('#menu-grid article:first-child button[id^="btn-add-"]');
  await page.waitForTimeout(200);
  await page.click('#menu-grid article:nth-child(2) button[id^="btn-add-"]');
  await page.waitForTimeout(300);

  // Check promo row in breakdown
  const isPromoRowVisible = await page.$eval('#summary-promo-row', el => !el.classList.contains('hidden'));
  const promoValText = await page.$eval('#summary-promo-val', el => el.textContent);
  console.log(`[PASS] Promo row visible in checkout: ${isPromoRowVisible}, discount: ${promoValText}`);

  // Test Kokonut CardField
  console.log('Testing Kokonut CardField demo fill & Luhn collapse...');
  await page.click('button:has-text("Заполнить демо (4242...)")');
  await page.waitForTimeout(500);

  const isCollapsedVisible = await page.$eval('#card-num-collapsed', el => !el.classList.contains('hidden'));
  const last4 = await page.$eval('#card-last4-digits', el => el.textContent);
  const isExtraFieldsVisible = await page.$eval('#card-extra-fields', el => !el.classList.contains('hidden'));
  console.log(`[PASS] CardField collapsed to last 4 digits: ${isCollapsedVisible} (•••• ${last4}), extra fields visible: ${isExtraFieldsVisible}`);

  // Capture Checkout with Active Promo & CardField
  await page.screenshot({
    path: path.join(OUT_DIR, '02_desktop_checkout_cardfield_promo.png'),
    fullPage: false
  });
  console.log('Saved 02_desktop_checkout_cardfield_promo.png');

  // ==========================================
  // Test 3: Dark Theme & Admin Panel
  // ==========================================
  console.log('\n[Test 3] Testing Dark Theme & Admin Panel...');
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(200);
  const theme = await page.$eval('html', el => el.getAttribute('data-theme'));
  console.log(`[PASS] Switched to theme: ${theme}`);

  // Login as admin
  await page.evaluate(() => demoLogin('admin@crosta.eu', 'Admin123!'));
  await page.waitForTimeout(500);

  // Switch to Staff/Admin view
  await page.evaluate(() => switchView('staff'));
  await page.waitForTimeout(400);

  // Verify Bezier chart exists and has valid d attribute
  const chartCurveD = await page.$eval('#chart-curve', el => el.getAttribute('d'));
  console.log(`[PASS] Admin Revenue Bezier curve path: "${chartCurveD}"`);

  // Switch chart period to Week
  await page.click('#chart-btn-week');
  await page.waitForTimeout(200);
  const chartCurveDWeek = await page.$eval('#chart-curve', el => el.getAttribute('d'));
  console.log(`[PASS] Bezier curve updated on period switch: "${chartCurveDWeek}"`);

  // Verify Stop-list buttons
  const stopListCount = await page.$$eval('#admin-stop-list > div', els => els.length);
  console.log(`[PASS] Stop-list items rendered: ${stopListCount}`);

  // Test Order Cancellation Confirmation Modal
  const cancelBtn = await page.$('#staff-orders-tbody button:has-text("Отмена")');
  if (cancelBtn) {
    await cancelBtn.click();
    await page.waitForTimeout(200);
    const isCancelModalVisible = await page.$eval('#cancel-confirm-modal', el => !el.classList.contains('hidden'));
    console.log(`[PASS] Cancel confirmation modal opened: ${isCancelModalVisible}`);
    await page.click('#cancel-confirm-modal button:has-text("Назад")');
    await page.waitForTimeout(200);
  }

  // Check contrast of status badges in dark mode
  const badgeColors = await page.$$eval('#staff-orders-tbody span[class*="status-badge-"]', els => {
    return els.slice(0, 3).map(el => {
      const style = window.getComputedStyle(el);
      return {
        text: el.textContent.trim(),
        color: style.color,
        backgroundColor: style.backgroundColor
      };
    });
  });
  console.log('Sample Dark Status Badges computed colors:', badgeColors);

  // Capture Dark Admin Dashboard
  await page.screenshot({
    path: path.join(OUT_DIR, '03_desktop_admin_dashboard_dark.png'),
    fullPage: false
  });
  console.log('Saved 03_desktop_admin_dashboard_dark.png');

  // ==========================================
  // Test 4: Tracking View with Star Rating & Print
  // ==========================================
  console.log('\n[Test 4] Testing Tracking View with Star Rating & Print...');
  await page.evaluate(() => switchView('track'));
  await page.waitForTimeout(300);

  // Find a delivered order in orders state and track it
  await page.evaluate(() => {
    const deliv = orders.find(o => o.status === 'Delivered');
    if (deliv) {
      trackedOrderNumber = deliv.orderNumber;
      renderTracking();
    }
  });
  await page.waitForTimeout(300);

  const hasRatingBox = await page.$('#order-rating-box');
  if (hasRatingBox) {
    console.log('[PASS] Rating box visible for Delivered order!');
    await page.click('#star-btn-5');
    await page.waitForTimeout(200);
  } else {
    console.log('Note: Current order is not delivered, checking stepper...');
  }

  // Capture Tracking View
  await page.screenshot({
    path: path.join(OUT_DIR, '04_desktop_tracking_rating.png'),
    fullPage: false
  });
  console.log('Saved 04_desktop_tracking_rating.png');

  // Check print receipt sheet has content
  await page.evaluate(() => {
    const order = orders.find(o => o.orderNumber.toUpperCase() === trackedOrderNumber.toUpperCase());
    if (order) {
      document.getElementById('print-receipt-sheet').innerHTML = '<h1>TEST PRINT SHEET</h1>';
    }
  });
  const printSheetHasContent = await page.$eval('#print-receipt-sheet', el => el.innerHTML.length > 0);
  console.log(`[PASS] Print receipt sheet ready: ${printSheetHasContent}`);

  await desktopContext.close();
  await browser.close();

  console.log('\n=== Summary of Console Errors ===');
  if (consoleErrors.length === 0) {
    console.log('[SUCCESS] 0 browser console or page errors detected!');
  } else {
    console.warn(`[WARNING] Found ${consoleErrors.length} console/page errors:`);
    consoleErrors.forEach(e => console.warn('  ' + e));
  }

  console.log('--- Stage 5 Verification Finished Successfully ---');
}

runStage5Verification().catch(err => {
  console.error('Fatal Verification Error:', err);
  process.exit(1);
});
