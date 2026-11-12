const { chromium } = require('playwright'); const path = require('path');
const A = [
 ['H01-encore-vos-dossiers-a-21h','img/nuit-dossiers.jpg','40% 30%','21 h · Après le chantier','Encore vos dossiers<br>CEE <em>à 21 h ?</em>','On s’en occupe'],
 ['H02-vous-posez-on-gere','img/photo-chantier.jpg','45% 30%','Installateurs · Artisans','Vous posez.<br><em>On gère le dossier CEE.</em>','Rejoindre le réseau'],
 ['H03-pas-votre-metier','img/mains-dossiers.jpg','center 40%','Dossiers CEE','Le dossier CEE,<br><em>ce n’est pas votre métier.</em>','Confiez-le-nous'],
 ['H04-rentrez-chez-vous','img/fin-de-journee.jpg','40% 30%','Fin de chantier','Rentrez chez vous.<br><em>On s’occupe du dossier.</em>','Rejoindre le réseau'],
 ['H05-un-seul-interlocuteur','img/conseillere.jpg','center 25%','Mandataire CEE','Un seul interlocuteur<br><em>pour vos dossiers CEE.</em>','Rejoindre le réseau'],
 ['H06-moins-de-paperasse','paperasse.jpg','38% center','Aides CEE','Moins de paperasse.<br><em>Plus de chantiers.</em>','En savoir plus'],
 ['H07-vous-realisez-les-travaux','artisan-clients.jpg','60% center','Mandataire CEE','Vous réalisez les travaux.<br><em>Nous gérons vos aides CEE.</em>','Rejoindre le réseau'],
['R01-petit-artisan-pas-isole','reseau.jpg','46% center','Le réseau des artisans RGE','Petit artisan,<br><em>pas artisan isolé.</em>','Rejoindre le réseau'],
 ['R02-on-vous-aide-a-le-faire','img/nuit-dossiers.jpg','40% 30%','Petits artisans','Ce que vous n’arrivez pas à faire seul,<br><em>on vous aide à le faire.</em>','Rejoindre le réseau'],
 ['R03-pac-on-s-occupe-du-reste','pompe-a-chaleur.jpg','40% center','Installateurs de pompes à chaleur','Vous posez des pompes à chaleur.<br><em>On s’occupe du reste.</em>','Rejoindre le réseau'],
 ['R04-en-reseau-vous-pesez','fournisseur.jpg','56% center','Tarifs fournisseurs','Seul, vous négociez.<br><em>En réseau, vous pesez.</em>','Rejoindre le réseau'],
 ['R05-qualifie-rge','qualification-rge.jpg','38% center','Artisans qualifiés RGE','Qualifié RGE ?<br><em>Ne restez pas seul avec vos dossiers.</em>','Rejoindre le réseau'],
 ['R06-primes-expliquees','formation.jpg','72% center','Formation aux CEE','Les primes CEE,<br><em>enfin expliquées simplement.</em>','Rejoindre le réseau'],
 ['R07-qualification-rge','portrait-artisan.jpg','center 25%','Qualification RGE','La qualification RGE,<br><em>sans y laisser vos week-ends.</em>','Se faire accompagner'],
['L01-chantiers-soignes','artisan-clients.jpg','60% center','Artisans locaux','Vos chantiers sont soignés.<br><em>Vos dossiers aussi, désormais.</em>','Rejoindre le réseau'],
 ['L02-excellent-sur-le-chantier','img/photo-chantier.jpg','45% 8%','Artisans locaux','Excellent sur le chantier.<br><em>Perdu dans les dossiers ?</em>','On vous aide'],
 ['L03-artisan-du-coin','portrait-artisan.jpg','center 25%','Artisans de proximité','L’artisan du coin<br><em>mérite un vrai réseau.</em>','Rejoindre le réseau'],
];
(async () => { const b = await chromium.launch();
 for (const [n,img,pos,k,h,c] of A) for (const [f,w,hh] of [['carre',1080,1080],['portrait',1080,1350],['story',1080,1920]]) {
  const p = await b.newPage({ viewport: { width: w, height: hh } });
  const q = new URLSearchParams({ img, pos, k, h, c }); if (f==='story') q.set('story','1');
  await p.goto('file://' + path.resolve(__dirname,'visuel.html') + '?' + q); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname,'visuels',`${n}-${f}.jpg`), type:'jpeg', quality: 90 }); await p.close(); }
 await b.close(); })();
