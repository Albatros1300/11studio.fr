const { chromium } = require('playwright'); const path = require('path');
const A = [
 ['A-dossiers-cee','pac-installation.jpg','60% center','Installateurs · Artisans','Vos dossiers CEE,<br><em>on s’en occupe.</em>','Devenir partenaire'],
 ['B-moins-de-paperasse','paperasse.jpg','70% center','Aides CEE','Moins de paperasse.<br><em>Plus de chantiers.</em>','En savoir plus'],
 ['C-vous-realisez-les-travaux','artisan-clients.jpg','center','Mandataire CEE','Vous réalisez les travaux.<br><em>Nous gérons vos aides CEE.</em>','Devenir partenaire'],
];
(async () => { const b = await chromium.launch();
 for (const [n,img,pos,k,h,c] of A) for (const [f,w,hh] of [['carre',1080,1080],['story',1080,1920]]) {
  const p = await b.newPage({ viewport: { width: w, height: hh } });
  const q = new URLSearchParams({ img, pos, k, h, c }); if (f==='story') q.set('story','1');
  await p.goto('file://' + path.resolve(__dirname,'visuel.html') + '?' + q); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname,'visuels',`${n}-${f}.jpg`), type:'jpeg', quality: 90 }); await p.close(); }
 await b.close(); })();
