const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const targetDirs = [
  'C:\\Код\\PizzaOrderSystem\\screenshots\\baseline',
  'C:\\Users\\Limon\\.gemini\\antigravity\\brain\\9fffb143-0a4a-428c-b8f0-6fd2e625d429\\baseline'
];

targetDirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

async function run() {
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true
  });

  const viewports = [
    { name: 'desktop', width: 1440, height: 900 },
    { name: 'mobile', width: 390, height: 844 }
  ];

  for (const vp of viewports) {
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: 2
    });
    const page = await context.newPage();

    console.log(`Navigating to http://127.0.0.1:5000 for ${vp.name}...`);
    await page.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000); // ensure tailwind and menu rendering

    // 1. Store view
    for (const dir of targetDirs) {
      await page.screenshot({ path: path.join(dir, `${vp.name}_01_store.png`), fullPage: false });
    }
    console.log(`Captured ${vp.name}_01_store.png`);

    // 2. Track view
    await page.click('#tab-track');
    await page.waitForTimeout(500);
    for (const dir of targetDirs) {
      await page.screenshot({ path: path.join(dir, `${vp.name}_02_track.png`), fullPage: false });
    }
    console.log(`Captured ${vp.name}_02_track.png`);

    // 3. Staff view
    await page.click('#tab-staff');
    await page.waitForTimeout(500);
    for (const dir of targetDirs) {
      await page.screenshot({ path: path.join(dir, `${vp.name}_03_staff.png`), fullPage: false });
    }
    console.log(`Captured ${vp.name}_03_staff.png`);

    await context.close();
  }

  await browser.close();
  console.log('All baseline screenshots captured successfully.');
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
