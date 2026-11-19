const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:5000/#/pizza/PZ-004');
  await page.waitForTimeout(500);
  await page.click('button:has-text("+ Оставить отзыв")');
  await page.waitForTimeout(400);

  const starPaths = await page.$$eval('#detail-star-rating-slot .db-star-btn path', paths => {
    return paths.map(p => ({
      attrFill: p.getAttribute('fill'),
      attrStroke: p.getAttribute('stroke'),
      styleFill: p.style.fill,
      computedFill: getComputedStyle(p).fill,
      computedStroke: getComputedStyle(p).stroke
    }));
  });
  console.log('Star paths styles:', JSON.stringify(starPaths, null, 2));
  await browser.close();
})();
