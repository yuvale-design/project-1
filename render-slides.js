const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const HTML = 'file://' + path.resolve(__dirname, 'glidai-carousel.html');
const OUT = path.resolve(__dirname, 'slides');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=medium'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });

  await page.goto(HTML, { waitUntil: 'networkidle0', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 800));

  const count = await page.$$eval('.slide', s => s.length);
  console.log(`Found ${count} slides`);

  for (let i = 0; i < count; i++) {
    // Pin THIS slide to viewport 0,0 and hide everything else.
    // This bypasses any RTL / flex / scroll weirdness with clip.
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide');
      const labels = document.querySelectorAll('.label');
      slides.forEach((s, j) => s.style.display = (j === idx) ? '' : 'none');
      labels.forEach(l => l.style.display = 'none');
      const s = slides[idx];
      s.style.position = 'fixed';
      s.style.top = '0';
      s.style.left = '0';
      s.style.margin = '0';
      document.body.style.padding = '0';
      document.body.style.margin = '0';
      window.scrollTo(0, 0);
    }, i);

    await new Promise(r => setTimeout(r, 200));

    const file = path.join(OUT, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({
      path: file,
      type: 'png',
      clip: { x: 0, y: 0, width: 1080, height: 1350 },
      omitBackground: false,
    });
    console.log(`  ✓ ${path.basename(file)}`);
  }

  await browser.close();
  console.log('Done.');
})().catch(e => { console.error(e); process.exit(1); });
