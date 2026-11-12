const { chromium } = require('playwright'); const path = require('path');
const A = [
 ['H01-encore-vos-dossiers-a-21h','img/nuit-dossiers.jpg','40% 30%','21 h · Après le chantier','Encore vos dossiers<br>CEE <em>à 21 h ?</em>','On s’en occupe'],
 ['H02-vous-posez-on-gere','img/photo-chantier.jpg','45% 30%','Installateurs · Artisans','Vous posez.<br><em>On gère le dossier CEE.</em>','Devenir partenaire'],
 ['H03-pas-votre-metier','img/mains-dossiers.jpg','center 40%','Dossiers CEE','Le dossier CEE,<br><em>ce n’est pas votre métier.</em>','Confiez-le-nous'],
 ['H04-rentrez-chez-vous','img/fin-de-journee.jpg','40% 30%','Fin de chantier','Rentrez chez vous.<br><em>On s’occupe du dossier.</em>','Devenir partenaire'],
 ['H05-un-seul-interlocuteur','img/conseillere.jpg','center 25%','Mandataire CEE','Un seul interlocuteur<br><em>pour vos dossiers CEE.</em>','Devenir partenaire'],
 ['H06-moins-de-paperasse','paperasse.jpg','38% center','Aides CEE','Moins de paperasse.<br><em>Plus de chantiers.</em>','En savoir plus'],
 ['H07-vous-realisez-les-travaux','artisan-clients.jpg','60% center','Mandataire CEE','Vous réalisez les travaux.<br><em>Nous gérons vos aides CEE.</em>','Devenir partenaire'],
];
(async () => { const b = await chromium.launch();
 for (const [n,img,pos,k,h,c] of A) for (const [f,w,hh] of [['carre',1080,1080],['portrait',1080,1350],['story',1080,1920]]) {
  const p = await b.newPage({ viewport: { width: w, height: hh } });
  const q = new URLSearchParams({ img, pos, k, h, c }); if (f==='story') q.set('story','1');
  await p.goto('file://' + path.resolve(__dirname,'visuel.html') + '?' + q); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname,'visuels',`${n}-${f}.jpg`), type:'jpeg', quality: 90 }); await p.close(); }
 await b.close(); })();
