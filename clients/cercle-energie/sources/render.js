const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, mode, a, b, c] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'overlay.html'));
  await page.evaluate(() => window.ready);
  if (mode === 'preview') {            // node render.js preview outdir t1,t2,...  (white checker bg)
    await page.addStyleTag({ content: 'html{background:#5d7a8c !important}' });
    for (const t of b.split(',')) {
      await page.evaluate(t => window.renderAt(t), +t);
      await page.screenshot({ path: path.join(a, `p_${(+t).toFixed(2)}.jpg`), type: 'jpeg', quality: 80 });
    }
  } else {                              // node render.js frames outdir startFrame endFrame  (fps 24)
    for (let f = +b; f < +c; f++) {
      await page.evaluate(t => window.renderAt(t), f / 24);
      await page.screenshot({ path: path.join(a, `f_${String(f).padStart(5, '0')}.png`), omitBackground: true });
    }
  }
  await browser.close();
})();
