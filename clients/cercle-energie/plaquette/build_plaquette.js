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
const NOTE = '* Sous réserve de validation du dossier.';

// Diapositive « volet » : photo paysage bord à bord d'un côté, texte de l'autre.
// La photo est pré-recadrée au ratio exact de sa boîte (7,6 × 6,1 po).
async function volet(idx, side, dark, photo, focal, titleLines, lead, items, note) {
  const s = newSlide(); s.background = { color: dark ? C.navyD : C.mist };
  const pw = 7.6, ph = 6.1, py = (H - ph) / 2, R = 0.24;
  const px = side === 'R' ? W - pw : 0;
  await pic(s, photo, px, py, pw, ph, Object.assign({}, focal, { r: side === 'R' ? [R, 0, 0, R] : [0, R, R, 0], bg: dark ? C.navyD : C.mist }));
  const tx = side === 'R' ? M : pw + 0.6, tw = W - pw - M - 0.6;
  const fg = dark ? C.white : C.navy, sub = dark ? C.pale : C.grey;
  // mesure du bloc pour le centrer verticalement sur la hauteur de la photo
  const tH = titleLines.length * (28 / 72) * 1.18 + 0.05;
  const lH = estH(lead, 14.5, tw, false, 1.25);
  const iMax = Math.max(0.44, ...items.map((t) => estH(t, 14, tw - 0.62, true, 1.1)));
  const iH = items.map(() => iMax);
  const nH = note ? 0.5 : 0;
  const total = 0.62 + 0.38 + tH + 0.28 + lH + 0.42 + iH.reduce((a, b) => a + b + 0.16, 0) - 0.16 + nH;
  let y = py + Math.max(0.15, (ph - total) / 2);
  disc(s, tx, y, 0.62, C.green);
  T(s, '0' + idx, { x: tx, y, w: 0.62, h: 0.62, fontSize: 17, bold: true, align: 'center', valign: 'middle' });
  T(s, `VOLET ${idx} SUR 6`, { x: tx + 0.82, y, w: tw - 0.82, h: 0.62, fontSize: 12, bold: true, charSpacing: 4, valign: 'middle', color: dark ? C.lime : C.greenD });
  y += 0.62 + 0.38;
  T(s, titleLines.map((t, i) => ({ text: t, options: { breakLine: i < titleLines.length - 1 } })), { x: tx, y, w: tw + 0.2, h: tH, fontSize: 28, bold: true, color: fg, lineSpacingMultiple: 0.98 });
  y += tH + 0.28;
  T(s, lead, { x: tx, y, w: tw, h: lH, fontSize: 14.5, color: sub, lineSpacingMultiple: 1.25 });
  y += lH + 0.42;
  for (let i = 0; i < items.length; i++) {
    const dy = y + (iH[i] - 0.4) / 2;
    disc(s, tx, dy, 0.4, dark ? C.lime : C.green);
    await ico(s, 'FaCheck', dark ? '07264B' : 'FFFFFF', tx + 0.12, dy + 0.12, 0.16);
    T(s, items[i], { x: tx + 0.62, y, w: tw - 0.62, h: iH[i], fontSize: 14, bold: true, color: fg, valign: 'middle', lineSpacingMultiple: 1.1 });
    y += iH[i] + 0.16;
  }
  if (note) T(s, note, { x: tx, y: y + 0.12, w: tw, h: 0.24, fontSize: 10.5, color: sub });
  pno(s);
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
    const s = newSlide();
    await pic(s, 'pac-installation', 0, 0, W, H, { z: 1.15, fx: 0.465, fy: 0.55 });
    s.addImage({ path: OV.left, x: 0, y: 0, w: W, h: H });
    ring(s, 9.9, -5.0, 7.4, C.lime, 34, 55);
    logoPill(s, M, 0.5, 2.1, 'logo_full.png');
    kicker(s, 'Le réseau d’accompagnement des artisans RGE', M, 2.45);
    T(s, [{ text: 'Artisans RGE,', options: { breakLine: true } }, { text: 'vous n’êtes', options: { color: C.lime, breakLine: true } }, { text: 'plus seuls.', options: { color: C.lime } }],
      { x: M, y: 2.85, w: 6.8, h: 2.55, fontSize: 56, bold: true, lineSpacingMultiple: 0.95 });
    T(s, 'Le partenaire unique de vos projets', { x: M, y: 5.72, w: 6.4, h: 0.35, fontSize: 18, bold: true });
    T(s, 'Dossiers CEE, démarches administratives, formation, qualification RGE, fournisseurs, réseau.', { x: M, y: 6.16, w: 5.5, h: 0.7, fontSize: 14, color: C.pale, lineSpacingMultiple: 1.2 });
  }

  // ---------- 2. Le constat
  {
    const s = newSlide();
    await pic(s, 'paperasse', 0, 0, W, H, { fx: 0.5, fy: 0.5 });
    s.addImage({ path: OV.right, x: 0, y: 0, w: W, h: H });
    const x = 7.15;
    kicker(s, 'Le constat', x, 0.95);
    T(s, [{ text: 'Petit artisan RGE,', options: { breakLine: true } }, { text: 'seul face à tout.', options: { color: C.lime } }],
      { x, y: 1.38, w: 5.6, h: 1.15, fontSize: 32, bold: true, lineSpacingMultiple: 0.98 });
    const pts = [
      ['FaFolderOpen', 'L’administratif', `Dossiers, pièces à réunir, suivi${NB}: du temps en moins sur vos chantiers.`],
      ['FaAward', 'Les exigences RGE', 'Une qualification à obtenir, puis à conserver.'],
      ['FaTags', 'Les prix fournisseurs', 'Difficile de négocier son matériel quand on est seul.'],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, t, d] = pts[i], y = 3.0 + i * 1.28;
      disc(s, x, y, 0.72, C.navyL, { line: { color: C.lime, width: 1.5 } });
      await ico(s, ic, 'B9E35A', x + 0.21, y + 0.21, 0.3);
      T(s, t, { x: x + 0.98, y: y - 0.02, w: 4.4, h: 0.36, fontSize: 18, bold: true });
      T(s, d, { x: x + 0.98, y: y + 0.38, w: 4.3, h: 0.62, fontSize: 14, color: C.pale, lineSpacingMultiple: 1.15 });
    }
    pno(s);
  }

  // ---------- 3. La réponse
  {
    const s = newSlide(); s.background = { color: C.navyD };
    ring(s, -3.6, 5.2, 7.2, C.teal, 30, 70); ring(s, 9.4, -3.4, 7.6, C.lime, 34, 72);
    kicker(s, 'Notre réponse', M, 0.85);
    T(s, [{ text: 'Ce que vous n’arrivez pas', options: { breakLine: true } }, { text: 'à faire seul,', options: { breakLine: true } }, { text: 'on vous aide à le faire.', options: { color: C.lime } }],
      { x: M, y: 1.3, w: CW, h: 2.05, fontSize: 42, bold: true, lineSpacingMultiple: 0.98 });
    T(s, `Cercle Énergie est un réseau d’accompagnement pour les artisans RGE, surtout les petits artisans. Mandataire CEE, nous gérons vos dossiers${NB}: c’est le cœur de notre métier. Mais ce n’est plus tout. Administratif, formation, qualification RGE, fournisseurs${NB}: nous vous aidons là où vous êtes seul.`,
      { x: M, y: 3.62, w: 9.0, h: 1.75, fontSize: 17, color: C.pale, lineSpacingMultiple: 1.25 });
    ['Simplifier', 'Sécuriser', 'Valoriser'].forEach((w, i) => {
      const x = M + i * 3.05;
      rrect(s, x, 5.75, 2.8, 0.85, i === 1 ? C.lime : C.green, 0.42);
      T(s, w, { x, y: 5.75, w: 2.8, h: 0.85, fontSize: 22, bold: true, align: 'center', valign: 'middle', color: i === 1 ? C.navyD : C.white });
    });
    pno(s);
  }

  // ================================================================ COMPRENDRE
  section('Comment ça marche');

  // ---------- 4. Comment ça marche (schéma)
  {
    const s = newSlide(); s.background = { color: C.mist };
    kicker(s, 'Comment ça marche', M, 0.65, C.greenD);
    title(s, 'Des fournisseurs d’énergie à votre client', C.navy);
    const nodes = [
      ['FaBolt', `Les «${NB}obligés${NB}»`, 'Les fournisseurs d’énergie. L’État les oblige à financer des économies d’énergie.'],
      ['FaLandmark', 'Les délégataires', `Les obligés leur délèguent cette obligation. Ils financent les primes${NB}CEE*.`],
      [null, 'Cercle Énergie', 'Mandataire. Fait le lien entre vous et les délégataires, et prend en charge l’administratif.'],
      ['FaTools', 'L’artisan RGE', 'Vous réalisez les travaux.'],
      ['FaHome', 'Votre client', `Il bénéficie de la prime${NB}CEE*.`],
    ];
    const colW = CW / 5, d = 1.6, cy = 3.0;
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
      T(s, t, { x: cx - colW / 2, y: 4.1, w: colW, h: 0.35, fontSize: 16, bold: true, color: i === 2 ? C.greenD : C.navy, align: 'center' });
      T(s, desc, { x: cx - 1.1, y: 4.5, w: 2.2, h: 1.25, fontSize: 12.5, color: C.grey, align: 'center', lineSpacingMultiple: 1.15 });
    }
    rrect(s, M, 5.92, CW, 0.74, C.navy, 0.37);
    T(s, [{ text: `En clair${NB}: `, options: { bold: true, color: C.lime } }, { text: 'vous réalisez les travaux, votre client bénéficie de la prime*, nous faisons le lien.' }],
      { x: M + 0.4, y: 5.92, w: CW - 0.8, h: 0.74, fontSize: 14.5, valign: 'middle', align: 'center' });
    T(s, NOTE, { x: M, y: 6.92, w: 8, h: 0.26, fontSize: 10.5, color: C.grey });
    pno(s);
  }

  // ================================================================ L'ACCOMPAGNEMENT
  section('Les six volets');

  // ---------- 5. Six volets (vue d'ensemble)
  {
    const s = newSlide(); s.background = { color: C.navyD };
    ring(s, 10.3, -4.4, 6.8, C.teal, 26, 75);
    kicker(s, 'Notre accompagnement', M, 0.65);
    title(s, [{ text: 'Six volets. ' }, { text: 'Un seul réseau.', options: { color: C.lime } }]);
    const V = [
      ['FaFileSignature', 'Dossiers CEE et primes*', 'Éligibilité, montage, vérification, suivi jusqu’au versement des primes*.'],
      ['FaFolderOpen', 'Démarches administratives', 'Nous vous épaulons sur l’administratif lié à vos chantiers aidés.'],
      ['FaChalkboardTeacher', 'Formation aux CEE', 'Les primes*, les pièces à fournir, les dossiers refusés à éviter.'],
      ['FaAward', 'Qualification RGE', 'Un accompagnement pour obtenir et conserver la qualification RGE.'],
      ['FaTags', 'Tarifs préférentiels fournisseurs', 'Des fournisseurs partenaires, à des conditions préférentielles.'],
      ['FaUsers', 'Un réseau', 'Un interlocuteur, des artisans comme vous, le lien avec les délégataires CEE.'],
    ];
    const g = 0.2, cw = (CW - 2 * g) / 3, ch = 2.12, y0 = 2.05;
    for (let i = 0; i < 6; i++) {
      const [ic, t, d] = V[i], x = M + (i % 3) * (cw + g), y = y0 + Math.floor(i / 3) * (ch + g), last = i === 5;
      rrect(s, x, y, cw, ch, last ? C.lime : C.navyL);
      disc(s, x + 0.28, y + 0.28, 0.74, last ? C.navyD : C.green);
      await ico(s, ic, last ? 'B9E35A' : 'FFFFFF', x + 0.5, y + 0.5, 0.3);
      T(s, '0' + (i + 1), { x: x + cw - 1.0, y: y + 0.3, w: 0.72, h: 0.4, fontSize: 22, bold: true, align: 'right', color: last ? C.navyD : C.lime });
      T(s, t, { x: x + 1.2, y: y + 0.28, w: cw - 2.15, h: 0.74, fontSize: 14.5, bold: true, valign: 'middle', color: last ? C.navyD : C.white, lineSpacingMultiple: 1.0 });
      T(s, d, { x: x + 0.28, y: y + 1.2, w: cw - 0.5, h: 0.8, fontSize: 12.5, color: last ? C.navyD : C.pale, lineSpacingMultiple: 1.2 });
    }
    T(s, NOTE, { x: M, y: 6.72, w: 8, h: 0.26, fontSize: 10.5, color: C.pale });
    pno(s);
  }

  // ---------- 6–11. Un volet par diapositive
  await volet(1, 'R', false, 'remise-dossier', { fx: 0.53, fy: 0.5 }, ['Dossiers CEE', 'et primes*'],
    'Le cœur de notre accompagnement. Vous réalisez les travaux, nous prenons en charge le dossier, du début à la fin.',
    ['Éligibilité étudiée selon vos travaux', 'Dossier monté et vérifié', 'Suivi jusqu’au versement\ndes primes*'], NOTE);
  await volet(2, 'L', true, 'portrait-conseillere', { fx: 0.4, fy: 0.5 }, ['Démarches', 'administratives'],
    'Pas seulement les CEE. Nous vous épaulons sur l’administratif lié à vos chantiers aidés.',
    ['Au-delà des seuls dossiers CEE', 'L’administratif de vos\nchantiers aidés', 'Un interlocuteur pour vous épauler']);
  await volet(3, 'R', false, 'formation', { fx: 0.55, fy: 0.5 }, ['Formation', 'aux CEE'],
    'Comprendre le dispositif pour ne plus le subir. Nous vous expliquons ce qu’il faut savoir.',
    ['Comment fonctionnent les primes*', 'Quelles pièces fournir', 'Comment éviter les dossiers refusés'], '* Primes versées sous réserve de validation du dossier.');
  await volet(4, 'L', true, 'qualification-rge', { fx: 0.65, fy: 0.5 }, ['Qualification', 'RGE'],
    'La qualification RGE s’obtient, puis se conserve. Nous vous accompagnons aux deux moments.',
    ['Un accompagnement pour l’obtenir', 'Un accompagnement pour\nla conserver', 'Vous n’êtes plus seul face\naux exigences RGE']);
  await volet(5, 'R', false, 'fournisseur', { fx: 0.45, fy: 0.5 }, ['Tarifs', 'préférentiels', 'fournisseurs'],
    'Nous vous mettons en relation avec des fournisseurs de matériel partenaires.',
    ['Des fournisseurs de matériel\npartenaires', 'Des conditions préférentielles', 'Vous n’êtes plus seul face aux prix']);
  await volet(6, 'L', true, 'reseau', { fx: 0.51, fy: 0.5 }, ['Un réseau'],
    'Vous ne travaillez plus seul dans votre coin. Vous rejoignez un réseau qui avance avec vous.',
    ['Un interlocuteur', 'Des artisans comme vous', 'Le lien avec les délégataires CEE']);

  // ================================================================ VOS DOSSIERS CEE
  section('Vos dossiers CEE');
  const SV = [
    ['Étude d’éligibilité', 'Identification des aides CEE mobilisables selon les travaux envisagés.'],
    ['Valorisation financière', 'Recherche des meilleures conditions de valorisation auprès de nos partenaires.'],
    ['Gestion administrative', 'Constitution, vérification et suivi des dossiers.'],
    ['Accompagnement réglementaire', `Vérification des exigences documentaires et des conditions du${NB}dispositif.`],
    ['Suivi du financement', `Coordination avec les délégataires jusqu’au traitement du dossier et au versement des${NB}primes*.`],
  ];

  // ---------- 12. Cinq étapes
  {
    const s = newSlide(); s.background = { color: C.navyD };
    ring(s, 10.3, -4.4, 6.8, C.teal, 26, 75);
    kicker(s, 'Vos dossiers CEE', M, 0.65);
    title(s, [{ text: 'Un dossier CEE, ' }, { text: 'cinq étapes.', options: { color: C.lime } }]);
    T(s, 'Vous réalisez les travaux. Nous nous occupons du dossier, étape par étape.', { x: M, y: 1.72, w: 10, h: 0.34, fontSize: 16, color: C.pale });
    const gap = 0.14, cw = (CW - 4 * gap) / 5, y0 = 3.05, ch = 3.3;
    SV.forEach(([t, d], i) => {
      const x = M + i * (cw + gap), last = i === 4, fg = last ? C.navyD : C.white;
      rrect(s, x, y0, cw, ch, last ? C.lime : C.navyL);
      disc(s, x + 0.18, y0 - 0.43, 0.86, last ? C.navyD : C.green);
      T(s, '0' + (i + 1), { x: x + 0.18, y: y0 - 0.43, w: 0.86, h: 0.86, fontSize: 20, bold: true, align: 'center', valign: 'middle', color: last ? C.lime : C.white });
      T(s, t, { x: x + 0.18, y: y0 + 0.66, w: cw - 0.3, h: 0.62, fontSize: 13, bold: true, color: fg, lineSpacingMultiple: 1.0 });
      T(s, d, { x: x + 0.18, y: y0 + 1.36, w: cw - 0.34, h: 1.85, fontSize: 13, color: last ? C.navyD : C.pale, lineSpacingMultiple: 1.2 });
    });
    T(s, NOTE, { x: M, y: 6.72, w: 8, h: 0.26, fontSize: 10.5, color: C.pale });
    pno(s);
  }

  // ---------- 13. Qui fait quoi
  {
    const s = newSlide(); s.background = { color: C.white };
    kicker(s, 'Répartition des rôles', M, 0.65, C.greenD);
    title(s, [{ text: 'Vous, sur le chantier.', options: { breakLine: true } }, { text: 'Nous, sur le dossier.', options: { color: C.green } }], C.navy, { h: 1.15 });
    const cols = [
      { t: 'Vous', k: 'Artisan RGE', li: ['Vous présentez les travaux envisagés', 'Vous réalisez les travaux', 'Vous restez concentré sur vos clients'] },
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
    pno(s);
  }

  // ================================================================ VOS SECTEURS
  section('Vos secteurs');

  // ---------- 14. Mosaïque
  {
    const s = newSlide(); s.background = { color: C.navyD };
    const tiles = [['pompe-a-chaleur', 'Pompes à chaleur', 0.48, 0.5], ['chauffage', 'Chauffage', 0.5, 0.5], ['isolation-combles', 'Isolation', 0.68, 0.5], ['renovation', 'Rénovation énergétique', 0.58, 0.5], ['tertiaire', 'Tertiaire', 0.5, 0.5], ['industrie', 'Industrie', 0.62, 0.5], ['agricole', 'Agricole', 0.62, 0.5]];
    const tw = W / 4, th = H / 2, g = 0.04, lb = 0.78;
    rect(s, 0, 0, tw - g, th - g, C.green);
    T(s, 'NOS TERRAINS', { x: 0.42, y: 0.5, w: tw - 0.7, h: 0.3, fontSize: 11, bold: true, charSpacing: 4, color: C.navyD });
    T(s, [{ text: 'Partout où', options: { breakLine: true } }, { text: 'il y a de', options: { breakLine: true } }, { text: 'l’énergie à', options: { breakLine: true } }, { text: 'économiser.' }], { x: 0.42, y: 0.95, w: tw - 0.6, h: 2.2, fontSize: 28, bold: true, lineSpacingMultiple: 1.0 });
    for (let i = 0; i < tiles.length; i++) {
      const [img, label, fx, fy] = tiles[i];
      const k = i + 1, x = (k % 4) * tw + (k % 4 ? g : 0), y = Math.floor(k / 4) * th + (k >= 4 ? g : 0);
      const w = tw - g, h = th - g;
      await pic(s, img, x, y, w, h - lb, { fx, fy });
      rect(s, x, y + h - lb, w, lb, k % 2 ? C.navy : C.navyL);
      T(s, label, { x: x + 0.3, y: y + h - lb, w: w - 0.5, h: lb, fontSize: 16, bold: true, valign: 'middle' });
    }
  }

  // ---------- 15. Quatre secteurs, les professionnels concernés
  {
    const s = newSlide(); s.background = { color: C.mist };
    kicker(s, 'Secteurs d’intervention', M, 0.65, C.greenD);
    title(s, 'Quatre secteurs, les professionnels concernés', C.navy);
    const SE = [
      ['isolation-combles', 0.6, 'Résidentiel', ['Installateurs de pompes à chaleur et de systèmes de chauffage', 'Entreprises d’isolation et de rénovation énergétique', 'Professionnels de la ventilation']],
      ['tertiaire', 0.5, 'Tertiaire', ['Entreprises intervenant dans le secteur tertiaire', 'Professionnels de la ventilation et des équipements thermiques', 'Installateurs de systèmes de chauffage']],
      ['industrie', 0.6, 'Industrie', ['Entreprises intervenant dans le secteur industriel', 'Professionnels des équipements thermiques', 'Professionnels de la ventilation']],
      ['agricole', 0.55, 'Agricole', ['Entreprises intervenant dans le secteur agricole', 'Professionnels des équipements thermiques', 'Installateurs de systèmes de chauffage']],
    ];
    const g = 0.22, cw = (CW - 3 * g) / 4, y0 = 1.95, ch = 4.78, ph = 1.4;
    const tw = cw - 0.74;
    const rowH = [0.7, 0.92, 0.48]; // 3, 4 et 2 lignes au plus (vérifié au rendu)
    for (let i = 0; i < 4; i++) {
      const [img, fx, word, items] = SE[i], x = M + i * (cw + g);
      rrect(s, x, y0, cw, ch, C.white, 0.16, { shadow: softShadow() });
      await pic(s, img, x, y0, cw, ph, { fx, fy: 0.5, r: [0.16, 0.16, 0, 0], bg: C.mist });
      T(s, word, { x: x + 0.26, y: y0 + ph + 0.22, w: cw - 0.4, h: 0.42, fontSize: 20, bold: true, color: C.navy });
      let y = y0 + ph + 0.76;
      items.forEach((it, r) => {
        const h = rowH[r];
        disc(s, x + 0.26, y + 0.06, 0.12, C.green);
        T(s, it, { x: x + 0.52, y, w: tw, h, fontSize: 12, color: C.grey, lineSpacingMultiple: 1.12 });
        y += h + 0.16;
      });
    }
    pno(s);
  }

  // ================================================================ POURQUOI NOUS REJOINDRE
  section('Pourquoi nous rejoindre');

  // ---------- 16. Seul / avec le réseau
  {
    const s = newSlide(); s.background = { color: C.white };
    rect(s, W / 2, 0, W / 2, H, C.navy);
    T(s, 'SEUL', { x: M, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: '6F819B' });
    T(s, 'Vous portez tout.', { x: M, y: 1.2, w: 5.4, h: 0.7, fontSize: 26, bold: true, color: C.navy });
    T(s, 'AVEC CERCLE ÉNERGIE', { x: W / 2 + 0.85, y: 0.8, w: 5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: C.lime });
    T(s, 'Vous avancez en réseau.', { x: W / 2 + 0.85, y: 1.2, w: 5.0, h: 0.7, fontSize: 26, bold: true });
    const rows = [
      ['Dossiers CEE à monter\net à suivre vous-même', 'Dossiers CEE montés,\nvérifiés et suivis'],
      ['Administratif des chantiers\naidés à gérer seul', 'Un appui sur vos démarches\nadministratives'],
      ['Règles des CEE et exigences\nRGE à maîtriser seul', 'Formation aux CEE,\naccompagnement RGE'],
      ['Matériel à négocier seul\nauprès des fournisseurs', 'Fournisseurs partenaires,\nconditions préférentielles'],
    ];
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
    pno(s);
  }

  // ---------- 17. FAQ
  const cardX = (k) => M + k * (3.76 + 0.275);
  {
    const s = newSlide(); s.background = { color: C.mist };
    kicker(s, 'Questions fréquentes', M, 0.65, C.greenD);
    title(s, 'Vos questions, nos réponses', C.navy);
    const qa = [
      [`Qu’est-ce qu’un mandataire CEE${NB}?`, 'Un intermédiaire qui fait le lien entre les artisans et les délégataires CEE, et qui prend en charge l’administratif. C’est le rôle de Cercle Énergie.'],
      [`Cercle Énergie, c’est seulement les dossiers CEE${NB}?`, `Non. Les dossiers CEE restent le cœur. S’y ajoutent${NB}: les démarches administratives, la formation aux CEE, la qualification RGE, les tarifs préférentiels fournisseurs et le réseau.`],
      [`Le versement des primes est-il garanti${NB}?`, `Non. Le versement des primes intervient sous réserve de validation du dossier. Notre rôle${NB}: monter, vérifier et suivre votre dossier, en lien avec les délégataires.`],
    ];
    qa.forEach(([q, a], i) => {
      const x = cardX(i), y0 = 2.05, w = 3.76, h = 4.75, hi = i === 2;
      rrect(s, x, y0, w, h, hi ? C.navyD : C.white, 0.16, { shadow: softShadow() });
      disc(s, x + 0.32, y0 + 0.32, 0.7, hi ? C.lime : C.green);
      T(s, '?', { x: x + 0.32, y: y0 + 0.32, w: 0.7, h: 0.7, fontSize: 22, bold: true, align: 'center', valign: 'middle', color: hi ? C.navyD : C.white });
      T(s, q, { x: x + 0.32, y: y0 + 1.25, w: w - 0.6, h: 0.95, fontSize: 17, bold: true, color: hi ? C.white : C.navy, lineSpacingMultiple: 1.0 });
      T(s, a, { x: x + 0.32, y: y0 + 2.35, w: w - 0.62, h: 2.2, fontSize: 13.5, color: hi ? C.pale : C.grey, lineSpacingMultiple: 1.25 });
    });
    pno(s);
  }

  // ================================================================ REJOINDRE LE RÉSEAU
  section('Rejoindre le réseau');

  // ---------- 18. Rejoindre le réseau, en pratique
  {
    const s = newSlide(); s.background = { color: C.navyD };
    await pic(s, 'equipe', W / 2, 0, W / 2, H, { fx: 0.545, fy: 0.5 });
    ring(s, -4.3, 5.6, 6.2, C.teal, 26, 72);
    kicker(s, 'Rejoindre le réseau', M, 0.7);
    T(s, [{ text: 'Un échange,', options: { breakLine: true } }, { text: 'et vous n’êtes', options: { color: C.lime, breakLine: true } }, { text: 'plus seul.', options: { color: C.lime } }], { x: M, y: 1.08, w: 5.5, h: 1.4, fontSize: 30, bold: true, lineSpacingMultiple: 0.98 });
    const st = [
      ['Vous prenez contact', 'Présentez-nous votre activité et vos chantiers.'],
      ['Nous faisons le point', 'Nous voyons ensemble où vous avez besoin d’aide.'],
      ['Nous lançons vos dossiers CEE', 'Éligibilité, montage, vérification, suivi.'],
      ['Vous avancez avec le réseau', 'Administratif, formation, RGE, fournisseurs.'],
    ];
    st.forEach(([t, d], i) => {
      const y = 2.85 + i * 1.0;
      disc(s, M, y, 0.64, C.green);
      T(s, String(i + 1), { x: M, y, w: 0.64, h: 0.64, fontSize: 18, bold: true, align: 'center', valign: 'middle' });
      T(s, t, { x: M + 0.9, y: y - 0.02, w: 4.6, h: 0.32, fontSize: 16, bold: true });
      T(s, d, { x: M + 0.9, y: y + 0.33, w: 4.6, h: 0.5, fontSize: 13, color: C.pale, lineSpacingMultiple: 1.1 });
    });
    pno(s);
  }

  // ---------- 19. Message clé
  {
    const s = newSlide();
    await pic(s, 'artisan-clients', 0, 0, W, H, { fx: 0.5, fy: 0.5 });
    s.addImage({ path: OV.bottom, x: 0, y: 0, w: W, h: H });
    kicker(s, 'Notre message', M, 4.55);
    T(s, [{ text: `«${NB}Vous réalisez les travaux. `, options: {} }, { text: `Pour ce que vous n’arrivez pas à faire seul, il y a le réseau Cercle${NB}Énergie.${NB}»`, options: { color: C.lime } }],
      { x: M, y: 4.98, w: 11.0, h: 1.75, fontSize: 31, bold: true, lineSpacingMultiple: 1.0 });
    pno(s);
  }

  // ---------- 20. Clôture
  {
    const s = newSlide(); s.background = { color: C.green };
    ring(s, 10.6, -3.9, 8.4, C.white, 40, 78); ring(s, -3.4, 5.0, 7.0, C.navy, 34, 80);
    logoPill(s, M, 0.6, 2.5, 'logo_full.png');
    T(s, 'Rejoindre le réseau', { x: M, y: 2.75, w: CW, h: 1.2, fontSize: 64, bold: true });
    T(s, [{ text: 'Cercle Énergie, le partenaire unique de vos projets.', options: { breakLine: true } }, { text: 'Ce que vous n’arrivez pas à faire seul, on vous aide à le faire.' }], { x: M, y: 4.2, w: CW, h: 1.0, fontSize: 20, bold: true, color: C.navyD, lineSpacingMultiple: 1.2 });
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
