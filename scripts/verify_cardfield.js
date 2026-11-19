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

async function verifyCardField() {
  console.log('=== Verifying Kokonut UI CardField (MIT) Adaptation ===');
  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
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

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  // Set dark theme to match store styling
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    // Add item to cart and open cart drawer
    addToCart(1);
    openCartDrawer();
  });
  await page.waitForTimeout(500);

  // 1. Verify CardField container is visible in checkout
  const isVisible = await page.$eval('#cardfield-container', el => !el.classList.contains('hidden'));
  console.log(`CardField container visible: ${isVisible}`);
  if (!isVisible) throw new Error('CardField container is not visible');

  // Check initial placeholder and unknown brand
  const placeholderText = await page.$eval('#cardfield-placeholder', el => el.textContent.trim());
  console.log(`Initial placeholder: "${placeholderText}"`);

  // 2. Test typing test card using fillTestCard()
  console.log('Calling fillTestCard()...');
  await page.evaluate(() => fillTestCard());
  // Wait for the keystroke animation sequence to complete (~1200ms)
  await page.waitForTimeout(1600);

  // Check that card number collapsed and Expiry & CVC are populated
  const isCollapsed = await page.evaluate(() => cardState.isCollapsed);
  const extraVisible = await page.$eval('#cardfield-extra', el => !el.classList.contains('hidden'));
  const expVal = await page.$eval('#cardfield-exp-input', el => el.value);
  const cvcVal = await page.$eval('#cardfield-cvc-input', el => el.value);
  const brandName = await page.$eval('#cardfield-brand-name', el => el.textContent.trim());

  console.log(`Card State after fillTestCard:`, {
    isCollapsed,
    extraVisible,
    expVal,
    cvcVal,
    brandName
  });

  if (!isCollapsed || !extraVisible) {
    throw new Error('CardField failed to collapse or show extra fields');
  }

  // 3. Test CVC focus and card flip
  console.log('Focusing CVC input to test card flip to back...');
  await page.focus('#cardfield-cvc-input');
  await page.waitForTimeout(400);

  const hintTextOnCvc = await page.$eval('#cardfield-hint-text', el => el.textContent.trim());
  console.log(`Hint on CVC focus: "${hintTextOnCvc}"`);

  // Scroll to checkout drawer area
  const drawerPanel = await page.$('#cart-drawer-panel');
  await drawerPanel.scrollIntoViewIfNeeded();

  // Capture Screenshot of Kokonut UI CardField in collapsed state with CVC focused and back-of-card flip!
  const cardfieldScreenshot = await page.screenshot({ fullPage: false });
  saveScreenshot('09_kokonut_cardfield.png', cardfieldScreenshot);

  // 4. Test expanding card number back
  console.log('Clicking collapsed card number to test expandCardNumber()...');
  await page.click('#cardfield-edit-btn');
  await page.waitForTimeout(300);

  const isExpanded = await page.evaluate(() => !cardState.isCollapsed);
  const extraHidden = await page.$eval('#cardfield-extra', el => el.classList.contains('hidden'));
  console.log(`Card State after expand:`, { isExpanded, extraHidden });

  if (!isExpanded || !extraHidden) {
    throw new Error('CardField failed to expand back');
  }

  // 5. Test Luhn failure shake
  console.log('Testing invalid Luhn number shake...');
  await page.evaluate(() => {
    const numInput = document.getElementById('cardfield-number-input');
    numInput.value = '4242 4242 4242 4241';
    handleNumberInput({ target: numInput });
  });
  await page.waitForTimeout(400);

  const hasErrorClass = await page.$eval('#cardfield-row', el => el.classList.contains('has-error'));
  const errorHint = await page.$eval('#cardfield-hint-text', el => el.textContent.trim());
  console.log(`Luhn validation error detected: ${hasErrorClass}, message: "${errorHint}"`);

  if (!hasErrorClass) {
    throw new Error('Luhn error class was not added on invalid card');
  }

  // Reset with test card
  await page.evaluate(() => fillTestCard());
  await page.waitForTimeout(1600);

  await browser.close();

  console.log(`\nCardField verification passed with ${consoleErrors.length} console errors.`);
  if (consoleErrors.length > 0) {
    console.error('Errors found:', consoleErrors);
    process.exit(1);
  }
}

verifyCardField().catch(err => {
  console.error('CardField verification failed:', err);
  process.exit(1);
});
