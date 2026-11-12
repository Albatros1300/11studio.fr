// Présentation commerciale Cercle Énergie — alignée sur le brief de marque client (novembre 2026)
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
p.title = 'Cercle Énergie — Présentation commerciale';
p.company = 'Cercle Énergie';
p.author = 'Cercle Énergie';
p.theme = { headFontFace: F, bodyFontFace: F };

// ---------------------------------------------------------------- images
// Recadre `name` au ratio exact w/h (pouces) autour du point focal (fx, fy ∈ 0..1),
// zoom optionnel z ≥ 1, coins arrondis optionnels r = [hg, hd, bd, bg] en pouces (→ PNG,
// ou JPEG bien plus léger si `bg` donne la couleur unie du fond sous les coins).
async function crop(name, w, h, o = {}) {
  const { fx = 0.5, fy = 0.5, z = 1, r = null, bg = null } = o;
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
  if (bg) {
    const out = path.join(CROPS, `${tag}_r_${bg}.jpg`);
    const cut = await img.composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
    await sharp(cut).flatten({ background: '#' + bg }).jpeg({ quality: 90, chromaSubsampling: '4:4:4' }).withMetadata({ density: DPI }).toFile(out);
    return out;
  }
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


// Numérotation automatique : pageNo(s) lit le rang réel de la diapositive.
let NSL = 0;
const newSlide = () => { NSL += 1; const s = slide(); s._n = NSL; return s; };
const pno = (s) => pageNo(s, s._n);
// Hauteur estimée d'un bloc de texte (Montserrat est large : estimation prudente).
const estH = (text, pt, w, bold, lsm) => {
  const cpl = Math.max(1, Math.floor(w / ((pt / 72) * (bold ? 0.58 : 0.56))));
  const n = text.split('\n').reduce((a, l) => {
    let k = 1, cur = 0;
    l.split(' ').forEach((wd) => { if (cur && cur + 1 + wd.length > cpl) { k += 1; cur = wd.length; } else cur += (cur ? 1 : 0) + wd.length; });
    return a + k;
  }, 0);
  return n * (pt / 72) * 1.22 * (lsm || 1) + 0.04;
};
const NOTE = '* Selon les conditions contractuelles et la validation des dossiers.';
const NOTE2 = '* Selon les conditions contractuelles\net la validation des dossiers.';
// « 6e » avec e en exposant
const sixieme = (before, after, o) => [{ text: before + '6', options: o || {} }, { text: 'e', options: Object.assign({ superscript: true }, o || {}) }, { text: after, options: o || {} }];

// Pastilles en flux (retour à la ligne automatique). Retourne le y de fin.
const chips = (s, items, x, y, maxW, st) => {
  const pt = st.pt || 12, h = st.h || 0.5, gap = 0.14;
  let cx = x, cy = y;
  items.forEach((t) => {
    const w = t.length * (pt / 72) * 0.56 + 0.52;
    if (cx > x && cx + w > x + maxW) { cx = x; cy += h + gap; }
    rrect(s, cx, cy, w, h, st.fill, h / 2, st.line ? { line: st.line } : {});
    T(s, t, { x: cx, y: cy, w, h, fontSize: pt, bold: true, align: 'center', valign: 'middle', color: st.color });
    cx += w + gap;
  });
  return cy + h;
};

// Diapositive « volet » : photo paysage bord à bord d'un côté, texte de l'autre.
// La photo est pré-recadrée au ratio exact de sa boîte (7,6 × 6,1 po).
async function feature(o) {
  const { side, dark, photo, focal, ic, kick, titleLines, lead, items = [], note, leadPt = 14.5, tag } = o;
  const s = newSlide(); s.background = { color: dark ? C.navyD : C.mist };
  const pw = 7.6, ph = 6.1, py = (H - ph) / 2, R = 0.24;
  const px = side === 'R' ? W - pw : 0;
  await pic(s, photo, px, py, pw, ph, Object.assign({}, focal, { r: side === 'R' ? [R, 0, 0, R] : [0, R, R, 0], bg: dark ? C.navyD : C.mist }));
  const tx = side === 'R' ? M : pw + 0.6, tw = W - pw - M - 0.6;
  const fg = dark ? C.white : C.navy, sub = dark ? C.pale : C.grey;
  const TP = 26;
  const tH = titleLines.length * (TP / 72) * 1.18 + 0.05;
  const lH = estH(lead, leadPt, tw, false, 1.25);
  const iMax = Math.max(0.44, ...items.map((t) => estH(t, 14, tw - 0.62, true, 1.1)));
  const iH = items.map(() => iMax);
  const nH = note ? 0.5 : 0;
  const itemsH = items.length ? 0.42 + iH.reduce((a, b) => a + b + 0.16, 0) - 0.16 : 0;
  const tagH = tag ? 0.42 + 0.54 : 0;
  const total = 0.62 + 0.38 + tH + 0.28 + lH + itemsH + nH + tagH;
  let y = py + Math.max(0.15, (ph - total) / 2);
  disc(s, tx, y, 0.62, C.green);
  await ico(s, ic, 'FFFFFF', tx + 0.18, y + 0.18, 0.26);
  T(s, kick.toUpperCase(), { x: tx + 0.82, y, w: tw - 0.82, h: 0.62, fontSize: 12, bold: true, charSpacing: 4, valign: 'middle', color: dark ? C.lime : C.greenD });
  y += 0.62 + 0.38;
  T(s, titleLines.map((t, i) => ({ text: t.t || t, options: { breakLine: i < titleLines.length - 1, color: t.c || fg } })), { x: tx, y, w: tw + 0.2, h: tH, fontSize: TP, bold: true, color: fg, lineSpacingMultiple: 0.98 });
  y += tH + 0.28;
  T(s, lead, { x: tx, y, w: tw, h: lH, fontSize: leadPt, color: sub, lineSpacingMultiple: 1.25 });
  y += lH + 0.42;
  if (tag) {
    const w = tag.length * (12 / 72) * 0.6 + 0.6;
    rrect(s, tx, y, w, 0.54, dark ? C.navyL : C.white, 0.27, { line: { color: C.lime, width: 1.5 } });
    T(s, tag, { x: tx, y, w, h: 0.54, fontSize: 12, bold: true, align: 'center', valign: 'middle', color: fg });
  }
  for (let i = 0; i < items.length; i++) {
    const dy = y + (iH[i] - 0.4) / 2;
    disc(s, tx, dy, 0.4, dark ? C.lime : C.green);
    await ico(s, 'FaCheck', dark ? '07264B' : 'FFFFFF', tx + 0.12, dy + 0.12, 0.16);
    T(s, items[i], { x: tx + 0.62, y, w: tw - 0.62, h: iH[i], fontSize: 14, bold: true, color: fg, valign: 'middle', lineSpacingMultiple: 1.1 });
    y += iH[i] + 0.16;
  }
  if (note) T(s, note, { x: tx, y: y + 0.12, w: tw, h: 0.4, fontSize: 10.5, color: sub, lineSpacingMultiple: 1.1 });
  pno(s);
}

// Les huit étapes du parcours (section 4 du brief client).
const STEPS = [
  ['FaBullseye', 'Opportunité', 'Vous aider à accéder à des projets qualifiés et à mieux organiser la prise de contact avec vos prospects.'],
  ['FaSearch', 'Qualification du projet', 'Comprendre le besoin du client, le logement, l’équipement envisagé et les conditions d’éligibilité.'],
  ['FaClipboardList', 'Visite technique', 'Structurer les relevés et fiabiliser les informations recueillies sur place. Logiciel utilisé pour la visite : WOLTIC.'],
  ['FaBoxOpen', 'Choix des équipements', 'Vous donner accès à des équipements de qualité, notamment via des marques telles que Hitachi ou Thomson, selon les accords et gammes disponibles.'],
  ['FaFileInvoice', 'Devis et financement', 'Vous aider à présenter un projet lisible, à identifier les aides mobilisables et à expliquer le reste à charge.'],
  ['FaHardHat', 'Chantier et justificatifs', 'Accompagner la collecte des documents, les points de conformité et la traçabilité du dossier.'],
  ['FaTasks', 'Montage et suivi CEE', 'Préparer, contrôler et suivre vos dossiers, avec une visibilité sur leur état d’avancement.'],
  ['FaCheckCircle', 'Versement de la prime', 'Accompagner le suivi jusqu’au paiement, selon les conditions contractuelles et la validation des dossiers.'],
];
async function parcours(from, subtitle, withNote) {
  const s = newSlide(); s.background = { color: C.navyD };
  kicker(s, `Le parcours de A à Z · étapes ${from + 1} à ${from + 4}`, M, 0.65);
  title(s, [{ text: 'Le parcours de A à Z, ' }, { text: 'en huit étapes.', options: { color: C.lime } }]);
  T(s, subtitle, { x: M, y: 1.72, w: CW, h: 0.34, fontSize: 16, color: C.pale });
  // repère de progression : 8 points, 4 actifs
  for (let i = 0; i < 8; i++) {
    const on = i >= from && i < from + 4, d = 0.2, x = W - M - 8 * d - 7 * 0.14 + i * (d + 0.14);
    disc(s, x, 0.69, d, on ? C.lime : C.navyL);
  }
  const g = 0.2, cw = (CW - 3 * g) / 4, y0 = 2.95, ch = 3.55;
  for (let k = 0; k < 4; k++) {
    const i = from + k, [ic, t, d] = STEPS[i], x = M + k * (cw + g), last = i === 7, fg = last ? C.navyD : C.white;
    rrect(s, x, y0, cw, ch, last ? C.lime : C.navyL);
    disc(s, x + 0.24, y0 - 0.45, 0.9, last ? C.navyD : C.green, last ? { line: { color: C.lime, width: 2.5 } } : {});
    T(s, '0' + (i + 1), { x: x + 0.24, y: y0 - 0.45, w: 0.9, h: 0.9, fontSize: 21, bold: true, align: 'center', valign: 'middle', color: last ? C.lime : C.white });
    await ico(s, ic, last ? '07264B' : 'B9E35A', x + cw - 0.68, y0 + 0.26, 0.4);
    T(s, t, { x: x + 0.26, y: y0 + 0.72, w: cw - 0.5, h: 0.62, fontSize: 16, bold: true, color: fg, valign: 'bottom', lineSpacingMultiple: 1.0 });
    rect(s, x + 0.26, y0 + 1.46, 0.5, 0.045, last ? C.navyD : C.green);
    T(s, d, { x: x + 0.26, y: y0 + 1.66, w: cw - 0.46, h: 1.8, fontSize: 12.5, color: last ? C.navyD : C.pale, lineSpacingMultiple: 1.2 });
  }
  if (withNote) T(s, NOTE, { x: M, y: 6.82, w: 9, h: 0.26, fontSize: 10.5, color: C.pale });
  pno(s);
}

(async () => {
  await logoDims();
  const OV = {
    left: await overlay('ov_left', 0, 0, 1, 0, [[0, 0.97], [0.30, 0.94], [0.47, 0.74], [0.68, 0]]),
  };

  // ================================================================ OUVERTURE
  section('Ouverture');

  // ---------- 1. Couverture
  {
    const s = newSlide();
    await pic(s, 'pac-installation', 0, 0, W, H, { z: 1.15, fx: 0.465, fy: 0.55 });
    s.addImage({ path: OV.left, x: 0, y: 0, w: W, h: H });
    ring(s, 9.9, -5.0, 7.4, C.lime, 34, 55);
    logoPill(s, M, 0.5, 2.1, 'logo_full.png');
    disc(s, M, 2.44, 0.2, C.green);
    T(s, sixieme('MANDATAIRE CEE DE LA ', ' PÉRIODE'), { x: M + 0.36, y: 2.4, w: 7, h: 0.28, fontSize: 12, bold: true, charSpacing: 4, color: C.lime });
    T(s, [{ text: 'Vous installez.', options: { breakLine: true } }, { text: 'Nous vous', options: { color: C.lime, breakLine: true } }, { text: 'accompagnons', options: { color: C.lime, breakLine: true } }, { text: 'à chaque étape.', options: { color: C.lime } }],
      { x: M, y: 2.82, w: 6.9, h: 2.95, fontSize: 46, bold: true, lineSpacingMultiple: 0.95 });
    T(s, 'Cercle Énergie — Le partenaire unique de vos projets', { x: M, y: 5.98, w: 7.2, h: 0.35, fontSize: 17, bold: true });
    T(s, `CEE${NB}: Certificats d’Économies d’Énergie`, { x: M, y: 6.46, w: 6, h: 0.3, fontSize: 13, color: C.pale });
  }

  // ---------- 2. Les notions en clair
  {
    const s = newSlide(); s.background = { color: C.mist };
    kicker(s, 'Les notions en clair', M, 0.65, C.greenD);
    title(s, [{ text: 'Les CEE, ' }, { text: 'en trois notions', options: { color: C.green } }], C.navy);
    T(s, `CEE${NB}: Certificats d’Économies d’Énergie.`, { x: M, y: 1.72, w: CW, h: 0.34, fontSize: 16, color: C.grey });
    const N = [
      ['FaLandmark', 'Le dispositif CEE', 'Un dispositif d’État. Il oblige les fournisseurs d’énergie et les distributeurs de carburant à financer des travaux de rénovation énergétique, sous peine de pénalités.'],
      ['FaBolt', `Les «${NB}obligés${NB}»`, 'Les fournisseurs d’énergie et les distributeurs de carburant. Ce sont eux que le dispositif oblige à financer ces travaux.'],
      ['FaHandshake', 'Le mandataire CEE', 'Une société de services spécialisée, qui aide les obligés à réaliser leurs obligations. Experte du montage des dossiers, des règles fixées par l’État et de l’accompagnement des entreprises de travaux.'],
    ];
    const g = 0.275, cw = (CW - 2 * g) / 3, y0 = 2.3, ch = 3.52;
    for (let i = 0; i < 3; i++) {
      const [ic, t, d] = N[i], x = M + i * (cw + g), hi = i === 2;
      rrect(s, x, y0, cw, ch, hi ? C.navyD : C.white, 0.16, { shadow: softShadow() });
      disc(s, x + 0.32, y0 + 0.32, 0.78, hi ? C.lime : C.green);
      await ico(s, ic, hi ? '07264B' : 'FFFFFF', x + 0.32 + 0.23, y0 + 0.32 + 0.23, 0.32);
      T(s, '0' + (i + 1), { x: x + cw - 1.05, y: y0 + 0.44, w: 0.75, h: 0.5, fontSize: 24, bold: true, align: 'right', color: hi ? C.lime : C.pale });
      T(s, t, { x: x + 0.32, y: y0 + 1.26, w: cw - 0.6, h: 0.4, fontSize: 19, bold: true, color: hi ? C.white : C.navy });
      T(s, d, { x: x + 0.32, y: y0 + 1.74, w: cw - 0.56, h: 1.7, fontSize: 12.5, color: hi ? C.pale : C.grey, lineSpacingMultiple: 1.22 });
    }
    rrect(s, M, 6.06, CW, 0.7, C.navy, 0.35);
    T(s, [...sixieme('Cercle Énergie est mandataire CEE de la ', ' période. ', { bold: true, color: C.lime }), { text: 'Et, pour vous, le partenaire unique de vos projets.' }],
      { x: M + 0.4, y: 6.06, w: CW - 0.8, h: 0.7, fontSize: 14.5, valign: 'middle', align: 'center' });
    pno(s);
  }

  // ================================================================ VOUS
  section('Vous');

  // ---------- 3. À qui nous parlons
  {
    const s = newSlide(); s.background = { color: C.mist };
    const pw = 5.0;
    await pic(s, 'chauffage', 0, 0, pw, H, { fx: 0.47, fy: 0.5 });
    rect(s, pw, 0, 0.09, H, C.green);
    const x = pw + 0.8, w = W - x - M;
    kicker(s, 'À qui nous parlons', x, 0.72, C.greenD);
    T(s, [{ text: 'Aux professionnels', options: { breakLine: true } }, { text: 'de terrain.', options: { color: C.green } }], { x, y: 1.08, w, h: 1.12, fontSize: 32, bold: true, color: C.navy, lineSpacingMultiple: 0.98 });
    T(s, `Votre priorité${NB}: conseiller, dimensionner,\ninstaller et satisfaire vos clients.`, { x, y: 2.34, w, h: 0.66, fontSize: 15, color: C.grey, lineSpacingMultiple: 1.25 });
    T(s, 'VOS MÉTIERS', { x, y: 3.3, w, h: 0.26, fontSize: 11, bold: true, charSpacing: 4, color: C.greenD });
    let y = chips(s, ['Artisans chauffagistes', 'Entreprises de génie climatique', 'Spécialistes de l’isolation', 'Professionnels RGE**'], x, 3.66, w, { fill: C.navy, color: C.white, h: 0.46 });
    T(s, 'VOS CHANTIERS CHEZ LES PARTICULIERS', { x, y: y + 0.36, w, h: 0.26, fontSize: 11, bold: true, charSpacing: 4, color: C.greenD });
    y = chips(s, ['Pompes à chaleur (PAC) air/eau', 'PAC air/air*', 'Chauffe-eau thermodynamiques'], x, y + 0.72, w, { fill: C.tint, color: C.navy, line: { color: C.green, width: 1 }, h: 0.46 });
    T(s, [{ text: '* Lorsque les dispositifs le permettent.', options: { breakLine: true } }, { text: `** RGE${NB}: Reconnu Garant de l’Environnement.` }], { x, y: 6.58, w: w - 0.8, h: 0.5, fontSize: 10.5, color: C.grey, lineSpacingMultiple: 1.15 });
    pno(s);
  }

  // ---------- 4. Vos irritants quotidiens
  {
    const s = newSlide(); s.background = { color: C.navyD };
    ring(s, 10.3, -4.4, 6.8, C.teal, 26, 75);
    kicker(s, 'Votre quotidien', M, 0.65);
    title(s, [{ text: 'Votre quotidien, ' }, { text: 'nous le connaissons.', options: { color: C.lime } }]);
    T(s, 'Vous faites des chantiers de qualité. Autour, cinq sujets vous prennent du temps.', { x: M, y: 1.72, w: 10.5, h: 0.34, fontSize: 16, color: C.pale });
    const I = [
      ['FaBalanceScale', 'Des offres difficiles à comparer', `Négoces et fabricants${NB}: prix, disponibilité, qualité, support, conditions.`],
      ['FaSyncAlt', 'Des aides complexes et mouvantes', 'Les CEE et les autres dispositifs demandent du temps pour être suivis.'],
      ['FaShieldAlt', 'Un besoin de confiance', 'La crainte d’une erreur ou d’un refus de dossier.'],
      ['FaPuzzlePiece', 'Une chaîne morcelée', 'Contacts, visites, devis, équipements, justificatifs, suivi, primes, trésorerie.'],
      ['FaUser', 'Le sentiment de tout gérer seul', `Commercial, technique, administratif, financier${NB}: tout repose sur vous.`],
    ];
    const gap = 0.14, cw = (CW - 4 * gap) / 5, y0 = 2.42, ch = 3.42;
    for (let i = 0; i < 5; i++) {
      const [ic, t, d] = I[i], x = M + i * (cw + gap);
      rrect(s, x, y0, cw, ch, C.navyL);
      disc(s, x + 0.2, y0 + 0.24, 0.72, C.green);
      await ico(s, ic, 'FFFFFF', x + 0.2 + 0.21, y0 + 0.24 + 0.21, 0.3);
      T(s, t, { x: x + 0.2, y: y0 + 1.16, w: cw - 0.32, h: 0.72, fontSize: 13.5, bold: true, lineSpacingMultiple: 1.0 });
      T(s, d, { x: x + 0.2, y: y0 + 2.0, w: cw - 0.36, h: 1.32, fontSize: 12, color: C.pale, lineSpacingMultiple: 1.2 });
    }
    rrect(s, M, 6.06, 8.9, 0.7, C.lime, 0.35);
    T(s, 'Moins de temps dans l’administratif, plus de temps sur vos chantiers.', { x: M + 0.3, y: 6.06, w: 8.3, h: 0.7, fontSize: 15, bold: true, color: C.navyD, valign: 'middle', align: 'center' });
    pno(s);
  }

  // ================================================================ NOTRE POSITIONNEMENT
  section('Notre positionnement');

  // ---------- 5. Notre promesse
  {
    const s = newSlide(); s.background = { color: C.navyD };
    ring(s, 10.6, -4.2, 7.6, C.lime, 34, 72);
    kicker(s, 'Notre promesse', M, 0.85);
    T(s, [{ text: 'Moins de complexité, plus de visibilité', options: { breakLine: true } }, { text: `et un accompagnement concret${NB}:`, options: { breakLine: true } }, { text: 'du premier contact commercial', options: { color: C.lime, breakLine: true } }, { text: 'au versement de la prime*.', options: { color: C.lime } }],
      { x: M, y: 1.3, w: CW, h: 2.3, fontSize: 34, bold: true, lineSpacingMultiple: 0.98 });
    T(s, [{ text: `Notre ambition${NB}: `, options: { bold: true, color: C.white } }, { text: 'être le partenaire de référence des artisans, notamment des chauffagistes qui installent des pompes à chaleur ou des chauffe-eau thermodynamiques. Et devenir votre point d’entrée unique vers les services, les outils, les financements et les partenaires utiles à votre activité.' }],
      { x: M, y: 3.86, w: 9.4, h: 1.55, fontSize: 16, color: C.pale, lineSpacingMultiple: 1.25 });
    const pw = [2.3, 2.9, 4.5], pl = ['Fiable', 'Accessible', 'Présent à chaque étape'];
    let px = M;
    pl.forEach((t, i) => {
      rrect(s, px, 5.7, pw[i], 0.82, i === 1 ? C.lime : C.green, 0.41);
      T(s, t, { x: px, y: 5.7, w: pw[i], h: 0.82, fontSize: 20, bold: true, align: 'center', valign: 'middle', color: i === 1 ? C.navyD : C.white });
      px += pw[i] + 0.22;
    });
    T(s, NOTE, { x: M, y: 6.82, w: 9, h: 0.26, fontSize: 10.5, color: C.pale });
    pno(s);
  }

  // ---------- 6. Un cercle de confiance
  {
    const s = newSlide(); s.background = { color: C.mist };
    kicker(s, 'Notre positionnement', M, 0.65, C.greenD);
    title(s, [{ text: 'Un cercle ' }, { text: 'de confiance', options: { color: C.green } }], C.navy);
    T(s, 'Le cercle symbolise la continuité de l’accompagnement, la proximité et la coopération.', { x: M, y: 1.72, w: CW, h: 0.34, fontSize: 16, color: C.grey });
    const cx = W / 2, cy = 4.13;
    ring(s, cx - 1.72, cy - 1.72, 3.44, C.teal, 2, 35);
    ring(s, cx - 1.45, cy - 1.45, 2.9, C.green, 16);
    disc(s, cx - 1.12, cy - 1.12, 2.24, C.white, { shadow: softShadow() });
    logoAt(s, cx, cy, 1.62);
    const P = [
      ['FaRoute', 'Simplicité', 'Un interlocuteur identifié, des étapes claires et des informations compréhensibles.'],
      ['FaShieldAlt', 'Confiance', 'Des dossiers rigoureux, une communication transparente et une culture de conformité.'],
      ['FaChartLine', 'Performance', 'Des outils et services qui font gagner du temps et aident à convertir les projets.'],
      ['FaComments', 'Proximité', 'Un langage de terrain, des échanges humains et une connaissance des contraintes des installateurs.'],
    ];
    const cw = 4.1, ch = 1.76, xs = [M, W - M - cw], ys = [2.3, 4.2];
    for (let i = 0; i < 4; i++) {
      const [ic, t, d] = P[i], x = xs[i % 2], y = ys[Math.floor(i / 2)];
      rrect(s, x, y, cw, ch, C.white, 0.16, { shadow: softShadow() });
      disc(s, x + 0.26, y + 0.26, 0.7, C.green);
      await ico(s, ic, 'FFFFFF', x + 0.26 + 0.2, y + 0.26 + 0.2, 0.3);
      T(s, t, { x: x + 1.16, y: y + 0.22, w: cw - 1.3, h: 0.36, fontSize: 18, bold: true, color: C.navy });
      T(s, d, { x: x + 1.16, y: y + 0.62, w: cw - 1.38, h: 1.0, fontSize: 12, color: C.grey, lineSpacingMultiple: 1.18 });
    }
    rrect(s, M, 6.14, CW - 0.9, 0.66, C.navy, 0.33);
    T(s, [{ text: 'Expliquer', options: { bold: true, color: C.lime } }, { text: ' plutôt que promettre.  ' }, { text: 'Répondre', options: { bold: true, color: C.lime } }, { text: ' plutôt que renvoyer.  ' }, { text: 'Sécuriser', options: { bold: true, color: C.lime } }, { text: ' plutôt que complexifier.' }],
      { x: M + 0.3, y: 6.14, w: CW - 1.5, h: 0.66, fontSize: 14, valign: 'middle', align: 'center' });
    pno(s);
  }

  // ================================================================ LE PARCOURS DE A À Z
  section('Le parcours de A à Z');
  // ---------- 7–8. Les huit étapes
  await parcours(0, 'Du premier contact au paiement de la prime*, un seul cercle de services.', true);
  await parcours(4, 'Vous installez. Nous vous accompagnons à chaque étape.', false);

  // ================================================================ NOS SERVICES
  section('Nos services');

  // ---------- 9. Le cœur de métier : le financement CEE
  await feature({ side: 'R', dark: false, photo: 'qualification-rge', focal: { fx: 0.57, fy: 0.5 }, ic: 'FaFileSignature', kick: 'Le cœur de métier',
    titleLines: ['Le financement CEE,', { t: 'notre cœur de métier', c: C.green }],
    lead: `Une équipe d’experts dédiée vous accompagne, avec deux exigences${NB}:\nla pédagogie et la conformité.`,
    items: ['Comprendre les règles', 'Constituer et contrôler\nvos dossiers', 'Suivre chaque étape,\njusqu’au paiement des primes*'], note: NOTE2 });

  // ---------- 10. La visite technique avec WOLTIC
  await feature({ side: 'L', dark: true, photo: 'artisan-clients', focal: { fx: 0.6, fy: 0.5 }, ic: 'FaClipboardList', kick: 'La visite technique',
    titleLines: ['La visite technique', { t: 'avec WOLTIC', c: C.lime }],
    lead: 'WOLTIC est le logiciel utilisé pour les visites techniques. Il aide à structurer la collecte des informations terrain.', leadPt: 16, tag: 'Étape 03 du parcours' });

  // ---------- 11. Un suivi humain de vos dossiers
  await feature({ side: 'R', dark: false, photo: 'portrait-conseillere', focal: { fx: 0.4, fy: 0.5 }, ic: 'FaUserFriends', kick: 'Le suivi',
    titleLines: ['Un suivi humain', { t: 'de vos dossiers', c: C.green }],
    lead: 'Des dossiers suivis, des règles expliquées, un partenaire à vos côtés.',
    items: ['Une équipe d’experts dédiée', 'Un interlocuteur identifié', 'Une visibilité sur l’avancement\nde vos dossiers'] });

  // ---------- 12. Des équipements et des partenaires sélectionnés
  await feature({ side: 'L', dark: true, photo: 'fournisseur', focal: { fx: 0.45, fy: 0.5 }, ic: 'FaBoxOpen', kick: 'Les équipements',
    titleLines: ['Des équipements', { t: 'sélectionnés', c: C.lime }],
    lead: 'Un accès simplifié à des équipements de qualité, notamment via des marques telles que Hitachi ou Thomson, selon les accords et gammes disponibles.',
    items: ['Cohérence technique', 'Un choix adapté au chantier', 'Disponibilité et\naccompagnement commercial'] });

  // ---------- 13. Un cercle qui s'élargit
  {
    const s = newSlide(); s.background = { color: C.navyD };
    const lw = 4.9;
    kicker(s, 'Et demain', M, 0.85);
    T(s, [{ text: 'Un cercle', options: { breakLine: true } }, { text: 'qui s’élargit.', options: { color: C.lime } }], { x: M, y: 1.3, w: lw, h: 1.45, fontSize: 40, bold: true, lineSpacingMultiple: 0.98 });
    T(s, 'Le cercle pourra s’élargir à d’autres services utiles à votre activité.', { x: M, y: 3.1, w: lw, h: 1.0, fontSize: 17, lineSpacingMultiple: 1.25 });
    rect(s, M, 4.42, 0.6, 0.05, C.green);
    T(s, 'Ces services sont envisagés pour la suite. Ils ne font pas partie de l’offre actuelle et seront annoncés lorsqu’ils seront disponibles.', { x: M, y: 4.7, w: lw - 0.3, h: 1.3, fontSize: 13.5, color: C.pale, lineSpacingMultiple: 1.25 });
    const cx = 9.35, cy = 3.8, R = 2.25;
    ring(s, cx - 3.05, cy - 3.05, 6.1, C.teal, 2, 55);
    s.addShape(p.ShapeType.ellipse, { x: cx - R, y: cy - R, w: 2 * R, h: 2 * R, fill: { type: 'none' }, line: { color: C.lime, width: 2.25, dashType: 'dash' } });
    ring(s, cx - 1.3, cy - 1.3, 2.6, C.green, 14);
    disc(s, cx - 1.0, cy - 1.0, 2.0, C.white);
    logoAt(s, cx, cy, 1.45);
    const F = [['Accompagnement technique', -90, 3.1], ['Outils digitaux', -18, 2.2], ['Formation', 54, 1.9], ['Partenariats', 126, 1.9], ['Appui commercial', 198, 2.3]];
    F.forEach(([t, a, w]) => {
      const px = cx + R * Math.cos(a * Math.PI / 180), py = cy + R * Math.sin(a * Math.PI / 180), h = 0.58;
      rrect(s, px - w / 2, py - h / 2, w, h, C.navyL, h / 2, { line: { color: C.lime, width: 1.5 } });
      T(s, t, { x: px - w / 2, y: py - h / 2, w, h, fontSize: 13, bold: true, align: 'center', valign: 'middle' });
    });
    pno(s);
  }

  // ================================================================ NOTRE FAÇON DE TRAVAILLER
  section('Notre façon de travailler');

  // ---------- 14. Ce que nous ne promettons pas / notre façon de travailler
  {
    const s = newSlide(); s.background = { color: C.white };
    rect(s, W / 2, 0, W / 2, H, C.navy);
    T(s, 'CE QUE NOUS NE PROMETTONS PAS', { x: M, y: 0.8, w: 5.4, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: '6F819B' });
    T(s, 'Pas de promesse en l’air.', { x: M, y: 1.2, w: 5.5, h: 0.7, fontSize: 26, bold: true, color: C.navy });
    T(s, 'NOTRE FAÇON DE TRAVAILLER', { x: W / 2 + 0.85, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: C.lime });
    T(s, 'Des règles expliquées.', { x: W / 2 + 0.85, y: 1.2, w: 5.2, h: 0.7, fontSize: 26, bold: true });
    const rows = [
      ['Une prime garantie', 'Des étapes et des conditions\nexpliquées'],
      ['Un versement systématique', 'Des pièces et des points\nde conformité contrôlés'],
      ['Un délai identique\npour tous les dossiers', 'Une visibilité sur\nl’avancement de vos dossiers'],
      ['Un discours centré\nsur le montant des aides', 'Un suivi jusqu’au\npaiement des primes*'],
    ];
    for (let i = 0; i < rows.length; i++) {
      const [a, b] = rows[i], y = 2.42 + i * 1.02;
      disc(s, M, y + 0.16, 0.46, 'D6DEE8');
      await ico(s, 'FaTimes', 'FFFFFF', M + 0.13, y + 0.29, 0.2);
      T(s, a, { x: M + 0.7, y, w: 4.5, h: 0.78, fontSize: 16, color: C.grey, valign: 'middle', lineSpacingMultiple: 1.1 });
      disc(s, W / 2 + 0.85, y + 0.16, 0.46, C.green);
      await ico(s, 'FaCheck', 'FFFFFF', W / 2 + 0.98, y + 0.29, 0.2);
      T(s, b, { x: W / 2 + 1.55, y, w: 4.4, h: 0.78, fontSize: 17, bold: true, valign: 'middle', lineSpacingMultiple: 1.1 });
    }
    disc(s, W / 2 - 0.55, 3.4, 1.1, C.green, { line: { color: C.white, width: 5 } });
    await ico(s, 'FaArrowRight', 'FFFFFF', W / 2 - 0.2, 3.75, 0.4);
    T(s, NOTE2, { x: W / 2 + 0.85, y: 6.62, w: 4.4, h: 0.42, fontSize: 10.5, color: C.pale, lineSpacingMultiple: 1.1 });
    pno(s);
  }

  // ================================================================ PARLONS DE VOS PROJETS
  section('Parlons de vos projets');

  // ---------- 15. Notre cap (citation d'intention — pas un témoignage)
  {
    const s = newSlide(); s.background = { color: C.navyD };
    await pic(s, 'equipe', W / 2, 0, W / 2, H, { fx: 0.545, fy: 0.5 });
    ring(s, -4.3, 5.6, 6.2, C.teal, 26, 72);
    kicker(s, 'Notre cap', M, 0.8);
    T(s, `Ce que nous voulons que chaque artisan puisse se dire en travaillant avec nous${NB}:`, { x: M, y: 1.3, w: 5.2, h: 0.75, fontSize: 15, color: C.pale, lineSpacingMultiple: 1.25 });
    rect(s, M, 2.42, 0.07, 3.0, C.green);
    const BL = { breakLine: true }, LB = { color: C.lime, breakLine: true };
    T(s, [{ text: `«${NB}Enfin un partenaire`, options: BL }, { text: 'qui comprend mon métier,', options: BL }, { text: 'me parle simplement,', options: LB }, { text: 'm’aide à monter', options: LB }, { text: 'des projets solides', options: LB }, { text: 'et reste présent', options: LB }, { text: `jusqu’au bout.${NB}»`, options: { color: C.lime } }],
      { x: M + 0.35, y: 2.38, w: 5.2, h: 3.1, fontSize: 23, bold: true, lineSpacingMultiple: 1.08, valign: 'middle' });
    T(s, 'C’est notre objectif, pas un témoignage client.', { x: M, y: 5.82, w: 5.3, h: 0.3, fontSize: 12, color: C.pale });
    pno(s);
  }

  // ---------- 16. Clôture
  {
    const s = newSlide(); s.background = { color: C.green };
    ring(s, 10.6, -3.9, 8.4, C.white, 40, 78); ring(s, -3.6, 5.75, 7.0, C.navy, 34, 80);
    logoPill(s, M, 0.6, 2.5, 'logo_full.png');
    T(s, 'Parlons de vos projets', { x: M, y: 2.8, w: CW, h: 1.15, fontSize: 60, bold: true });
    T(s, [{ text: 'Cercle Énergie, le partenaire unique de vos projets.', options: { breakLine: true } }, { text: 'Les bons équipements, les bons outils, le bon accompagnement.' }], { x: M, y: 4.2, w: CW, h: 1.0, fontSize: 20, bold: true, color: C.navyD, lineSpacingMultiple: 1.2 });
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
  console.log('écrit', f, '—', NSL, 'diapositives');
})().catch((e) => { console.error(e); process.exit(1); });
