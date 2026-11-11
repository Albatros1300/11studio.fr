// Plaquette Cercle Énergie — version « agence »
// Usage : NODE_PATH=<node_modules avec pptxgenjs, sharp, react, react-dom, react-icons> node build_plaquette.js
//
// RÈGLE IMAGES : jamais de `sizing` pptxgenjs (PowerPoint l'affiche étiré).
// Chaque image est pré-recadrée par sharp au ratio exact de sa boîte (crops/),
// puis insérée avec x/y/w/h simples. Les dimensions du logo viennent des pixels réels.
const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const fa = require('react-icons/fa');

const PHOTO = (n) => path.join(__dirname, '..', 'photos', n + '.jpg');
const LOGO_SRC = (n) => path.join(__dirname, '..', 'site', 'assets', 'img', n);
const LOGO = (n) => path.join(__dirname, 'assets', n); // copie détourée, mêmes pixels (voir logoDims) — à poser sur formes blanches uniquement
const ASSETS = path.join(__dirname, 'assets');
const CROPS = path.join(ASSETS, 'crops');
const ICONS = path.join(ASSETS, 'icons');
[ASSETS, CROPS, ICONS].forEach((d) => fs.mkdirSync(d, { recursive: true }));

const C = { navy: '0B3566', navyD: '07264B', navyL: '123F78', lime: 'B9E35A', green: '73AF01', greenD: '4E8A06', teal: '01B7BA', white: 'FFFFFF', mist: 'F1F6FB', grey: '40577A', pale: 'CFE0F3', tint: 'EAF4D3' };
const F = 'Montserrat';
const W = 13.333, H = 7.5, M = 0.75, CW = W - 2 * M;
const DPI = 192;
const NB = ' '; // espace insécable

const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.title = 'Cercle Énergie — Plaquette de présentation';
p.company = 'Cercle Énergie';
p.author = 'Cercle Énergie';
p.theme = { headFontFace: F, bodyFontFace: F };

// ---------------------------------------------------------------- images
// Recadre `name` au ratio exact w/h (pouces) autour du point focal (fx, fy ∈ 0..1),
// zoom optionnel z ≥ 1, coins arrondis optionnels r = [hg, hd, bd, bg] en pouces (→ PNG).
async function crop(name, w, h, o = {}) {
  const { fx = 0.5, fy = 0.5, z = 1, r = null } = o;
  const src = PHOTO(name);
  const meta = await sharp(src).metadata();
  const ar = w / h;
  let cw = meta.width, ch = cw / ar;
  if (ch > meta.height) { ch = meta.height; cw = ch * ar; }
  cw = Math.round(cw / z); ch = Math.round(ch / z);
  const left = Math.max(0, Math.min(meta.width - cw, Math.round(fx * meta.width - cw / 2)));
  const top = Math.max(0, Math.min(meta.height - ch, Math.round(fy * meta.height - ch / 2)));
  const ow = Math.min(cw, Math.round(w * DPI)), oh = Math.round(ow / ar);
  const tag = `${name}_${ow}x${oh}_${Math.round(fx * 100)}_${Math.round(fy * 100)}_${Math.round(z * 100)}`;
  let img = sharp(src).extract({ left, top, width: cw, height: ch }).resize(ow, oh, { fit: 'cover' }).withMetadata({ density: DPI });
  if (!r) {
    const out = path.join(CROPS, tag + '.jpg');
    await img.jpeg({ quality: 88 }).toFile(out);
    return out;
  }
  const [a, b, c, d] = r.map((v) => Math.round(v * ow / w));
  const mask = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${ow}" height="${oh}"><path d="M${a},0 H${ow - b} A${b},${b} 0 0 1 ${ow},${b} V${oh - c} A${c},${c} 0 0 1 ${ow - c},${oh} H${d} A${d},${d} 0 0 1 0,${oh - d} V${a} A${a},${a} 0 0 1 ${a},0 Z" fill="#fff"/></svg>`);
  const out = path.join(CROPS, tag + '_r.png');
  await img.composite([{ input: mask, blend: 'dest-in' }]).png({ compressionLevel: 9 }).toFile(out);
  return out;
}
const pic = async (s, name, x, y, w, h, o) => s.addImage({ path: await crop(name, w, h, o), x, y, w, h });

// Dégradés marine (PNG) : insérés à la taille exacte de leur boîte.
async function overlay(name, x1, y1, x2, y2, stops) {
  const out = path.join(ASSETS, name + '.png');
  const st = stops.map(([o, a]) => `<stop offset="${o}" stop-color="#07264B" stop-opacity="${a}"/>`).join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900"><defs><linearGradient id="g" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}">${st}</linearGradient></defs><rect width="1600" height="900" fill="url(#g)"/></svg>`;
  await sharp(Buffer.from(svg)).png().toFile(out);
  return out;
}
async function icon(name, color) {
  const out = path.join(ICONS, `${name}_${color}.png`);
  const svg = renderToStaticMarkup(React.createElement(fa[name], { color: '#' + color, size: 256 }));
  await sharp(Buffer.from(svg)).resize(256, 256, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toFile(out);
  return out;
}
const ico = async (s, name, color, x, y, d) => s.addImage({ path: await icon(name, color), x, y, w: d, h: d });

// ---------------------------------------------------------------- helpers
const T = (s, text, o) => s.addText(text, Object.assign({ fontFace: F, color: C.white, margin: 0, valign: 'top', fit: 'none', isTextBox: true }, o));
const rect = (s, x, y, w, h, fill, extra) => s.addShape(p.ShapeType.rect, Object.assign({ x, y, w, h, fill: { color: fill }, line: { type: 'none' } }, extra || {}));
const rrect = (s, x, y, w, h, fill, r, extra) => s.addShape(p.ShapeType.roundRect, Object.assign({ x, y, w, h, fill: { color: fill }, line: { type: 'none' }, rectRadius: r == null ? 0.16 : r }, extra || {}));
const disc = (s, x, y, d, fill, extra) => s.addShape(p.ShapeType.ellipse, Object.assign({ x, y, w: d, h: d, fill: { color: fill }, line: { type: 'none' } }, extra || {}));
const ring = (s, x, y, d, color, pt, transp) => s.addShape(p.ShapeType.ellipse, { x, y, w: d, h: d, fill: { type: 'none' }, line: { color, width: pt, transparency: transp == null ? 0 : transp } });
const softShadow = () => ({ type: 'outer', color: '0B3566', opacity: 0.14, blur: 14, offset: 5, angle: 90 });
const kicker = (s, text, x, y, color) => {
  disc(s, x, y + 0.04, 0.2, C.green);
  T(s, text.toUpperCase(), { x: x + 0.36, y, w: 9, h: 0.28, fontSize: 12, bold: true, charSpacing: 4, color: color || C.lime });
};
const title = (s, runs, color, o) => T(s, runs, Object.assign({ x: M, y: 1.02, w: CW, h: 0.7, fontSize: 34, bold: true, color: color || C.white, lineSpacingMultiple: 0.98 }, o || {}));
const pageNo = (s, n) => {
  rrect(s, W - M - 0.6, H - 0.55, 0.6, 0.3, C.navyD, 0.15);
  T(s, String(n).padStart(2, '0'), { x: W - M - 0.6, y: H - 0.55, w: 0.6, h: 0.3, fontSize: 10, bold: true, align: 'center', valign: 'middle' });
};
let LOGOS = {};
async function logoDims() {
  for (const n of ['logo_mark.png', 'logo_full.png']) {
    // Le fond des fichiers source vaut 254 et non 255 : on le pousse au blanc pur, sans toucher aux proportions.
    // et on le rend transparent (« dé-prémultiplication » sur blanc) : rendu identique sur une forme blanche,
    // sans rectangle fantôme à l'export PDF.
    const { data, info } = await sharp(LOGO_SRC(n)).flatten({ background: '#ffffff' }).linear(1.03, 0).removeAlpha().raw().toBuffer({ resolveWithObject: true });
    const out = Buffer.alloc(info.width * info.height * 4);
    for (let i = 0, j = 0; i < data.length; i += 3, j += 4) {
      const a = 1 - Math.min(data[i], data[i + 1], data[i + 2]) / 255;
      for (let k = 0; k < 3; k++) out[j + k] = a > 0 ? Math.max(0, Math.min(255, Math.round((data[i + k] - (1 - a) * 255) / a))) : 255;
      out[j + 3] = Math.round(a * 255);
    }
    await sharp(out, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toFile(LOGO(n));
    LOGOS[n] = info.height / info.width;
  }
}
// Logo sur pastille blanche : hauteur calculée depuis les pixels réels du fichier.
const logoPill = (s, x, y, w, file) => {
  const padX = w * 0.09, lw = w - 2 * padX, lh = lw * LOGOS[file], padY = w * 0.07, h = lh + 2 * padY;
  rrect(s, x, y, w, h, C.white, 0.16, { shadow: { type: 'outer', color: '000000', opacity: 0.25, blur: 12, offset: 4, angle: 90 } });
  s.addImage({ path: LOGO(file), x: x + padX, y: y + padY, w: lw, h: lh });
  return h;
};
const logoAt = (s, cx, cy, w) => { const h = w * LOGOS['logo_mark.png']; s.addImage({ path: LOGO('logo_mark.png'), x: cx - w / 2, y: cy - h / 2, w, h }); };
const nLines = (text, pt, w, bold) => text.split('\n').reduce((n, l) => n + Math.max(1, Math.ceil((l.length * (bold ? 0.58 : 0.48) * pt / 72) / w)), 0);
let SEC = '';
const slide = () => p.addSlide({ sectionTitle: SEC });
const section = (t) => { SEC = t; p.addSection({ title: t }); };

// Slide secteur : photo plein cadre + dégradé latéral, mot géant, professionnels concernés.
async function sector(n, idx, side, photo, focal, word, line, items, OV) {
  const s = slide();
  await pic(s, photo, 0, 0, W, H, focal);
  s.addImage({ path: side === 'L' ? OV.left : OV.right, x: 0, y: 0, w: W, h: H });
  const x = side === 'L' ? M : 7.2, w = 5.4;
  if (side === 'L') ring(s, 9.9, -3.3, 6.6, C.lime, 26, 60);
  kicker(s, `Secteur ${idx}/4`, x, 1.75);
  T(s, word, { x, y: 2.15, w: w + 0.6, h: 1.0, fontSize: 60, bold: true });
  T(s, line, { x, y: 3.3, w: w, h: 0.7, fontSize: 17, color: C.pale, lineSpacingMultiple: 1.15 });
  T(s, 'PROFESSIONNELS CONCERNÉS', { x, y: 4.3, w, h: 0.25, fontSize: 10.5, bold: true, charSpacing: 3, color: C.lime });
  let y = 4.72;
  items.forEach((it) => {
    const h = nLines(it, 15, w - 0.36, true) * 0.27 + 0.06;
    disc(s, x, y + 0.07, 0.14, C.lime);
    T(s, it, { x: x + 0.36, y, w: w - 0.36, h, fontSize: 15, bold: true, lineSpacingMultiple: 1.1 });
    y += h + 0.18;
  });
  pageNo(s, n);
}

(async () => {
  await logoDims();
  const OV = {
    left: await overlay('ov_left', 0, 0, 1, 0, [[0, 0.97], [0.30, 0.94], [0.47, 0.74], [0.68, 0]]),
    right: await overlay('ov_right', 1, 0, 0, 0, [[0, 0.97], [0.30, 0.94], [0.47, 0.74], [0.68, 0]]),
    bottom: await overlay('ov_bottom', 0, 0, 0, 1, [[0, 0], [0.40, 0], [0.60, 0.84], [1, 0.97]]),
  };

  // ================================================================ OUVERTURE
  section('Ouverture');

  // ---------- 1. Couverture
  {
    const s = slide();
    await pic(s, 'pac-installation', 0, 0, W, H, { z: 1.15, fx: 0.465, fy: 0.55 });
    s.addImage({ path: OV.left, x: 0, y: 0, w: W, h: H });
    ring(s, 9.9, -5.0, 7.4, C.lime, 34, 55);
    logoPill(s, M, 0.5, 2.1, 'logo_full.png');
    kicker(s, 'Mandataire CEE · Partenaire des professionnels', M, 2.3);
    T(s, [{ text: 'Vous réalisez', options: { breakLine: true } }, { text: 'les travaux.', options: { breakLine: true } }, { text: 'Nous gérons', options: { color: C.lime, breakLine: true } }, { text: 'vos aides CEE.', options: { color: C.lime } }],
      { x: M, y: 2.68, w: 6.6, h: 2.95, fontSize: 50, bold: true, lineSpacingMultiple: 0.95 });
    T(s, 'Le partenaire unique de vos projets', { x: M, y: 5.98, w: 6.4, h: 0.35, fontSize: 18, bold: true });
    T(s, 'L’accompagnement CEE des installateurs et des entreprises de la rénovation énergétique.', { x: M, y: 6.4, w: 5.6, h: 0.6, fontSize: 14, color: C.pale, lineSpacingMultiple: 1.15 });
  }

  // ---------- 2. Le constat
  {
    const s = slide();
    await pic(s, 'paperasse', 0, 0, W, H, { fx: 0.5, fy: 0.5 });
    s.addImage({ path: OV.right, x: 0, y: 0, w: W, h: H });
    const x = 7.15;
    kicker(s, 'Le constat', x, 1.55);
    T(s, [{ text: 'Les CEE font gagner', options: { breakLine: true } }, { text: 'des chantiers.', options: { breakLine: true } }, { text: 'La paperasse vous', options: { color: C.lime, breakLine: true } }, { text: 'les fait payer.', options: { color: C.lime } }],
      { x, y: 1.98, w: 5.6, h: 2.0, fontSize: 32, bold: true, lineSpacingMultiple: 0.98 });
    T(s, `Éligibilité, pièces à réunir, exigences du dispositif, suivi${NB}: autant de temps que vous ne passez ni sur vos chantiers, ni avec vos clients.`,
      { x, y: 4.3, w: 5.2, h: 1.5, fontSize: 16, color: C.pale, lineSpacingMultiple: 1.25 });
    pageNo(s, 2);
  }

  // ---------- 3. La réponse
  {
    const s = slide(); s.background = { color: C.navyD };
    ring(s, -3.6, 5.2, 7.2, C.teal, 30, 70); ring(s, 9.4, -3.4, 7.6, C.lime, 34, 72);
    kicker(s, 'Notre réponse', M, 0.95);
    T(s, [{ text: 'Un seul interlocuteur', options: { breakLine: true } }, { text: 'pour tous vos dossiers CEE.', options: { color: C.lime } }],
      { x: M, y: 1.4, w: CW, h: 1.5, fontSize: 44, bold: true, lineSpacingMultiple: 0.98 });
    T(s, 'Cercle Énergie est une société spécialisée dans l’accompagnement et la valorisation des Certificats d’Économies d’Énergie (CEE). En tant que mandataire, nous travaillons avec des délégataires CEE pour vous aider à financer vos projets de rénovation et d’efficacité énergétique, et nous simplifions vos démarches administratives.',
      { x: M, y: 3.25, w: 8.7, h: 1.9, fontSize: 17, color: C.pale, lineSpacingMultiple: 1.25 });
    ['Simplifier', 'Sécuriser', 'Valoriser'].forEach((w, i) => {
      const x = M + i * 3.05;
      rrect(s, x, 5.7, 2.8, 0.85, i === 1 ? C.lime : C.green, 0.42);
      T(s, w, { x, y: 5.7, w: 2.8, h: 0.85, fontSize: 22, bold: true, align: 'center', valign: 'middle', color: i === 1 ? C.navyD : C.white });
    });
    pageNo(s, 3);
  }

  // ================================================================ COMPRENDRE
  section('Comprendre');

  // ---------- 4. Les CEE en 30 secondes
  {
    const s = slide(); s.background = { color: C.mist };
    kicker(s, 'Comprendre', M, 0.65, C.greenD);
    title(s, 'Les CEE en 30 secondes', C.navy);
    const nodes = [
      ['FaBolt', `Les «${NB}obligés${NB}»`, 'Les fournisseurs d’énergie doivent promouvoir les économies d’énergie.'],
      ['FaLandmark', 'Les délégataires', 'Ils peuvent porter cette obligation à la place des obligés.'],
      [null, 'Le mandataire', 'Cercle Énergie fait le lien entre délégataires et installateurs.'],
      ['FaTools', 'L’installateur', 'Vous réalisez les travaux d’économies d’énergie.'],
      ['FaHome', 'Le client final', `Il bénéficie de la prime${NB}CEE*.`],
    ];
    const colW = CW / 5, d = 1.6, cy = 3.1;
    for (let i = 0; i < 5; i++) {
      const [ic, t, desc] = nodes[i];
      const cx = M + colW * (i + 0.5);
      if (ic) {
        disc(s, cx - d / 2, cy - d / 2, d, C.navy, { shadow: softShadow() });
        await ico(s, ic, 'B9E35A', cx - 0.33, cy - 0.33, 0.66);
      } else {
        disc(s, cx - d / 2 - 0.1, cy - d / 2 - 0.1, d + 0.2, C.green);
        disc(s, cx - d / 2, cy - d / 2, d, C.white);
        logoAt(s, cx, cy, 1.28);
      }
      if (i < 4) await ico(s, 'FaArrowRight', '01B7BA', cx + colW / 2 - 0.16, cy - 0.16, 0.32);
      T(s, t, { x: cx - colW / 2, y: 4.2, w: colW, h: 0.35, fontSize: 16, bold: true, color: i === 2 ? C.greenD : C.navy, align: 'center' });
      T(s, desc, { x: cx - 1.06, y: 4.62, w: 2.12, h: 1.05, fontSize: 13, color: C.grey, align: 'center', lineSpacingMultiple: 1.15 });
    }
    rrect(s, M, 5.82, CW, 0.78, C.navy, 0.39);
    T(s, [{ text: `Le principe${NB}: `, options: { bold: true, color: C.lime } }, { text: 'les obligés financent des travaux d’économies d’énergie sous forme de primes.' }],
      { x: M + 0.4, y: 5.82, w: CW - 0.8, h: 0.78, fontSize: 15, valign: 'middle', align: 'center' });
    T(s, '* Sous réserve de validation du dossier.', { x: M, y: 6.86, w: 8, h: 0.26, fontSize: 10.5, color: C.grey });
    pageNo(s, 4);
  }

  // ---------- 5. La chaîne
  {
    const s = slide(); s.background = { color: C.navyD };
    ring(s, W / 2 - 1.65, 4.2 - 1.65, 3.3, C.teal, 2, 40);
    kicker(s, 'Notre rôle', M, 0.65);
    title(s, [{ text: 'Le lien entre vos chantiers', options: { breakLine: true } }, { text: 'et le financement.', options: { color: C.lime } }], C.white, { h: 1.15 });
    const cy = 4.2, cxs = [2.6, W / 2, W - 2.6], d = 2.3, dc = 2.8;
    [[cxs[0] + d / 2, cxs[1] - dc / 2], [cxs[1] + dc / 2, cxs[2] - d / 2]].forEach(([a, b]) => {
      s.addShape(p.ShapeType.leftRightArrow, { x: a + 0.22, y: cy - 0.26, w: b - a - 0.44, h: 0.52, fill: { color: C.teal }, line: { type: 'none' } });
    });
    disc(s, cxs[0] - d / 2, cy - d / 2, d, C.navyL);
    T(s, 'Entreprises\nd’installation', { x: cxs[0] - d / 2, y: cy - d / 2, w: d, h: d, fontSize: 17, bold: true, align: 'center', valign: 'middle' });
    disc(s, cxs[1] - dc / 2 - 0.13, cy - dc / 2 - 0.13, dc + 0.26, C.green);
    disc(s, cxs[1] - dc / 2, cy - dc / 2, dc, C.white);
    logoAt(s, cxs[1], cy, 2.15);
    disc(s, cxs[2] - d / 2, cy - d / 2, d, C.green);
    T(s, 'Délégataires\nCEE', { x: cxs[2] - d / 2, y: cy - d / 2, w: d, h: d, fontSize: 17, bold: true, align: 'center', valign: 'middle' });
    ['Vous réalisez les travaux', 'Votre mandataire CEE', 'Les acteurs du financement'].forEach((t, i) =>
      T(s, t, { x: cxs[i] - 1.9, y: 6.0, w: 3.8, h: 0.34, fontSize: 15, bold: true, align: 'center', color: i === 1 ? C.lime : C.white }));
    T(s, 'Nous mettons en relation les entreprises d’installation et les acteurs du financement des CEE.', { x: M, y: 6.58, w: CW, h: 0.32, fontSize: 14, color: C.pale, align: 'center' });
    pageNo(s, 5);
  }

  // ---------- 6. Qui fait quoi
  {
    const s = slide(); s.background = { color: C.white };
    kicker(s, 'Répartition des rôles', M, 0.65, C.greenD);
    title(s, [{ text: 'Vous, sur le chantier.', options: { breakLine: true } }, { text: 'Nous, sur le dossier.', options: { color: C.green } }], C.navy, { h: 1.15 });
    const cols = [
      { t: 'Vous', k: 'Votre entreprise', li: ['Vous présentez les travaux envisagés', 'Vous réalisez les travaux', 'Vous restez concentré sur vos clients'] },
      { t: 'Cercle Énergie', k: 'Mandataire CEE', li: ['Étudie l’éligibilité', 'Recherche les meilleures conditions de valorisation', 'Constitue et vérifie le dossier', 'Coordonne et suit le financement'], big: true },
      { t: 'Délégataire CEE', k: 'Acteur du financement', li: ['Traite le dossier', `Verse les primes, sous réserve de validation du${NB}dossier`] },
    ];
    const xs = [M, 4.4, 8.93], ws = [3.4, 4.28, 3.65];
    cols.forEach((c, i) => {
      const y = c.big ? 2.5 : 2.8, h = c.big ? 4.25 : 3.65, fg = c.big ? C.white : C.navy;
      rrect(s, xs[i], y, ws[i], h, c.big ? C.navyD : C.mist, 0.18, c.big ? { shadow: softShadow() } : {});
      T(s, c.t, { x: xs[i] + 0.35, y: y + 0.32, w: ws[i] - 0.6, h: 0.5, fontSize: c.big ? 26 : 22, bold: true, color: fg });
      T(s, c.k.toUpperCase(), { x: xs[i] + 0.35, y: y + 0.9, w: ws[i] - 0.6, h: 0.28, fontSize: 10, bold: true, charSpacing: 3, color: c.big ? C.lime : C.greenD });
      let yy = y + 1.45;
      c.li.forEach((l) => {
        const tw = ws[i] - 1.0, hh = nLines(l, 14, tw) * 0.25 + 0.05;
        disc(s, xs[i] + 0.35, yy + 0.06, 0.14, c.big ? C.lime : C.green);
        T(s, l, { x: xs[i] + 0.68, y: yy, w: tw, h: hh, fontSize: 14, color: fg, lineSpacingMultiple: 1.1 });
        yy += hh + 0.17;
      });
    });
    pageNo(s, 6);
  }

  // ================================================================ NOS SERVICES
  section('Nos services');
  const SV = [
    ['Étude d’éligibilité', 'Identification des aides CEE mobilisables selon les travaux envisagés.',
      'La description des travaux envisagés.', 'Nous identifions les aides CEE mobilisables selon ces travaux.', 'Une vision claire des aides CEE mobilisables pour votre projet.'],
    ['Valorisation financière', 'Recherche des meilleures conditions de valorisation auprès de nos partenaires.',
      'Les éléments de votre projet.', 'Nous recherchons les meilleures conditions de valorisation auprès de nos partenaires.', 'Une proposition de valorisation issue de cette recherche.'],
    ['Gestion administrative', 'Constitution, vérification et suivi des dossiers.',
      'Les pièces et informations nécessaires au dossier.', 'Nous constituons, vérifions et suivons vos dossiers.', 'Un dossier constitué, vérifié et suivi par nos soins.'],
    ['Accompagnement réglementaire', `Vérification des exigences documentaires et des conditions du${NB}dispositif.`,
      'Les documents liés à vos travaux.', 'Nous vérifions les exigences documentaires et les conditions du dispositif.', 'Un dossier vérifié au regard des exigences du dispositif.'],
    ['Suivi du financement', `Coordination avec les délégataires jusqu’au traitement du dossier et au versement des${NB}primes*.`,
      'Les compléments éventuellement demandés.', 'Nous coordonnons avec les délégataires jusqu’au traitement du dossier.', 'Un suivi jusqu’au versement des primes, sous réserve de validation du dossier.'],
  ];

  // ---------- 7. Cinq services
  {
    const s = slide(); s.background = { color: C.navyD };
    ring(s, 10.3, -4.4, 6.8, C.teal, 26, 75);
    kicker(s, 'Nos services', M, 0.65);
    title(s, [{ text: 'Cinq étapes. ' }, { text: 'Zéro paperasse pour vous.', options: { color: C.lime } }]);
    const gap = 0.14, cw = (CW - 4 * gap) / 5, y0 = 2.95, ch = 3.35;
    SV.forEach(([t, d], i) => {
      const x = M + i * (cw + gap), last = i === 4, fg = last ? C.navyD : C.white;
      rrect(s, x, y0, cw, ch, last ? C.lime : C.navyL);
      disc(s, x + 0.18, y0 - 0.43, 0.86, last ? C.navyD : C.green);
      T(s, '0' + (i + 1), { x: x + 0.18, y: y0 - 0.43, w: 0.86, h: 0.86, fontSize: 20, bold: true, align: 'center', valign: 'middle', color: last ? C.lime : C.white });
      T(s, t, { x: x + 0.18, y: y0 + 0.66, w: cw - 0.3, h: 0.62, fontSize: 13, bold: true, color: fg, lineSpacingMultiple: 1.0 });
      T(s, d, { x: x + 0.18, y: y0 + 1.36, w: cw - 0.34, h: 1.9, fontSize: 13, color: last ? C.navyD : C.pale, lineSpacingMultiple: 1.2 });
    });
    T(s, '* Sous réserve de validation du dossier.', { x: M, y: 6.72, w: 8, h: 0.26, fontSize: 10.5, color: C.pale });
    pageNo(s, 7);
  }

  // ---------- 8 & 9. Services en détail
  const svcCard = (s, x, i) => {
    const y0 = 2.05, w = 3.76, h = 4.75, sv = SV[i];
    rrect(s, x, y0, w, h, C.white, 0.16, { shadow: softShadow() });
    disc(s, x + 0.3, y0 + 0.3, 0.62, C.green);
    T(s, String(i + 1), { x: x + 0.3, y: y0 + 0.3, w: 0.62, h: 0.62, fontSize: 17, bold: true, align: 'center', valign: 'middle' });
    T(s, sv[0], { x: x + 1.08, y: y0 + 0.3, w: w - 1.3, h: 0.62, fontSize: 15, bold: true, color: C.navy, valign: 'middle', lineSpacingMultiple: 1.0 });
    [['Vous nous transmettez', sv[2]], ['Nous faisons', sv[3]], ['Vous obtenez', sv[4]]].forEach(([lab, txt], k) => {
      const y = y0 + [1.08, 2.1, 3.42][k];
      if (k === 2) rrect(s, x + 0.16, y - 0.14, w - 0.32, 1.28, C.tint, 0.1);
      T(s, lab.toUpperCase(), { x: x + 0.32, y, w: w - 0.6, h: 0.22, fontSize: 10, bold: true, charSpacing: 2.5, color: C.greenD });
      T(s, txt, { x: x + 0.32, y: y + 0.27, w: w - 0.64, h: 0.78, fontSize: 13, bold: k === 2, color: k === 2 ? C.navy : C.grey, lineSpacingMultiple: 1.15 });
    });
  };
  const cardX = (k) => M + k * (3.76 + 0.275);
  {
    const s = slide(); s.background = { color: C.mist };
    kicker(s, 'Nos services en détail · 1/2', M, 0.65, C.greenD);
    title(s, 'De l’éligibilité au dossier', C.navy);
    [0, 1, 2].forEach((i) => svcCard(s, cardX(i), i));
    pageNo(s, 8);
  }
  {
    const s = slide(); s.background = { color: C.mist };
    kicker(s, 'Nos services en détail · 2/2', M, 0.65, C.greenD);
    title(s, 'Du contrôle au financement', C.navy);
    svcCard(s, cardX(0), 3); svcCard(s, cardX(1), 4);
    const x = cardX(2), y0 = 2.05, w = 3.76, h = 4.75, ph = 3.15;
    rrect(s, x, y0, w, h, C.navyD, 0.16, { shadow: softShadow() });
    await pic(s, 'chauffage', x, y0, w, ph, { fx: 0.47, fy: 0.45, r: [0.16, 0.16, 0, 0] });
    T(s, [{ text: 'Pendant ce temps,', options: { breakLine: true } }, { text: 'vous restez', options: { color: C.lime, breakLine: true } }, { text: 'sur vos chantiers.', options: { color: C.lime } }],
      { x: x + 0.32, y: y0 + ph + 0.3, w: w - 0.6, h: 1.05, fontSize: 18, bold: true, lineSpacingMultiple: 1.0 });
    pageNo(s, 9);
  }

  // ================================================================ VOS SECTEURS
  section('Vos secteurs');

  // ---------- 10. Mosaïque
  {
    const s = slide(); s.background = { color: C.navyD };
    const tiles = [['pompe-a-chaleur', 'Pompes à chaleur', 0.48, 0.5], ['chauffage', 'Chauffage', 0.5, 0.5], ['isolation-combles', 'Isolation', 0.68, 0.5], ['renovation', 'Rénovation énergétique', 0.58, 0.5], ['tertiaire', 'Tertiaire', 0.5, 0.5], ['industrie', 'Industrie', 0.62, 0.5], ['agricole', 'Agricole', 0.62, 0.5]];
    const tw = W / 4, th = H / 2, g = 0.04, lb = 0.78;
    rect(s, 0, 0, tw - g, th - g, C.green);
    T(s, 'NOS TERRAINS', { x: 0.42, y: 0.5, w: tw - 0.7, h: 0.3, fontSize: 11, bold: true, charSpacing: 4, color: C.navyD });
    T(s, [{ text: 'Partout où', options: { breakLine: true } }, { text: 'il y a de', options: { breakLine: true } }, { text: 'l’énergie à', options: { breakLine: true } }, { text: 'économiser.' }], { x: 0.42, y: 0.95, w: tw - 0.6, h: 2.2, fontSize: 28, bold: true, lineSpacingMultiple: 1.0 });
    for (let i = 0; i < tiles.length; i++) {
      const [img, label, fx, fy] = tiles[i];
      const k = i + 1, x = (k % 4) * tw + (k % 4 ? g : 0), y = Math.floor(k / 4) * th + (k >= 4 ? g : 0);
      const w = tw - (k % 4 ? g : g), h = th - g;
      await pic(s, img, x, y, w, h - lb, { fx, fy });
      rect(s, x, y + h - lb, w, lb, k % 2 ? C.navy : C.navyL);
      T(s, label, { x: x + 0.3, y: y + h - lb, w: w - 0.5, h: lb, fontSize: 16, bold: true, valign: 'middle' });
    }
    pageNo(s, 10);
  }

  // ---------- 11–14. Secteurs
  await sector(11, 1, 'L', 'isolation-combles', { fx: 0.5, fy: 0.5 }, 'Résidentiel', `Vos chantiers dans l’habitat,\nnos dossiers${NB}CEE.`,
    ['Installateurs de pompes à chaleur\net de systèmes de chauffage', 'Entreprises d’isolation\net de rénovation énergétique', 'Professionnels de la ventilation'], OV);
  await sector(12, 2, 'R', 'tertiaire', { fx: 0.5, fy: 0.5 }, 'Tertiaire', `Vos chantiers dans les bâtiments tertiaires,\nnos dossiers${NB}CEE.`,
    ['Entreprises intervenant\ndans le secteur tertiaire', 'Professionnels de la ventilation\net des équipements thermiques', 'Installateurs de systèmes de chauffage'], OV);
  await sector(13, 3, 'L', 'industrie', { fx: 0.5, fy: 0.5 }, 'Industrie', `Vos chantiers sur les sites industriels,\nnos dossiers${NB}CEE.`,
    ['Entreprises intervenant\ndans le secteur industriel', 'Professionnels des équipements thermiques', 'Professionnels de la ventilation'], OV);
  await sector(14, 4, 'L', 'agricole', { fx: 0.5, fy: 0.5 }, 'Agricole', `Vos chantiers dans les exploitations agricoles,\nnos dossiers${NB}CEE.`,
    ['Entreprises intervenant\ndans le secteur agricole', 'Professionnels des équipements thermiques', 'Installateurs de systèmes de chauffage'], OV);

  // ================================================================ NOS ENGAGEMENTS
  section('Nos engagements');

  // ---------- 15. Trois bénéfices (photo en haut, panneau plein en bas)
  {
    const s = slide(); s.background = { color: C.navyD };
    const cols = [['portrait-dossier', 0.5, 'Simplifier', 'Un interlocuteur unique pour toutes vos démarches CEE.'], ['portrait-conseillere', 0.55, 'Sécuriser', 'Des dossiers vérifiés au regard des exigences du dispositif.'], ['portrait-artisan', 0.42, 'Valoriser', 'Les meilleures conditions de valorisation recherchées auprès de nos partenaires.']];
    const g = 0.05, cw = (W - 2 * g) / 3, ph = 4.15;
    for (let i = 0; i < 3; i++) {
      const [img, fy, t, d] = cols[i], x = i * (cw + g);
      rect(s, x, ph, cw, H - ph, i === 1 ? C.navy : C.navyD);
      await pic(s, img, x, 0, cw, ph, { fx: 0.5, fy });
      disc(s, x + 0.5, ph - 0.45, 0.9, C.lime, { line: { color: i === 1 ? C.navy : C.navyD, width: 5 } });
      T(s, '0' + (i + 1), { x: x + 0.5, y: ph - 0.45, w: 0.9, h: 0.9, fontSize: 20, bold: true, align: 'center', valign: 'middle', color: C.navyD });
      T(s, t, { x: x + 0.5, y: ph + 0.72, w: cw - 0.8, h: 0.7, fontSize: 34, bold: true });
      T(s, d, { x: x + 0.5, y: ph + 1.55, w: cw - 1.0, h: 1.2, fontSize: 15, color: C.pale, lineSpacingMultiple: 1.2 });
    }
    pageNo(s, 15);
  }

  // ---------- 16. Pourquoi Cercle Énergie
  {
    const s = slide(); s.background = { color: C.navyD };
    const px = 4.9, ph = 3.5;
    await pic(s, 'remise-dossier', px, 0, W - px, ph, { fx: 0.5, fy: 0.45 });
    ring(s, -4.2, 5.0, 6.6, C.teal, 26, 72);
    kicker(s, 'Nos engagements', M, 1.05);
    T(s, [{ text: 'Pourquoi', options: { breakLine: true } }, { text: 'Cercle', options: { color: C.lime, breakLine: true } }, { text: `Énergie${NB}?`, options: { color: C.lime } }], { x: M, y: 1.45, w: 3.9, h: 1.9, fontSize: 38, bold: true, lineSpacingMultiple: 0.98 });
    T(s, 'Le partenaire unique\nde vos projets', { x: M, y: 3.9, w: 3.8, h: 0.7, fontSize: 16, color: C.pale, lineSpacingMultiple: 1.15 });
    const why = [
      ['FaUserTie', 'Un interlocuteur unique', 'Un seul contact pour toutes vos démarches CEE.'],
      ['FaClipboardCheck', 'Des dossiers vérifiés', `Chaque dossier est contrôlé au regard des exigences du${NB}dispositif.`],
      ['FaSearch', 'Les meilleures conditions recherchées', `Nous sollicitons nos partenaires pour valoriser vos${NB}projets.`],
      ['FaFlagCheckered', 'Un suivi jusqu’au financement', 'Jusqu’au versement des primes, sous réserve de validation du dossier.'],
    ];
    const x0 = px + 0.4, colW = 3.75, rows = [3.92, 5.42];
    for (let i = 0; i < 4; i++) {
      const [ic, t, d] = why[i], x = x0 + (i % 2) * colW, y = rows[Math.floor(i / 2)];
      disc(s, x, y, 0.62, C.navyL);
      await ico(s, ic, 'B9E35A', x + 0.17, y + 0.17, 0.28);
      T(s, t, { x: x + 0.82, y: y, w: colW - 1.05, h: 0.56, fontSize: 15, bold: true, valign: 'middle', lineSpacingMultiple: 1.0 });
      T(s, d, { x: x + 0.82, y: y + 0.64, w: colW - 1.1, h: 0.75, fontSize: 13, color: C.pale, lineSpacingMultiple: 1.15 });
    }
    pageNo(s, 16);
  }

  // ---------- 17. Avant / après
  {
    const s = slide(); s.background = { color: C.white };
    rect(s, W / 2, 0, W / 2, H, C.navy);
    T(s, 'SANS ACCOMPAGNEMENT', { x: M, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: '6F819B' });
    T(s, 'Vous gérez tout.', { x: M, y: 1.2, w: 5.4, h: 0.7, fontSize: 26, bold: true, color: C.navy });
    T(s, 'AVEC CERCLE ÉNERGIE', { x: W / 2 + 0.85, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: C.lime });
    T(s, 'Vous gérez vos chantiers.', { x: W / 2 + 0.85, y: 1.2, w: 5.0, h: 0.7, fontSize: 26, bold: true });
    const rows = [['Aides à identifier vous-même,\nchantier par chantier', 'Aides CEE identifiées\nselon vos travaux'], ['Dossiers à constituer, vérifier\net suivre en interne', 'Dossiers constitués,\nvérifiés et suivis'], ['Exigences du dispositif\nà maîtriser seul', 'Exigences documentaires\nvérifiées pour vous'], ['Acteurs du financement\nà trouver et à coordonner', 'Un partenaire unique,\nen lien avec les délégataires']];
    for (let i = 0; i < rows.length; i++) {
      const [a, b] = rows[i], y = 2.65 + i * 1.05;
      disc(s, M, y + 0.16, 0.46, 'D6DEE8');
      await ico(s, 'FaTimes', 'FFFFFF', M + 0.13, y + 0.29, 0.2);
      T(s, a, { x: M + 0.7, y, w: 4.5, h: 0.78, fontSize: 16, color: C.grey, valign: 'middle', lineSpacingMultiple: 1.1 });
      disc(s, W / 2 + 0.85, y + 0.16, 0.46, C.green);
      await ico(s, 'FaCheck', 'FFFFFF', W / 2 + 0.98, y + 0.29, 0.2);
      T(s, b, { x: W / 2 + 1.55, y, w: 4.3, h: 0.78, fontSize: 17, bold: true, valign: 'middle', lineSpacingMultiple: 1.1 });
    }
    disc(s, W / 2 - 0.55, 3.75, 1.1, C.green, { line: { color: C.white, width: 5 } });
    await ico(s, 'FaArrowRight', 'FFFFFF', W / 2 - 0.2, 4.1, 0.4);
    pageNo(s, 17);
  }

  // ---------- 18. FAQ
  {
    const s = slide(); s.background = { color: C.mist };
    kicker(s, 'Questions fréquentes', M, 0.65, C.greenD);
    title(s, 'Vos questions, nos réponses', C.navy);
    const qa = [
      [`Qu’est-ce qu’un mandataire CEE${NB}?`, 'Un intermédiaire qui fait le lien entre les entreprises d’installation et les acteurs du financement des CEE. À ce titre, Cercle Énergie travaille avec des délégataires CEE et simplifie vos démarches administratives.'],
      [`Avec qui travaillez-vous${NB}?`, 'Avec les installateurs de pompes à chaleur et de systèmes de chauffage, les entreprises d’isolation et de rénovation énergétique, les professionnels de la ventilation et des équipements thermiques, dans les secteurs résidentiel, tertiaire, industriel et agricole.'],
      [`Le versement des primes est-il garanti${NB}?`, `Non. Le versement des primes intervient sous réserve de validation du dossier. Notre rôle${NB}: constituer, vérifier et suivre votre dossier, puis coordonner avec les délégataires jusqu’à son${NB}traitement.`],
    ];
    qa.forEach(([q, a], i) => {
      const x = cardX(i), y0 = 2.05, w = 3.76, h = 4.75, hi = i === 2;
      rrect(s, x, y0, w, h, hi ? C.navyD : C.white, 0.16, { shadow: softShadow() });
      disc(s, x + 0.32, y0 + 0.32, 0.7, hi ? C.lime : C.green);
      T(s, '?', { x: x + 0.32, y: y0 + 0.32, w: 0.7, h: 0.7, fontSize: 22, bold: true, align: 'center', valign: 'middle', color: hi ? C.navyD : C.white });
      T(s, q, { x: x + 0.32, y: y0 + 1.22, w: w - 0.6, h: 0.66, fontSize: 17, bold: true, color: hi ? C.white : C.navy, lineSpacingMultiple: 1.0 });
      T(s, a, { x: x + 0.32, y: y0 + 2.02, w: w - 0.62, h: 2.5, fontSize: 13, color: hi ? C.pale : C.grey, lineSpacingMultiple: 1.2 });
    });
    pageNo(s, 18);
  }

  // ================================================================ DÉMARRER
  section('Démarrer');

  // ---------- 19. Démarrer
  {
    const s = slide(); s.background = { color: C.navyD };
    await pic(s, 'equipe', W / 2, 0, W / 2, H, { fx: 0.545, fy: 0.5 });
    ring(s, -4.3, 5.6, 6.2, C.teal, 26, 72);
    kicker(s, 'Démarrer', M, 0.7);
    T(s, [{ text: 'Un échange,', options: { breakLine: true } }, { text: 'et nous prenons', options: { color: C.lime, breakLine: true } }, { text: 'le relais.', options: { color: C.lime } }], { x: M, y: 1.08, w: 5.5, h: 1.4, fontSize: 30, bold: true, lineSpacingMultiple: 0.98 });
    const st = [['Vous prenez contact', 'Présentez-nous votre activité et vos travaux.'], ['Nous étudions l’éligibilité', 'Nous identifions les aides CEE mobilisables.'], ['Nous constituons le dossier', 'Constitution, vérification, suivi.'], ['Nous suivons le financement', 'Jusqu’au versement des primes, sous réserve de validation du dossier.']];
    st.forEach(([t, d], i) => {
      const y = 2.85 + i * 1.0;
      disc(s, M, y, 0.64, C.green);
      T(s, String(i + 1), { x: M, y, w: 0.64, h: 0.64, fontSize: 18, bold: true, align: 'center', valign: 'middle' });
      T(s, t, { x: M + 0.9, y: y - 0.02, w: 4.5, h: 0.32, fontSize: 16, bold: true });
      T(s, d, { x: M + 0.9, y: y + 0.33, w: 4.5, h: 0.5, fontSize: 13, color: C.pale, lineSpacingMultiple: 1.1 });
    });
    pageNo(s, 19);
  }

  // ---------- 20. Message clé
  {
    const s = slide();
    await pic(s, 'artisan-clients', 0, 0, W, H, { fx: 0.5, fy: 0.5 });
    s.addImage({ path: OV.bottom, x: 0, y: 0, w: W, h: H });
    kicker(s, 'Notre message', M, 4.55);
    T(s, [{ text: `«${NB}Vous réalisez les travaux, `, options: {} }, { text: `Cercle Énergie vous accompagne dans la gestion et le financement de vos aides CEE.${NB}»`, options: { color: C.lime } }],
      { x: M, y: 4.98, w: 11.2, h: 1.75, fontSize: 31, bold: true, lineSpacingMultiple: 1.0 });
    pageNo(s, 20);
  }

  // ---------- 21. Clôture
  {
    const s = slide(); s.background = { color: C.green };
    ring(s, 10.6, -3.9, 8.4, C.white, 40, 78); ring(s, -3.4, 5.0, 7.0, C.navy, 34, 80);
    logoPill(s, M, 0.6, 2.5, 'logo_full.png');
    T(s, 'Devenez partenaire.', { x: M, y: 2.75, w: CW, h: 1.2, fontSize: 64, bold: true });
    T(s, `Cercle Énergie${NB}: votre partenaire pour simplifier, sécuriser et valoriser vos projets d’économies d’énergie.`, { x: M, y: 4.2, w: 9.4, h: 1.0, fontSize: 20, bold: true, color: C.navyD, lineSpacingMultiple: 1.2 });
    const cts = [['FaPhoneAlt', '[Téléphone]'], ['FaEnvelope', '[E-mail]'], ['FaGlobe', '[Site web]']];
    for (let i = 0; i < 3; i++) {
      const x = M + i * 3.3;
      rrect(s, x, 5.75, 3.05, 0.84, C.navyD, 0.42);
      disc(s, x + 0.12, 5.87, 0.6, C.lime);
      await ico(s, cts[i][0], '07264B', x + 0.29, 6.04, 0.26);
      T(s, cts[i][1], { x: x + 0.9, y: 5.75, w: 2.0, h: 0.84, fontSize: 16, bold: true, valign: 'middle' });
    }
  }

  const f = await p.writeFile({ fileName: path.join(__dirname, 'Cercle-Energie-Plaquette.pptx') });
  try { require('child_process').execFileSync('zip', ['-dq', f, '*/']); } catch (e) { /* pas d'entrées dossier ou zip absent */ }
  console.log('écrit', f);
})().catch((e) => { console.error(e); process.exit(1); });
