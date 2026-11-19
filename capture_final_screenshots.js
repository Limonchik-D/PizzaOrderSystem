const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const targetDirs = [
  'C:\\Код\\PizzaOrderSystem\\screenshots\\final',
  'C:\\Users\\Limon\\.gemini\\antigravity\\brain\\9fffb143-0a4a-428c-b8f0-6fd2e625d429\\final'
];

targetDirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

async function saveScreenshots(page, name) {
  for (const dir of targetDirs) {
    await page.screenshot({ path: path.join(dir, `${name}.png`), fullPage: false });
  }
  console.log(`Saved screenshot: ${name}.png`);
}

async function run() {
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true
  });

  // =========================================================================
  // 1. Desktop 1440x900
  // =========================================================================
  const deskContext = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  const page = await deskContext.newPage();

  console.log('Navigating to http://127.0.0.1:5000 (Desktop)...');
  await page.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // 1.1 Storefront Light
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_01_store_light');

  // 1.2 Storefront Dark
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_02_store_dark');

  // Switch back to Light theme for modal, profile, cart, tracking
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(400);

  // 1.3 Auth Modal (Login / Register dialog with quick demo buttons)
  await page.evaluate(() => openAuthModal('login'));
  await page.waitForTimeout(500);
  await saveScreenshots(page, 'desktop_03_auth_modal');
  await page.evaluate(() => closeAuthModal());
  await page.waitForTimeout(300);

  // 1.4 Profile & Loyalty Club (David logged in)
  await page.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await page.waitForTimeout(1000);
  await page.click('#tab-profile');
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_04_profile_loyalty');

  // 1.5 Cart & Checkout with Bonus Deduction
  await page.click('#tab-store');
  await page.waitForTimeout(500);
  const addBtn = await page.$('#menu-grid article:first-child button:has-text("В корзину")');
  if (addBtn) {
    await addBtn.click();
    await page.waitForTimeout(500);
  }
  // Adjust bonus slider
  await page.evaluate(() => {
    const slider = document.getElementById('bonus-spend-slider');
    if (slider) {
      slider.value = '3.00';
      setBonusSpend(3.00);
    }
  });
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_05_cart_checkout_bonuses');

  // 1.6 Order Tracking Screen
  await page.click('#tab-track');
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_06_order_tracking');

  // 1.7 Admin Analytics Dashboard (Elena logged in)
  await page.evaluate(() => demoLogin('admin@crosta.eu', 'Admin123!'));
  await page.waitForTimeout(1000);
  await page.click('#tab-staff');
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_07_admin_dashboard');

  // 1.8 Admin Analytics Dashboard in Dark Theme
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_08_admin_dashboard_dark');

  await deskContext.close();

  // =========================================================================
  // 2. Mobile 390x844
  // =========================================================================
  const mobContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2
  });
  const mobPage = await mobContext.newPage();

  console.log('Navigating to http://127.0.0.1:5000 (Mobile)...');
  await mobPage.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await mobPage.waitForTimeout(1000);

  // 2.1 Mobile Storefront Light
  await mobPage.evaluate(() => {
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
      toggleTheme();
    }
    window.scrollTo(0, 0);
  });
  await mobPage.waitForTimeout(400);
  await saveScreenshots(mobPage, 'mobile_01_store_light');

  // 2.2 Mobile Storefront Dark
  await mobPage.evaluate(() => toggleTheme());
  await mobPage.waitForTimeout(400);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_02_store_dark');

  // Switch back to Light
  await mobPage.evaluate(() => toggleTheme());
  await mobPage.waitForTimeout(400);

  // 2.3 Mobile Profile & Loyalty Card (David logged in)
  await mobPage.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await mobPage.waitForTimeout(1000);
  await mobPage.click('#tab-profile');
  await mobPage.waitForTimeout(500);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_03_profile_loyalty');

  // 2.4 Mobile Tracking
  await mobPage.click('#tab-track');
  await mobPage.waitForTimeout(500);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_04_tracking');

  // 2.5 Mobile Admin Dashboard (Elena logged in)
  await mobPage.evaluate(() => demoLogin('admin@crosta.eu', 'Admin123!'));
  await mobPage.waitForTimeout(1000);
  await mobPage.click('#tab-staff');
  await mobPage.waitForTimeout(600);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_05_admin_dashboard');

  await mobContext.close();
  await browser.close();

  console.log('Stage 4 final verification screenshots captured successfully!');
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
