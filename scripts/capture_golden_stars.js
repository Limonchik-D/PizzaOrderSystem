const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const LOCAL_OUT_DIR = path.join(__dirname, '..', 'screenshots', 'stage6');
const ARTIFACT_OUT_DIR = 'C:\\Users\\Limon\\.gemini\\antigravity\\brain\\9fffb143-0a4a-428c-b8f0-6fd2e625d429\\stage6';

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME_PATH });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });

  await page.goto('http://127.0.0.1:5000/#/pizza/PZ-004');
  await page.waitForTimeout(600);

  // Set dark theme
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  });
  await page.waitForTimeout(300);

  // Open review form
  await page.click('button:has-text("+ Оставить отзыв")');
  await page.waitForTimeout(400);

  // Click 4th star
  const starBtns = await page.$$('#detail-star-rating-slot .db-star-btn');
  await starBtns[3].hover();
  await page.waitForTimeout(200);
  await starBtns[3].click();
  await page.waitForTimeout(400);

  // Fill sample text
  await page.fill('#detail-review-input', 'Превосходное тесто длительной ферментации! Хрустящий бортик и нежнейший сыр.');
  await page.waitForTimeout(300);

  // Screenshot form
  const form = await page.$('#detail-review-form');
  const buffer = await form.screenshot();

  fs.writeFileSync(path.join(LOCAL_OUT_DIR, '07_star_rating_detail_golden.png'), buffer);
  fs.writeFileSync(path.join(ARTIFACT_OUT_DIR, '07_star_rating_detail_golden.png'), buffer);
  console.log('Saved 07_star_rating_detail_golden.png successfully!');

  await browser.close();
})();
