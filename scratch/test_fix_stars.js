const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:5000/#/pizza/PZ-004');
  await page.waitForTimeout(500);
  await page.click('button:has-text("+ Оставить отзыв")');
  await page.waitForTimeout(400);

  // Apply fix in browser memory to test:
  await page.evaluate(() => {
    // Remove CSS fill from stylesheet
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) {
          if (rule.selectorText && rule.selectorText.includes('.db-star-btn path')) {
            rule.style.fill = '';
            rule.style.stroke = '';
          }
        }
      } catch (e) {}
    }

    // Set inline styles on all star paths
    const paths = document.querySelectorAll('#detail-star-rating-slot .db-star-btn path');
    paths.forEach((p, idx) => {
      if (idx < 4) {
        p.style.fill = 'rgb(255, 210, 63)';
        p.style.stroke = 'rgb(255, 210, 63)';
        p.style.filter = 'drop-shadow(0 0 6px rgba(255, 210, 63, 0.4))';
      }
    });
  });

  const starPaths = await page.$$eval('#detail-star-rating-slot .db-star-btn path', paths => {
    return paths.map(p => ({
      computedFill: getComputedStyle(p).fill,
      computedStroke: getComputedStyle(p).stroke
    }));
  });
  console.log('Fixed computed styles:', JSON.stringify(starPaths, null, 2));

  // Take screenshot of fixed stars
  const reviewForm = await page.$('#detail-review-form');
  const buffer = await reviewForm.screenshot();
  const fs = require('fs');
  fs.writeFileSync('scratch/test_fixed_stars.png', buffer);
  console.log('Saved scratch/test_fixed_stars.png');

  await browser.close();
})();
