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

function saveScreenshot(filename, buffer) {
  fs.writeFileSync(path.join(LOCAL_OUT_DIR, filename), buffer);
  fs.writeFileSync(path.join(ARTIFACT_OUT_DIR, filename), buffer);
  console.log(`[Screenshot Saved] ${filename}`);
}

async function verifyStarRating() {
  console.log('=== Verifying DesignBookmark Star Rating Spring Component ===');
  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1200, height: 900 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
      console.error(`[Browser Console Error] ${msg.text()}`);
    }
  });

  // Navigate to application
  await page.goto(`${BASE_URL}/#/pizza/PZ-004`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Set theme to dark to match user screenshot
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  });
  await page.waitForTimeout(300);

  // Ensure we are on PZ-004 detail page
  const skuText = await page.$eval('#detail-sku', el => el.textContent.trim());
  console.log(`Current product SKU: ${skuText}`);
  if (skuText !== 'PZ-004') {
    await page.evaluate(() => openProductDetailBySku('PZ-004'));
    await page.waitForTimeout(500);
  }

  // 1. Click "+ Оставить отзыв" to reveal the review form
  const reviewBtn = await page.$('button:has-text("+ Оставить отзыв")');
  await reviewBtn.click();
  await page.waitForTimeout(400);

  // Check that review form is visible
  const isFormVisible = await page.$eval('#detail-review-form', el => !el.classList.contains('hidden'));
  console.log(`Review form visible: ${isFormVisible}`);

  // Check that Star Rating component is rendered inside #detail-star-rating-slot
  const starBtns = await page.$$('#detail-star-rating-slot .db-star-btn');
  console.log(`Found star buttons: ${starBtns.length} (expected: 5)`);
  if (starBtns.length !== 5) {
    throw new Error(`Expected 5 star buttons, got ${starBtns.length}`);
  }

  // Verify initial rolling text
  const initialWordColTransform = await page.$eval('#detail-star-rating-slot .db-star-col', el => el.style.transform);
  console.log(`Initial word column transform: ${initialWordColTransform}`);

  // 2. Hover over Star 4
  console.log('Hovering over Star 4...');
  await starBtns[3].hover();
  await page.waitForTimeout(300);

  // 3. Click Star 4
  console.log('Clicking Star 4...');
  await starBtns[3].click();
  await page.waitForTimeout(400);

  // Capture screenshot of Star Rating in review form with rating 4
  await page.fill('#detail-review-input', 'Потрясающая неаполитанская классика с лёгким дымным ароматом дровяной печи! Тесто воздушное, бортики пышные.');
  await page.waitForTimeout(400);

  // Scroll to review form
  const reviewFormEl = await page.$('#detail-review-form');
  await reviewFormEl.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);

  const starRatingScreenshot = await page.screenshot({ fullPage: false });
  saveScreenshot('07_star_rating_detail.png', starRatingScreenshot);

  // 4. Submit the review
  console.log('Submitting review...');
  const submitBtn = await page.$('button:has-text("Опубликовать отзыв")');
  await submitBtn.click();
  await page.waitForTimeout(600);

  // Verify that the new review appears in the list with SVG stars
  const firstReviewStars = await page.$('#detail-reviews-list > div:first-child svg');
  console.log(`First review has SVG stars: ${firstReviewStars !== null}`);

  // 5. Test Tracking View Rating
  console.log('Testing Delivered Order Rating in Tracking View...');
  await page.evaluate(() => {
    switchView('track');
    trackedOrderNumber = 'ORD-2026-101';
    renderTracking();
  });
  await page.waitForTimeout(600);

  const trackStarBtns = await page.$$('#track-star-rating-slot .db-star-btn');
  console.log(`Tracking star buttons found: ${trackStarBtns.length} (expected: 5)`);

  const trackingRatingBox = await page.$('#order-rating-box');
  if (trackingRatingBox) {
    await trackingRatingBox.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const trackingScreenshot = await page.screenshot({ fullPage: false });
    saveScreenshot('08_star_rating_tracking.png', trackingScreenshot);
  }

  await browser.close();

  console.log(`Verification completed with ${consoleErrors.length} console errors.`);
  if (consoleErrors.length > 0) {
    console.error('Errors found:', consoleErrors);
    process.exit(1);
  }
}

verifyStarRating().catch(err => {
  console.error('Verification failed:', err);
  process.exit(1);
});
