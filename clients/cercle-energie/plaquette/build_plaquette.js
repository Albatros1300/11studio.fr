// Plaquette Cercle Énergie — version « punch »
// Usage : NODE_PATH=<node_modules avec pptxgenjs> node build_plaquette.js
const pptxgen = require('pptxgenjs');
const path = require('path');
const IMG = (n) => path.join(__dirname, '..', 'site', 'assets', 'img', n);
const OV = (n) => path.join(__dirname, 'assets', n);

const C = { navy: '0B3566', navyD: '07264B', lime: 'B9E35A', green: '73AF01', greenD: '4E8A06', teal: '01B7BA', blue: '016CB4', white: 'FFFFFF', mist: 'F1F6FB', grey: '40577A', pale: 'CFE0F3' };
const F = 'Montserrat';
const W = 13.333, H = 7.5;

const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.title = 'Cercle Énergie — Plaquette de présentation';
p.company = 'Cercle Énergie';
p.theme = { headFontFace: F, bodyFontFace: F };

// ---------- helpers
const T = (s, text, o) => s.addText(text, Object.assign({ fontFace: F, color: C.white, margin: 0, valign: 'top', fit: 'none' }, o));
const photo = (s, name, ov) => {
  s.addImage({ path: IMG(name), x: 0, y: 0, w: W, h: H, sizing: { type: 'cover', w: W, h: H } });
  if (ov) s.addImage({ path: OV(ov), x: 0, y: 0, w: W, h: H });
};
const ring = (s, x, y, d, color, pt, transp) => s.addShape(p.ShapeType.ellipse, { x, y, w: d, h: d, fill: { type: 'none' }, line: { color, width: pt, transparency: transp == null ? 0 : transp } });
const kicker = (s, text, x, y, color) => {
  s.addShape(p.ShapeType.roundRect, { x, y: y + 0.09, w: 0.55, h: 0.07, fill: { color: C.green }, line: { type: 'none' }, rectRadius: 0.03 });
  T(s, text.toUpperCase(), { x: x + 0.72, y, w: 9, h: 0.28, fontSize: 12, bold: true, charSpacing: 4, color: color || C.lime });
};
const logoPill = (s, x, y, w) => {
  const h = w * 0.62;
  s.addShape(p.ShapeType.roundRect, { x, y, w, h, fill: { color: C.white }, line: { type: 'none' }, rectRadius: 0.14, shadow: { type: 'outer', color: '000000', opacity: 0.25, blur: 12, offset: 4, angle: 90 } });
  s.addImage({ path: IMG('logo_mark.png'), x: x + w * 0.11, y: y + h * 0.1, w: w * 0.78, h: w * 0.78 * (760 / 1090) });
};
const pageNo = (s, n, dark) => T(s, String(n).padStart(2, '0'), { x: W - 1.1, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 11, bold: true, align: 'right', color: dark ? C.navy : C.white, transparency: 30 });
const dark = (s) => { s.background = { color: C.navyD }; };

// ---------- 1. Couverture
{
  const s = p.addSlide(); photo(s, 'pac-installation.jpg', 'ov_left.png');
  ring(s, 8.6, -3.2, 7.4, C.lime, 34, 55);
  logoPill(s, 0.75, 0.6, 2.5);
  kicker(s, 'Mandataire CEE · Partenaire des professionnels', 0.75, 2.75);
  T(s, [{ text: 'Vous réalisez les travaux.', options: { breakLine: true } }, { text: 'Nous gérons vos aides CEE.', options: { color: C.lime } }],
    { x: 0.75, y: 3.2, w: 11.8, h: 2.5, fontSize: 46, bold: true, lineSpacingMultiple: 0.95 });
  T(s, 'L’accompagnement CEE des artisans, installateurs et entreprises du bâtiment.', { x: 0.75, y: 5.95, w: 7.4, h: 0.8, fontSize: 18, color: C.pale });
}

// ---------- 2. Le problème
{
  const s = p.addSlide(); photo(s, 'paperasse.jpg', 'ov_right.png');
  kicker(s, 'Le constat', 6.6, 1.5);
  T(s, [{ text: 'Les CEE font gagner des chantiers.', options: { breakLine: true } }, { text: 'La paperasse vous les fait payer.', options: { color: C.lime } }],
    { x: 6.6, y: 1.95, w: 6.1, h: 3.1, fontSize: 38, bold: true, lineSpacingMultiple: 0.98 });
  T(s, 'Éligibilité, pièces à réunir, exigences du dispositif, suivi : autant de temps que vous ne passez ni sur vos chantiers, ni avec vos clients.',
    { x: 6.6, y: 5.2, w: 5.9, h: 1.3, fontSize: 16, color: C.pale, lineSpacingMultiple: 1.2 });
  pageNo(s, 2);
}

// ---------- 3. La réponse
{
  const s = p.addSlide(); dark(s);
  ring(s, -2.6, 3.6, 7.2, C.teal, 30, 70); ring(s, 9.4, -3.4, 7.6, C.lime, 34, 72);
  kicker(s, 'Notre réponse', 0.9, 0.95);
  T(s, [{ text: 'Un seul interlocuteur', options: { breakLine: true } }, { text: 'pour tous vos dossiers CEE.', options: { color: C.lime } }],
    { x: 0.9, y: 1.4, w: 11.5, h: 2.1, fontSize: 46, bold: true, lineSpacingMultiple: 0.98 });
  T(s, 'Cercle Énergie est une société spécialisée dans l’accompagnement et la valorisation des Certificats d’Économies d’Énergie. En tant que mandataire, nous travaillons avec des délégataires CEE pour financer vos projets — et nous simplifions toutes vos démarches.',
    { x: 0.9, y: 3.75, w: 8.2, h: 1.6, fontSize: 17, color: C.pale, lineSpacingMultiple: 1.25 });
  ['Simplifier', 'Sécuriser', 'Valoriser'].forEach((w, i) => {
    const x = 0.9 + i * 3.05;
    s.addShape(p.ShapeType.roundRect, { x, y: 5.75, w: 2.8, h: 0.85, fill: { color: C.green }, line: { type: 'none' }, rectRadius: 0.42 });
    T(s, w, { x, y: 5.75, w: 2.8, h: 0.85, fontSize: 22, bold: true, align: 'center', valign: 'middle' });
  });
  pageNo(s, 3);
}

// ---------- 4. La chaîne
{
  const s = p.addSlide(); s.background = { color: C.white };
  kicker(s, 'Notre rôle', 0.9, 0.7, C.greenD);
  T(s, 'Le lien entre vos chantiers et le financement.', { x: 0.9, y: 1.1, w: 11.8, h: 0.9, fontSize: 31, bold: true, color: C.navy });
  const cy = 4.15, d = 2.5;
  const nodes = [
    { x: 1.3, fill: C.navy, t: 'Installateurs\n& artisans', sub: 'Vous réalisez les travaux' },
    { x: 5.17, fill: C.white, t: '', sub: 'Votre mandataire CEE', core: true },
    { x: 9.53, fill: C.green, t: 'Délégataires\nCEE', sub: 'Les acteurs du financement' },
  ];
  // liaisons
  [[3.8, 5.17], [8.17, 9.53]].forEach(([a, b]) => {
    s.addShape(p.ShapeType.leftRightArrow, { x: a + 0.12, y: cy - 0.28, w: b - a - 0.24, h: 0.56, fill: { color: C.teal }, line: { type: 'none' } });
  });
  nodes.forEach((n) => {
    const dd = n.core ? 3.0 : d, y = cy - dd / 2;
    if (n.core) {
      s.addShape(p.ShapeType.ellipse, { x: n.x - 0.12, y: y - 0.12, w: dd + 0.24, h: dd + 0.24, fill: { color: C.green }, line: { type: 'none' } });
      s.addShape(p.ShapeType.ellipse, { x: n.x, y, w: dd, h: dd, fill: { color: C.white }, line: { type: 'none' } });
      s.addImage({ path: IMG('logo_mark.png'), x: n.x + 0.45, y: y + 0.78, w: 2.1, h: 2.1 * (760 / 1090) });
    } else {
      s.addShape(p.ShapeType.ellipse, { x: n.x, y, w: dd, h: dd, fill: { color: n.fill }, line: { type: 'none' } });
      T(s, n.t, { x: n.x, y, w: dd, h: dd, fontSize: 21, bold: true, align: 'center', valign: 'middle' });
    }
    T(s, n.sub, { x: n.x - 0.6, y: cy + dd / 2 + 0.25, w: dd + 1.2, h: 0.4, fontSize: 16, bold: true, align: 'center', color: C.navy });
  });
  T(s, 'Nous mettons en relation les entreprises d’installation et les acteurs du financement des CEE.', { x: 0.9, y: 6.55, w: 11.5, h: 0.4, fontSize: 14, color: C.grey, align: 'center' });
  pageNo(s, 4, true);
}

// ---------- 5. Secteurs (mosaïque pleine page)
{
  const s = p.addSlide(); dark(s);
  const tiles = [['pompe-a-chaleur.jpg', 'Pompes à chaleur'], ['chauffage.jpg', 'Chauffage'], ['isolation-combles.jpg', 'Isolation'], ['renovation.jpg', 'Rénovation énergétique'], ['tertiaire.jpg', 'Tertiaire'], ['industrie.jpg', 'Industrie'], ['agricole.jpg', 'Agricole']];
  const tw = W / 4, th = H / 2, g = 0.04;
  // tuile titre en haut à gauche
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: tw, h: th, fill: { color: C.green }, line: { type: 'none' } });
  T(s, 'NOS TERRAINS', { x: 0.4, y: 0.5, w: tw - 0.6, h: 0.3, fontSize: 11, bold: true, charSpacing: 4 });
  T(s, 'Partout où il y a de l’énergie à économiser.', { x: 0.4, y: 0.95, w: tw - 0.6, h: 2.4, fontSize: 24, bold: true, lineSpacingMultiple: 1.0 });
  tiles.forEach(([img, label], i) => {
    const k = i + 1, x = (k % 4) * tw, y = Math.floor(k / 4) * th;
    s.addImage({ path: IMG(img), x: x + g, y: y + g, w: tw - 2 * g, h: th - 2 * g, sizing: { type: 'cover', w: tw - 2 * g, h: th - 2 * g } });
    s.addShape(p.ShapeType.rect, { x: x + g, y: y + th - 0.95, w: tw - 2 * g, h: 0.95 - g, fill: { color: C.navyD, transparency: 22 }, line: { type: 'none' } });
    T(s, label, { x: x + 0.3, y: y + th - 0.95, w: tw - 0.5, h: 0.9, fontSize: 17, bold: true, valign: 'middle' });
  });
}

// ---------- 6. Cinq services
{
  const s = p.addSlide(); s.background = { color: C.mist };
  kicker(s, 'Nos services', 0.9, 0.7, C.greenD);
  T(s, 'Cinq étapes. Zéro paperasse pour vous.', { x: 0.9, y: 1.1, w: 11.5, h: 0.9, fontSize: 36, bold: true, color: C.navy });
  const steps = [['Étude d’éligibilité', 'Identification des aides CEE mobilisables selon vos travaux.'], ['Valorisation financière', 'Recherche des meilleures conditions auprès de nos partenaires.'], ['Gestion administrative', 'Constitution, vérification et suivi des dossiers.'], ['Accompagnement réglementaire', 'Vérification des exigences documentaires et des conditions du dispositif.'], ['Suivi du financement', 'Coordination avec les délégataires jusqu’au versement des primes*.']];
  const cw = 2.2, gap = 0.14, x0 = 0.9;
  steps.forEach(([t, d], i) => {
    const x = x0 + i * (cw + gap), last = i === 4;
    s.addShape(p.ShapeType.roundRect, { x, y: 2.4, w: cw, h: 3.85, fill: { color: last ? C.navy : C.white }, line: { type: 'none' }, rectRadius: 0.16, shadow: { type: 'outer', color: '0B3566', opacity: 0.14, blur: 14, offset: 5, angle: 90 } });
    T(s, '0' + (i + 1), { x: x + 0.25, y: 2.6, w: cw - 0.4, h: 1.0, fontSize: 50, bold: true, color: last ? C.lime : C.green });
    T(s, t, { x: x + 0.25, y: 3.75, w: cw - 0.4, h: 0.85, fontSize: 12.5, bold: true, color: last ? C.white : C.navy, lineSpacingMultiple: 1.0 });
    T(s, d, { x: x + 0.25, y: 4.65, w: cw - 0.45, h: 1.5, fontSize: 12, color: last ? C.pale : C.grey, lineSpacingMultiple: 1.2 });
  });
  T(s, '* Sous réserve de validation du dossier.', { x: 0.9, y: 6.6, w: 8, h: 0.3, fontSize: 11, color: C.grey });
  pageNo(s, 6, true);
}

// ---------- 7. Qui fait quoi
{
  const s = p.addSlide(); dark(s);
  ring(s, 9.8, 3.9, 6.4, C.teal, 26, 75);
  kicker(s, 'Répartition des rôles', 0.9, 0.7);
  T(s, [{ text: 'Vous, sur le chantier. ' }, { text: 'Nous, sur le dossier.', options: { color: C.lime } }], { x: 0.9, y: 1.1, w: 11.6, h: 0.9, fontSize: 34, bold: true });
  const cols = [
    { t: 'Vous', k: 'Installateurs & artisans', li: ['Vous présentez les travaux envisagés', 'Vous réalisez les travaux', 'Vous restez concentré sur vos clients'], fill: '123F78', tc: C.white },
    { t: 'Cercle Énergie', k: 'Mandataire CEE', li: ['Étudie l’éligibilité', 'Recherche la meilleure valorisation', 'Constitue et vérifie le dossier', 'Coordonne et suit le financement'], fill: C.green, tc: C.white, big: true },
    { t: 'Délégataire CEE', k: 'Acteur du financement', li: ['Traite le dossier', 'Verse les primes, sous réserve de validation du dossier'], fill: '123F78', tc: C.white },
  ];
  const xs = [0.9, 4.55, 8.95], ws = [3.45, 4.2, 3.45];
  cols.forEach((c, i) => {
    const y = c.big ? 2.25 : 2.55, h = c.big ? 4.55 : 3.95;
    s.addShape(p.ShapeType.roundRect, { x: xs[i], y, w: ws[i], h, fill: { color: c.fill }, line: { type: 'none' }, rectRadius: 0.18 });
    T(s, c.t, { x: xs[i] + 0.35, y: y + 0.35, w: ws[i] - 0.6, h: 0.5, fontSize: c.big ? 26 : 22, bold: true });
    T(s, c.k.toUpperCase(), { x: xs[i] + 0.35, y: y + 0.95, w: ws[i] - 0.6, h: 0.3, fontSize: 10, bold: true, charSpacing: 3, color: c.big ? C.navyD : C.lime });
    T(s, c.li.map((l) => ({ text: l, options: { bullet: { code: '2713' }, breakLine: true, paraSpaceAfter: 9 } })), { x: xs[i] + 0.35, y: y + 1.5, w: ws[i] - 0.6, h: h - 1.7, fontSize: c.big ? 15 : 14, color: C.white, lineSpacingMultiple: 1.1 });
  });
  pageNo(s, 7);
}

// ---------- 8. Trois bénéfices (colonnes photo)
{
  const s = p.addSlide(); dark(s);
  const cols = [['dossier.jpg', 'Simplifier', 'Un interlocuteur unique pour toutes vos démarches CEE.'], ['remise-dossier.jpg', 'Sécuriser', 'Des dossiers vérifiés au regard des exigences du dispositif.'], ['artisan-clients.jpg', 'Valoriser', 'Les meilleures conditions recherchées auprès de nos partenaires.']];
  const cw = W / 3;
  cols.forEach(([img, t, d], i) => {
    const x = i * cw;
    s.addImage({ path: IMG(img), x, y: 0, w: cw, h: H, sizing: { type: 'cover', w: cw, h: H } });
    s.addShape(p.ShapeType.rect, { x, y: 0, w: cw, h: H, fill: { color: C.navyD, transparency: 68 }, line: { type: 'none' } });
    s.addShape(p.ShapeType.rect, { x, y: 4.0, w: cw, h: 3.5, fill: { color: C.navyD, transparency: 10 }, line: { type: 'none' } });
    T(s, '0' + (i + 1), { x: x + 0.5, y: 0.55, w: 2, h: 0.8, fontSize: 40, bold: true, color: C.lime });
    T(s, t, { x: x + 0.5, y: 4.35, w: cw - 0.8, h: 0.9, fontSize: 38, bold: true });
    s.addShape(p.ShapeType.roundRect, { x: x + 0.5, y: 5.35, w: 0.8, h: 0.08, fill: { color: C.green }, line: { type: 'none' }, rectRadius: 0.04 });
    T(s, d, { x: x + 0.5, y: 5.6, w: cw - 0.9, h: 1.3, fontSize: 15, color: C.pale, lineSpacingMultiple: 1.2 });
  });
}

// ---------- 9. Avant / après
{
  const s = p.addSlide(); s.background = { color: C.white };
  s.addShape(p.ShapeType.rect, { x: W / 2, y: 0, w: W / 2, h: H, fill: { color: C.navy }, line: { type: 'none' } });
  T(s, 'SANS ACCOMPAGNEMENT', { x: 0.9, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: '8A9BB3' });
  T(s, 'Vous gérez tout.', { x: 0.9, y: 1.2, w: 5.4, h: 0.9, fontSize: 29, bold: true, color: C.navy });
  T(s, 'AVEC CERCLE ÉNERGIE', { x: W / 2 + 0.8, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: C.lime });
  T(s, 'Vous gérez vos chantiers.', { x: W / 2 + 0.8, y: 1.2, w: 5.8, h: 0.9, fontSize: 29, bold: true, color: C.white });
  const rows = [['Aides à identifier vous-même, chantier par chantier', 'Aides identifiées selon vos travaux'], ['Dossiers à constituer, vérifier et suivre en interne', 'Dossiers constitués, vérifiés et suivis'], ['Exigences du dispositif à maîtriser seul', 'Exigences documentaires contrôlées'], ['Acteurs du financement à trouver et à coordonner', 'Un partenaire unique, en lien avec les délégataires']];
  rows.forEach(([a, b], i) => {
    const y = 2.65 + i * 1.08;
    s.addShape(p.ShapeType.ellipse, { x: 0.9, y: y + 0.05, w: 0.42, h: 0.42, fill: { color: 'D6DEE8' }, line: { type: 'none' } });
    T(s, '×', { x: 0.9, y: y + 0.05, w: 0.42, h: 0.42, fontSize: 16, bold: true, align: 'center', valign: 'middle', color: C.white });
    T(s, a, { x: 1.55, y, w: 4.6, h: 0.8, fontSize: 16, color: C.grey, valign: 'middle' });
    s.addShape(p.ShapeType.ellipse, { x: W / 2 + 0.8, y: y + 0.05, w: 0.42, h: 0.42, fill: { color: C.green }, line: { type: 'none' } });
    T(s, '✓', { x: W / 2 + 0.8, y: y + 0.05, w: 0.42, h: 0.42, fontSize: 14, bold: true, align: 'center', valign: 'middle' });
    T(s, b, { x: W / 2 + 1.45, y, w: 4.7, h: 0.8, fontSize: 17, bold: true, valign: 'middle' });
  });
  s.addShape(p.ShapeType.ellipse, { x: W / 2 - 0.55, y: 3.2, w: 1.1, h: 1.1, fill: { color: C.green }, line: { color: C.white, width: 5 } });
  T(s, '→', { x: W / 2 - 0.55, y: 3.2, w: 1.1, h: 1.1, fontSize: 28, bold: true, align: 'center', valign: 'middle' });
  pageNo(s, 9);
}

// ---------- 10. Démarrer
{
  const s = p.addSlide(); photo(s, 'equipe.jpg', 'ov_left.png');
  kicker(s, 'Démarrer', 0.9, 0.75);
  T(s, [{ text: 'Un échange,', options: { breakLine: true } }, { text: 'et nous prenons le relais.', options: { color: C.lime } }], { x: 0.9, y: 1.15, w: 8, h: 1.7, fontSize: 38, bold: true, lineSpacingMultiple: 0.98 });
  const st = [['Vous prenez contact', 'Présentez-nous votre activité et vos travaux.'], ['Nous étudions l’éligibilité', 'Nous identifions les aides CEE mobilisables.'], ['Nous constituons le dossier', 'Constitution, vérification, suivi.'], ['Nous suivons le financement', 'Jusqu’au versement des primes, sous réserve de validation du dossier.']];
  st.forEach(([t, d], i) => {
    const y = 3.2 + i * 0.98;
    s.addShape(p.ShapeType.ellipse, { x: 0.9, y, w: 0.72, h: 0.72, fill: { color: C.green }, line: { type: 'none' } });
    T(s, String(i + 1), { x: 0.9, y, w: 0.72, h: 0.72, fontSize: 20, bold: true, align: 'center', valign: 'middle' });
    T(s, t, { x: 1.85, y: y - 0.02, w: 6, h: 0.38, fontSize: 18, bold: true });
    T(s, d, { x: 1.85, y: y + 0.38, w: 6, h: 0.4, fontSize: 13, color: C.pale });
  });
  pageNo(s, 10);
}

// ---------- 11. Message clé
{
  const s = p.addSlide(); photo(s, 'artisan-clients.jpg', 'ov_bottom.png');
  ring(s, -2.2, -2.6, 5.6, C.lime, 28, 55);
  T(s, [{ text: '« Vous réalisez les travaux, ', options: {} }, { text: 'Cercle Énergie vous accompagne dans la gestion et le financement de vos aides CEE. »', options: { color: C.lime } }],
    { x: 0.9, y: 3.9, w: 11.5, h: 2.6, fontSize: 36, bold: true, lineSpacingMultiple: 1.0, valign: 'bottom' });
  pageNo(s, 11);
}

// ---------- 12. Appel à l'action
{
  const s = p.addSlide(); s.background = { color: C.green };
  ring(s, 8.2, -2.8, 8.4, C.white, 40, 78); ring(s, -3.0, 3.6, 7.0, C.navy, 34, 80);
  logoPill(s, 0.9, 0.7, 2.6);
  T(s, 'Devenez partenaire.', { x: 0.9, y: 2.75, w: 11.5, h: 1.3, fontSize: 66, bold: true });
  T(s, 'Cercle Énergie : votre partenaire pour simplifier, sécuriser et valoriser vos projets d’économies d’énergie.', { x: 0.9, y: 4.25, w: 9.2, h: 1.1, fontSize: 19, lineSpacingMultiple: 1.2 });
  ['[Téléphone]', '[E-mail]', '[Site web]'].forEach((c, i) => {
    const x = 0.9 + i * 3.25;
    s.addShape(p.ShapeType.roundRect, { x, y: 5.8, w: 3.0, h: 0.8, fill: { color: C.navy }, line: { type: 'none' }, rectRadius: 0.4 });
    T(s, c, { x, y: 5.8, w: 3.0, h: 0.8, fontSize: 16, bold: true, align: 'center', valign: 'middle' });
  });
}

p.writeFile({ fileName: path.join(__dirname, 'Cercle-Energie-Plaquette.pptx') }).then((f) => console.log('écrit', f));
