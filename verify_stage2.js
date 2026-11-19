const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const targetDirs = [
  'C:\\Код\\PizzaOrderSystem\\screenshots\\stage2',
  'C:\\Users\\Limon\\.gemini\\antigravity\\brain\\9fffb143-0a4a-428c-b8f0-6fd2e625d429\\stage2'
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
  // 1. Desktop 1440x900 (Light & Dark)
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
  await saveScreenshots(page, 'desktop_01_store_light');

  // 1.2 Tracking Light
  await page.click('#tab-track');
  await page.waitForTimeout(500);
  await saveScreenshots(page, 'desktop_02_track_light');

  // 1.3 Login as David via quick demo button & Profile Light
  await page.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await page.waitForTimeout(1000);
  await page.click('#tab-profile');
  await page.waitForTimeout(500);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_03_profile_david_light');

  // 1.4 Cart with Bonuses (David logged in)
  await page.click('#tab-store');
  await page.waitForTimeout(500);
  const addBtn = await page.$('#menu-grid article:first-child button:has-text("В корзину")');
  if (addBtn) {
    await addBtn.click();
    await page.waitForTimeout(500);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await saveScreenshots(page, 'desktop_04_cart_with_bonuses_light');

  // 1.5 Switch to Admin Elena & Staff/Admin view Light
  await page.evaluate(() => demoLogin('admin@crosta.eu', 'Admin123!'));
  await page.waitForTimeout(1000);
  await page.click('#tab-staff');
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_05_admin_dashboard_light');

  // 1.6 Dark Theme: Toggle Theme
  await page.evaluate(() => toggleTheme());
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await saveScreenshots(page, 'desktop_06_admin_dashboard_dark');

  // Dark Theme Storefront
  await page.click('#tab-store');
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_07_store_dark');

  // Dark Theme Profile (Switch back to David)
  await page.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await page.waitForTimeout(1000);
  await page.click('#tab-profile');
  await page.waitForTimeout(500);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);
  await saveScreenshots(page, 'desktop_08_profile_dark');

  await deskContext.close();

  // =========================================================================
  // 2. Mobile 390x844 (Light & Dark)
  // =========================================================================
  const mobContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2
  });
  const mobPage = await mobContext.newPage();

  console.log('Navigating to http://127.0.0.1:5000 (Mobile)...');
  await mobPage.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await mobPage.waitForTimeout(1000);

  // Mobile Storefront Light
  await saveScreenshots(mobPage, 'mobile_01_store_light');

  // Mobile Tracking Light
  await mobPage.click('#tab-track');
  await mobPage.waitForTimeout(400);
  await saveScreenshots(mobPage, 'mobile_02_track_light');

  // Mobile Profile Light (Login as David)
  await mobPage.evaluate(() => demoLogin('david@crosta.eu', 'User123!'));
  await mobPage.waitForTimeout(1000);
  await mobPage.click('#tab-profile');
  await mobPage.waitForTimeout(400);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_03_profile_light');

  // Mobile Dark Theme
  await mobPage.evaluate(() => toggleTheme());
  await mobPage.waitForTimeout(400);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await saveScreenshots(mobPage, 'mobile_04_profile_dark');

  // Mobile Storefront Dark
  await mobPage.click('#tab-store');
  await mobPage.waitForTimeout(400);
  await mobPage.evaluate(() => window.scrollTo(0, 0));
  await mobPage.waitForTimeout(300);
  await saveScreenshots(mobPage, 'mobile_05_store_dark');

  await mobContext.close();
  await browser.close();

  console.log('Stage 2 verification screenshots completed successfully!');
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
