const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/usr/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  
  const page = await browser.newPage();
  
  const htmlPath = path.join(__dirname, 'backcover.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });
  
  // Wait for fonts to load
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 2000));
  
  // Set viewport to match the exact dimensions (130mm x 198mm)
  // Use CSS mm units, so viewport in px at 96dpi: 130mm=491px, 198mm=748px
  // deviceScaleFactor 4 for high-res output
  await page.setViewport({ width: 491, height: 748, deviceScaleFactor: 4 });
  
  // Re-navigate after viewport change
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 2000));
  
  // Screenshot as PNG (high-res for print)
  await page.screenshot({
    path: path.join(__dirname, 'backcover-print.png'),
    fullPage: false,
    clip: { x: 0, y: 0, width: 491, height: 748 },
    omitBackground: false
  });
  
  // Also generate PDF
  await page.pdf({
    path: path.join(__dirname, 'backcover-print.pdf'),
    width: '130mm',
    height: '198mm',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });
  
  console.log('Generated backcover-print.png and backcover-print.pdf');
  
  await browser.close();
})();
