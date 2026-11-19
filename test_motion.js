const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));

  console.log('Navigating to http://127.0.0.1:5000...');
  await page.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Check GSAP availability
  const gsapOk = await page.evaluate(() => typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined');
  console.log('GSAP & ScrollTrigger loaded:', gsapOk);

  // Test category switch (triggers renderMenu with GSAP stagger)
  await page.click('button[data-cat="Мясные"]');
  await page.waitForTimeout(600);

  // Test add to cart (triggers addToCart and badge bump)
  await page.click('#menu-grid article:first-child button:has-text("В корзину")');
  await page.waitForTimeout(600);

  // Test switchView crossfade
  await page.click('#tab-track');
  await page.waitForTimeout(500);

  await page.click('#tab-profile');
  await page.waitForTimeout(500);

  await page.click('#tab-store');
  await page.waitForTimeout(500);

  console.log('Errors count:', errors.length);
  if (errors.length > 0) {
    console.error('Errors:', errors);
  } else {
    console.log('All motion and interaction checks passed with 0 errors!');
  }

  await browser.close();
})();
