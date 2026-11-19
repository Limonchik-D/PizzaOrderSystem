const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://127.0.0.1:5000';
const OUT_DIR = path.join(__dirname, '..', 'screenshots', 'word_roll');

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function runWordRollVerification() {
  console.log('--- Verifying Word Roll Integration ---');
  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const consoleErrors = [];

  // Desktop Test
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(`[Console Error] ${msg.text()}`);
  });
  page.on('pageerror', err => consoleErrors.push(`[Page Error] ${err.message}`));

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });

  // 1. Verify Hero Word Roll
  console.log('Testing Hero Word Roll...');
  const heroRollExists = await page.$('#hero-word-roll');
  if (!heroRollExists) throw new Error('Hero Word Roll element #hero-word-roll not found!');

  const initialWord = await page.$eval('#hero-roll-slot .word', el => el.textContent);
  console.log(`[PASS] Initial Hero word: "${initialWord}"`);

  // Initial slot width
  const initialWidth = await page.$eval('#hero-roll-slot', el => parseFloat(el.style.width || el.offsetWidth));
  console.log(`[PASS] Initial Hero slot width: ${initialWidth}px`);

  // Take screenshot of Initial Hero
  await page.screenshot({
    path: path.join(OUT_DIR, '01_hero_word_roll_initial.png'),
    clip: { x: 0, y: 0, width: 1440, height: 500 }
  });
  console.log('Saved 01_hero_word_roll_initial.png');

  // Click Hero Roll to trigger next word
  console.log('Clicking Hero Word Roll...');
  await page.click('#hero-word-roll');
  await page.waitForTimeout(400);

  const nextWord = await page.$eval('#hero-roll-slot .word:last-child', el => el.textContent);
  const updatedWidth = await page.$eval('#hero-roll-slot', el => parseFloat(el.style.width || el.offsetWidth));
  console.log(`[PASS] Next Hero word after click: "${nextWord}", updated slot width: ${updatedWidth}px`);

  // Screenshot of Next Hero Word Roll
  await page.screenshot({
    path: path.join(OUT_DIR, '02_hero_word_roll_transition.png'),
    clip: { x: 0, y: 0, width: 1440, height: 500 }
  });
  console.log('Saved 02_hero_word_roll_transition.png');

  // 2. Verify Bottom Showcase Word Roll
  console.log('\nTesting Bottom Showcase Word Roll...');
  const showcaseRollExists = await page.$('#roll');
  if (!showcaseRollExists) throw new Error('Showcase Word Roll element #roll not found!');

  await page.evaluate(() => {
    document.getElementById('roll')?.scrollIntoView({ behavior: 'instant', block: 'center' });
  });
  await page.waitForTimeout(300);

  const initialShowcaseWord = await page.$eval('#slot .word', el => el.textContent);
  console.log(`[PASS] Initial Showcase word: "${initialShowcaseWord}"`);

  // Click "Сменить слово"
  console.log('Clicking "Сменить слово ⟳"...');
  await page.click('button:has-text("Сменить слово ⟳")');
  await page.waitForTimeout(450);

  const secondShowcaseWord = await page.$eval('#slot .word:last-child', el => el.textContent);
  console.log(`[PASS] Showcase word after click: "${secondShowcaseWord}"`);

  // Click Slow-Mo
  console.log('Testing Slow-Mo toggle...');
  await page.click('#btn-slow-mo');
  await page.waitForTimeout(100);
  const slowMoText = await page.$eval('#btn-slow-mo', el => el.textContent);
  console.log(`[PASS] Slow-Mo button state: "${slowMoText.trim()}"`);

  // Screenshot of Bottom Showcase
  const showcaseCard = await page.$('#roll').then(el => el.evaluateHandle(node => node.closest('div.bg-surface')));
  if (showcaseCard) {
    await showcaseCard.asElement().screenshot({
      path: path.join(OUT_DIR, '03_showcase_word_roll.png')
    });
    console.log('Saved 03_showcase_word_roll.png');
  }

  // 3. Mobile 390x844 Viewport Test
  console.log('\nTesting Mobile 390x844 Viewport...');
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(BASE_URL, { waitUntil: 'networkidle' });

  await mobilePage.screenshot({
    path: path.join(OUT_DIR, '04_mobile_hero_word_roll.png'),
    clip: { x: 0, y: 0, width: 390, height: 600 }
  });
  console.log('Saved 04_mobile_hero_word_roll.png');

  await mobileContext.close();
  await context.close();
  await browser.close();

  console.log('\n=== Console Errors Report ===');
  if (consoleErrors.length === 0) {
    console.log('[SUCCESS] 0 console or page errors detected!');
  } else {
    console.warn(`[WARNING] Console errors:`, consoleErrors);
  }

  console.log('--- Word Roll Verification Finished Successfully ---');
}

runWordRollVerification().catch(err => {
  console.error('Verification failed:', err);
  process.exit(1);
});
