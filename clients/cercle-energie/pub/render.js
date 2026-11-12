const { chromium } = require('playwright'); const path = require('path');
const A = [
 ['C01-vous-installez','img/photo-chantier.jpg','45% 32%','Installateurs · Chauffagistes','Vous installez.<br><em>Nous vous accompagnons à chaque étape.</em>'],
 ['C02-dossiers-suivis','qualification-rge.jpg','38% center','Mandataire CEE','Des dossiers suivis, des règles expliquées,<br><em>un partenaire à vos côtés.</em>'],
 ['C03-un-seul-cercle','reseau.jpg','46% center','Le partenaire unique de vos projets','Du premier contact au paiement de la prime*,<br><em>un seul cercle de services.</em>'],
 ['C04-moins-d-administratif','img/mains-dossiers.jpg','center 40%','Avec des applications dédiées','Moins de temps dans l’administratif,<br><em>plus de temps sur vos chantiers.</em>'],
 ['C05-bons-equipements','fournisseur.jpg','56% center','Équipements · Outils','Les bons équipements, les bons outils,<br><em>le bon accompagnement.</em>'],
 ['C06-pompes-a-chaleur','pompe-a-chaleur.jpg','40% center','Pompes à chaleur','Vous posez des pompes à chaleur.<br><em>On vous accompagne sur le reste.</em>'],
 ['C07-isolation','isolation-combles.jpg','center','Isolation','Vous isolez.<br><em>Nous vous accompagnons à chaque étape.</em>'],
 ['L01-chantiers-soignes','artisan-clients.jpg','60% center','Artisans locaux','Vos chantiers sont soignés.<br><em>Vos dossiers le seront aussi.</em>'],
 ['L02-excellent-sur-le-chantier','portrait-artisan.jpg','center 25%','Artisans locaux','Excellent sur le chantier.<br><em>Perdu dans les dossiers ?</em>'],
 ['L03-artisan-local','img/fin-de-journee.jpg','40% 30%','Artisans de proximité','L’artisan local<br><em>mérite un vrai partenaire.</em>'],
 ['H01-encore-vos-dossiers-a-21h','img/nuit-dossiers.jpg','40% 30%','21 h · Après le chantier','Encore vos dossiers<br>CEE <em>à 21 h ?</em>'],
 ['H06-moins-de-paperasse','paperasse.jpg','38% center','Aides CEE','Moins de paperasse.<br><em>Plus de chantiers.</em>'],
].map(a => [...a, 'Parlons de vos projets']);
(async () => { const b = await chromium.launch();
 for (const [n,img,pos,k,h,c] of A) for (const [f,w,hh] of [['carre',1080,1080],['portrait',1080,1350],['story',1080,1920]]) {
  const p = await b.newPage({ viewport: { width: w, height: hh } });
  const q = new URLSearchParams({ img, pos, k, h, c }); if (f==='story') q.set('story','1');
  await p.goto('file://' + path.resolve(__dirname,'visuel.html') + '?' + q); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(500); console.log(n,f,await p.title());
  await p.screenshot({ path: path.join(__dirname,'visuels',`${n}-${f}.jpg`), type:'jpeg', quality: 90 }); await p.close(); }
 await b.close(); })();
