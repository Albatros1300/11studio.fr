/**
 * Cercle Énergie — Plaquette de présentation (PowerPoint 16:9)
 *
 * Usage :
 *   npm install pptxgenjs sharp react react-dom react-icons      (une fois, où vous voulez ; voir NODE_PATH)
 *   node build_plaquette.js
 *
 * Variables d'environnement facultatives :
 *   CE_FONT        police déclarée (défaut : Montserrat). Ex. CE_FONT=Arial pour tester le rendu de secours.
 *   CE_OUT         chemin du fichier de sortie (défaut : Cercle-Energie-Plaquette.pptx à côté du script).
 *   PPTX_SKILL_DIR dossier contenant scripts/apply_theme.js (écrit les couleurs du thème dans le fichier).
 */
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const lu = require("react-icons/lu");

const IMG = path.resolve(__dirname, "../site/assets/img");
const OUT = process.env.CE_OUT || path.join(__dirname, "Cercle-Energie-Plaquette.pptx");
const FONT = process.env.CE_FONT || "Montserrat";
const SKILL = process.env.PPTX_SKILL_DIR ||
  "/root/.claude/skills/synced/9284eb0f-0704-4ce8-9ff2-3102e52fd872_b7db30cf-bf43-42d0-96b5-f4d3362fc892/pptx";

const HEX = { navy: "0B3566", green: "73AF01", blue: "016CB4", teal: "01B7BA", tint: "F1F6FB", grey: "40577A", rule: "D5E0EC", white: "FFFFFF" };
const THEME = {
  name: "Cercle Énergie",
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: HEX.navy, lt1: HEX.white, dk2: HEX.grey, lt2: HEX.tint,
    accent1: HEX.green, accent2: HEX.blue, accent3: HEX.teal, accent4: HEX.navy, accent5: HEX.rule, accent6: HEX.grey,
    hlink: HEX.blue, folHlink: HEX.grey,
  },
};

const W = 13.333, H = 7.5, M = 0.6, CW = W - 2 * M; // grille : marges 0,6", zone utile 12,13"
const TOP = 1.85, BOTTOM = 6.55;                     // zone de contenu des pages intérieures

// ---------- helpers images ----------
/** Recadre une photo 1600x900 : plage horizontale [rx0, rx1] (0..1), ratio cible l/h, biais vertical 0..1. */
async function crop(name, rx0, rx1, ratio, yBias = 0.5) {
  const file = path.join(IMG, name + ".jpg");
  const meta = await sharp(file).metadata();
  let w = (rx1 - rx0) * meta.width, h = w / ratio, left = rx0 * meta.width;
  if (h > meta.height) { h = meta.height; const w2 = h * ratio; left += (w - w2) / 2; w = w2; }
  const top = (meta.height - h) * yBias;
  const buf = await sharp(file)
    .extract({ left: Math.round(left), top: Math.round(top), width: Math.floor(w), height: Math.floor(h) })
    .jpeg({ quality: 88 }).toBuffer();
  return "image/jpeg;base64," + buf.toString("base64");
}
async function icon(name, color) {
  const Comp = lu[name];
  if (!Comp) throw new Error("Icône introuvable : " + name);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { size: 256, color: "#" + color }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "Cercle Énergie — Plaquette de présentation";
  pres.author = "Cercle Énergie";
  pres.company = "Cercle Énergie";
  pres.subject = "Plaquette de présentation à destination des professionnels de la rénovation énergétique";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const NAVY = C.text1, GREY = C.text2, WHITE = C.background1, TINT = C.background2;
  const GREEN = C.accent1, BLUE = C.accent2, RULE = C.accent5;

  const LOGO_MARK = path.join(IMG, "logo_mark_t.png"); // 1090 x 760
  const LOGO_FULL = path.join(IMG, "logo_full_t.png"); // 1356 x 870
  const logoMark = (h) => ({ w: h * 1090 / 760, h });
  const logoFull = (w) => ({ w, h: w * 870 / 1356 });

  // ---------- gabarits (layouts) ----------
  const pageNumber = { x: W - M - 0.8, y: 6.9, w: 0.8, h: 0.3, fontSize: 10, color: GREY, align: "right", valign: "middle", margin: 0 };
  const sourcePh = { placeholder: { options: { name: "source", type: "body", x: M, y: 6.9, w: 10.5, h: 0.3, fontSize: 10, color: GREY, valign: "middle", margin: 0 }, text: "Note / source" } };
  const smallLogo = { image: { path: LOGO_MARK, x: W - M - logoMark(0.66).w, y: 0.4, ...logoMark(0.66), altText: "Logo Cercle Énergie" } };

  pres.defineSlideMaster({
    title: "Couverture", background: { color: WHITE },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 3.3, w: 5.3, h: 1.75, fontSize: 28, bold: true, color: NAVY, align: "left", valign: "top", margin: 0 }, text: "Titre" } },
    ],
  });
  pres.defineSlideMaster({
    title: "Contenu", background: { color: WHITE },
    objects: [
      smallLogo,
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: 10.7, h: 1.0, fontSize: 22, bold: true, color: NAVY, align: "left", valign: "top", margin: 0 }, text: "Titre-message" } },
      sourcePh,
    ],
    slideNumber: { ...pageNumber },
  });
  pres.defineSlideMaster({
    title: "Message", background: { color: TINT },
    objects: [
      smallLogo,
      { placeholder: { options: { name: "title", type: "title", x: 5.8, y: 2.05, w: 6.9, h: 3.2, fontSize: 28, bold: true, color: NAVY, align: "left", valign: "top", margin: 0 }, text: "Message clé" } },
    ],
    slideNumber: { ...pageNumber },
  });
  pres.defineSlideMaster({
    title: "Cloture", background: { color: WHITE },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 2.3, w: 7.0, h: 1.25, fontSize: 32, bold: true, color: NAVY, align: "left", valign: "top", margin: 0 }, text: "Appel à l'action" } },
    ],
    slideNumber: { ...pageNumber, x: M, align: "left" },
  });

  // ---------- helpers de composition ----------
  const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, valign: "top", color: GREY, fontSize: 14, ...o });
  const box = (s, x, y, w, h, color, name) => s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color }, objectName: name });
  const hair = (s, x, y, w) => s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color: RULE, width: 1 } });
  const num = (s, n, x, y, d, o = {}) => s.addText(String(n), {
    shape: pres.ShapeType.ellipse, x, y, w: d, h: d, fill: { color: o.fill || NAVY }, color: o.color || WHITE,
    bold: true, fontSize: o.fontSize || 16, align: "center", valign: "middle", margin: 0, objectName: "Numéro " + n,
  });
  const iconCircle = async (s, name, x, y, d, fill, hex) => {
    s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: fill } });
    s.addImage({ data: await icon(name, hex), x: x + d * 0.25, y: y + d * 0.25, w: d * 0.5, h: d * 0.5 });
  };
  const photo = async (s, name, rx0, rx1, x, y, w, h, alt, yBias) =>
    s.addImage({ data: await crop(name, rx0, rx1, w / h, yBias), x, y, w, h, altText: alt });
  const bullets = (items, o = {}) => items.map((t, i) => ({
    text: t, options: { bullet: { indent: 14 }, breakLine: i < items.length - 1, paraSpaceAfter: o.space ?? 6, ...(o.run || {}) },
  }));
  const content = (section, title, source) => {
    const s = pres.addSlide({ masterName: "Contenu", sectionTitle: section });
    s.addText(title, { placeholder: "title" });
    if (source) s.addText(source, { placeholder: "source" });
    return s;
  };
  const CAVEAT = "Note : le versement des primes CEE intervient sous réserve de validation du dossier.";
  const CEE = "CEE : Certificats d'Économies d'Énergie.";

  const S1 = "Ouverture", S2 = "Qui nous sommes", S3 = "Notre accompagnement", S4 = "Devenir partenaire";

  // ===== 1. Couverture =====
  pres.addSection({ title: S1 });
  {
    const s = pres.addSlide({ masterName: "Couverture", sectionTitle: S1 });
    await photo(s, "artisan-clients", 0.46, 1.0, 6.2, 0, W - 6.2, H, "Un artisan serre la main de ses clients devant une pompe à chaleur");
    s.addImage({ path: LOGO_FULL, x: M, y: 0.6, ...logoFull(2.6), altText: "Logo Cercle Énergie — Le partenaire unique de vos projets" });
    T(s, "PLAQUETTE DE PRÉSENTATION", { x: M, y: 2.8, w: 5.3, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 2 });
    s.addText("Le partenaire CEE des professionnels de la rénovation énergétique", { placeholder: "title" });
    T(s, "Accompagnement et valorisation des Certificats d'Économies d'Énergie (CEE) pour les artisans, installateurs et entreprises du bâtiment.",
      { x: M, y: 5.3, w: 5.0, h: 1.3, fontSize: 14 });
  }

  // ===== 2. Synthèse =====
  {
    const s = content(S1, "En bref : concentrez-vous sur vos chantiers, Cercle Énergie vous accompagne sur vos dossiers CEE", CEE);
    const cards = [
      ["Le constat", "Les aides CEE contribuent à financer vos projets, mais leurs démarches administratives sont lourdes à constituer, vérifier et suivre."],
      ["Qui nous sommes", "Une société spécialisée dans l'accompagnement et la valorisation des CEE. Mandataire, elle travaille en collaboration avec des délégataires CEE."],
      ["Cinq services", "Étude d'éligibilité, valorisation financière, gestion administrative, accompagnement réglementaire et suivi du financement."],
      ["Ce que vous y gagnez", "Des démarches simplifiées, des dossiers sécurisés et des projets valorisés : vous restez concentré sur votre métier."],
    ];
    const gap = 0.3, cw = (CW - gap) / 2, ch = (BOTTOM - TOP - gap) / 2;
    cards.forEach(([label, text], i) => {
      const x = M + (i % 2) * (cw + gap), y = TOP + Math.floor(i / 2) * (ch + gap);
      box(s, x, y, cw, ch, TINT, "Carte " + (i + 1));
      num(s, i + 1, x + 0.35, y + 0.35, 0.55);
      T(s, label, { x: x + 1.15, y: y + 0.35, w: cw - 1.5, h: 0.55, fontSize: 17, bold: true, color: NAVY, valign: "middle" });
      T(s, text, { x: x + 1.15, y: y + 1.0, w: cw - 1.5, h: ch - 1.2 });
    });
  }

  // ===== 3. Le problème =====
  pres.addSection({ title: S2 });
  {
    const s = content(S2, "Les aides CEE sont une opportunité pour vos chantiers, mais leur gestion administrative est lourde", CEE);
    await photo(s, "paperasse", 0.13, 0.65, M, TOP, 4.2, BOTTOM - TOP, "Un artisan submergé par des piles de dossiers");
    const x = 5.3, w = W - M - x;
    await iconCircle(s, "LuSprout", x, TOP, 0.55, GREEN, HEX.white);
    T(s, "L'opportunité", { x: x + 0.8, y: TOP, w: w - 0.8, h: 0.55, fontSize: 17, bold: true, color: NAVY, valign: "middle" });
    T(s, "Les Certificats d'Économies d'Énergie (CEE) contribuent au financement des projets de rénovation et d'efficacité énergétique.",
      { x: x + 0.8, y: TOP + 0.65, w: w - 0.8, h: 0.6 });
    hair(s, x, 3.35, w);
    await iconCircle(s, "LuFiles", x, 3.6, 0.55, NAVY, HEX.white);
    T(s, "La contrainte : des démarches pour chaque dossier", { x: x + 0.8, y: 3.6, w: w - 0.8, h: 0.55, fontSize: 17, bold: true, color: NAVY, valign: "middle" });
    T(s, bullets([
      "Identifier les aides CEE mobilisables selon les travaux",
      "Rechercher de bonnes conditions de valorisation",
      "Constituer, vérifier et suivre le dossier",
      "Respecter les exigences documentaires et les conditions du dispositif",
      "Se coordonner avec les acteurs du financement CEE",
    ], { space: 4 }), { x: x + 0.8, y: 4.25, w: w - 0.8, h: 1.75 });
    T(s, "Autant de temps qui n'est pas consacré à votre métier.", { x: x + 0.8, y: 6.15, w: w - 0.8, h: 0.4, bold: true, color: NAVY, valign: "middle" });
  }

  // ===== 4. Qui est Cercle Énergie =====
  {
    const s = content(S2, "Cercle Énergie est une société spécialisée dans l'accompagnement et la valorisation des CEE", CEE);
    const rows = [
      ["Notre spécialité", "L'accompagnement et la valorisation des Certificats d'Économies d'Énergie (CEE).", 0.7],
      ["Notre statut", "Mandataire, Cercle Énergie travaille en collaboration avec des délégataires CEE pour aider les professionnels à financer leurs projets de rénovation et d'efficacité énergétique.", 1.15],
      ["Notre rôle", "Mettre en relation les entreprises d'installation avec les acteurs du financement CEE, tout en simplifiant l'ensemble des démarches administratives.", 1.15],
    ];
    const lw = 7.5; let y = TOP;
    rows.forEach(([label, text, h], i) => {
      if (i) { y += 0.2; hair(s, M, y, lw); y += 0.2; }
      T(s, label, { x: M, y, w: 2.1, h: 0.4, fontSize: 15, bold: true, color: NAVY });
      T(s, text, { x: M + 2.3, y, w: lw - 2.3, h });
      y += h;
    });
    box(s, M, 5.8, lw, 0.75, TINT, "Objectif");
    T(s, [
      { text: "Notre objectif : ", options: { bold: true, color: NAVY } },
      { text: "vous permettre de vous concentrer sur votre métier.", options: { color: NAVY } },
    ], { x: M + 0.3, y: 5.8, w: lw - 0.6, h: 0.75, valign: "middle" });
    await photo(s, "equipe", 0.42, 1.0, 8.5, TOP, W - M - 8.5, BOTTOM - TOP, "L'équipe travaille sur un dossier autour d'une table");
  }

  // ===== 5. Chaîne de valeur =====
  {
    const s = content(S2, "Cercle Énergie fait le lien entre les entreprises d'installation et les acteurs du financement CEE", CAVEAT);
    const cw = 3.4, ch = 3.55, gap = (CW - 3 * cw) / 2, y = TOP, pad = 0.25, aw = 0.6;
    const nodes = [
      ["LuWrench", "Installateurs & artisans", "Vous réalisez les travaux", "Pompes à chaleur, chauffage, isolation, ventilation, rénovation énergétique."],
      ["LuHandshake", "Cercle Énergie", "Mandataire CEE", "Vous accompagne et simplifie l'ensemble des démarches administratives."],
      ["LuLandmark", "Délégataires CEE", "Acteurs du financement CEE", "Traitement des dossiers et versement des primes, sous réserve de validation du dossier."],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, title, sub, text] = nodes[i], x = M + i * (cw + gap), mid = i === 1;
      box(s, x, y, cw, ch, mid ? NAVY : TINT, "Acteur " + (i + 1));
      await iconCircle(s, ic, x + pad, y + 0.3, 0.7, mid ? GREEN : NAVY, HEX.white);
      T(s, title, { x: x + pad, y: y + 1.2, w: cw - 2 * pad, h: 0.4, fontSize: 15, bold: true, color: mid ? WHITE : NAVY });
      T(s, sub, { x: x + pad, y: y + 1.62, w: cw - 2 * pad, h: 0.3, fontSize: 12, bold: true, color: mid ? GREEN : BLUE });
      T(s, text, { x: x + pad, y: y + 2.1, w: cw - 2 * pad, h: ch - 2.3, color: mid ? WHITE : GREY });
      if (i < 2) s.addShape(pres.ShapeType.leftRightArrow, { x: x + cw + (gap - aw) / 2, y: y + ch / 2 - 0.18, w: aw, h: 0.36, fill: { color: GREEN }, objectName: "Lien " + (i + 1) });
    }
    T(s, [
      { text: "Un partenaire unique : ", options: { bold: true, color: NAVY } },
      { text: "Cercle Énergie met en relation votre entreprise et les acteurs du financement CEE, et simplifie vos démarches.", options: {} },
    ], { x: M, y: 5.7, w: CW, h: 0.85, valign: "middle" });
  }

  // ===== 6. Métiers et secteurs =====
  {
    const s = content(S2, "Nous accompagnons les métiers de la rénovation énergétique dans quatre secteurs d'activité");
    T(s, "Vos métiers", { x: M, y: TOP, w: 3.2, h: 0.4, fontSize: 17, bold: true, color: NAVY });
    T(s, bullets(["Pompes à chaleur et systèmes de chauffage", "Isolation et rénovation énergétique", "Ventilation et équipements thermiques"]),
      { x: M, y: TOP + 0.5, w: 3.2, h: 1.9 });
    hair(s, M, 4.25, 3.2);
    T(s, "Vos secteurs", { x: M, y: 4.45, w: 3.2, h: 0.4, fontSize: 17, bold: true, color: NAVY });
    T(s, bullets(["Résidentiel", "Tertiaire", "Industriel", "Agricole"], { space: 4 }), { x: M, y: 4.95, w: 3.2, h: 1.6 });
    const tiles = [
      ["pac-installation", "PAC & chauffage", "Installation d'une pompe à chaleur", 0.2, 1.0],
      ["isolation-combles", "Isolation", "Pose d'isolant en combles", 0, 1],
      ["renovation", "Rénovation énergétique", "Pose d'une fenêtre en rénovation", 0, 1],
      ["tertiaire", "Tertiaire", "Immeuble de bureaux", 0, 1],
      ["industrie", "Industrie", "Technicien dans un site industriel", 0, 0.9],
      ["agricole", "Agricole", "Serre et bâtiment agricole", 0, 1],
    ];
    const gx = 4.3, gap = 0.2, tw = (W - M - gx - 2 * gap) / 3, th = 1.8;
    for (let i = 0; i < 6; i++) {
      const [img, label, alt, a, b] = tiles[i];
      const x = gx + (i % 3) * (tw + gap), y = TOP + Math.floor(i / 3) * 2.4;
      await photo(s, img, a, b, x, y, tw, th, alt);
      T(s, label, { x, y: y + th + 0.08, w: tw, h: 0.32, fontSize: 13, bold: true, color: NAVY, valign: "middle" });
    }
  }

  // ===== 7. Les cinq services =====
  pres.addSection({ title: S3 });
  {
    const s = content(S3, "Cinq services couvrent tout le cycle de votre dossier CEE, de l'éligibilité au suivi du financement", CAVEAT);
    const steps = [
      ["Étude d'éligibilité", "Identification des aides CEE mobilisables selon les travaux envisagés."],
      ["Valorisation financière", "Recherche des meilleures conditions de valorisation auprès de nos partenaires."],
      ["Gestion administrative", "Constitution, vérification et suivi des dossiers."],
      ["Accompagnement réglementaire", "Vérification des exigences documentaires et des conditions du dispositif."],
      ["Suivi du financement", "Coordination avec les délégataires jusqu'au traitement du dossier et au versement des primes, sous réserve de validation."],
    ];
    const gap = 0.28, cw = (CW - 4 * gap) / 5, d = 0.72, y = 2.0;
    s.addShape(pres.ShapeType.line, { x: M + d, y: y + d / 2, w: 4 * (cw + gap) - d, h: 0, line: { color: RULE, width: 2 } });
    steps.forEach(([title, text], i) => {
      const x = M + i * (cw + gap);
      num(s, i + 1, x, y, d, { fontSize: 20 });
      T(s, title, { x, y: 3.0, w: cw, h: 0.75, fontSize: 15, bold: true, color: NAVY });
      T(s, text, { x, y: 3.8, w: cw, h: 1.75 });
    });
    box(s, M, 5.75, CW, 0.8, TINT, "Résultat");
    T(s, [
      { text: "Résultat : ", options: { bold: true, color: NAVY } },
      { text: "vous vous concentrez sur votre métier, Cercle Énergie vous accompagne dans la gestion et le financement de vos dossiers CEE.", options: { color: NAVY } },
    ], { x: M + 0.3, y: 5.75, w: CW - 0.6, h: 0.8, valign: "middle" });
  }

  // ===== 8. Qui fait quoi =====
  {
    const s = content(S3, "Une répartition claire des rôles vous permet de rester concentré sur votre métier", CAVEAT);
    const gap = 0.26, w1 = 3.5, w2 = CW - 2 * w1 - 2 * gap, h = BOTTOM - TOP;
    const cols = [
      [M, w1, "Vous", "Installateurs & artisans", ["Vous présentez les travaux envisagés", "Vous réalisez les travaux", "Vous restez concentré sur votre métier"]],
      [M + w1 + gap, w2, "Cercle Énergie", "Mandataire CEE", [
        "Identifie les aides CEE mobilisables",
        "Recherche les meilleures conditions de valorisation auprès de ses partenaires",
        "Constitue, vérifie et suit les dossiers",
        "Vérifie les exigences documentaires et les conditions du dispositif",
        "Coordonne avec les délégataires jusqu'au traitement du dossier"]],
      [M + w1 + gap + w2 + gap, w1, "Délégataire CEE", "Acteur du financement CEE", ["Collabore avec Cercle Énergie", "Traitement du dossier", "Versement des primes, sous réserve de validation du dossier"]],
    ];
    cols.forEach(([x, w, title, sub, items], i) => {
      const mid = i === 1;
      box(s, x, TOP, w, h, mid ? NAVY : TINT, "Rôle " + (i + 1));
      T(s, title, { x: x + 0.3, y: TOP + 0.3, w: w - 0.6, h: 0.4, fontSize: 18, bold: true, color: mid ? WHITE : NAVY });
      T(s, sub, { x: x + 0.3, y: TOP + 0.72, w: w - 0.6, h: 0.3, fontSize: 12, bold: true, color: mid ? GREEN : BLUE });
      T(s, bullets(items, { space: 8 }), { x: x + 0.3, y: TOP + 1.3, w: w - 0.6, h: h - 1.5, color: mid ? WHITE : GREY });
    });
  }

  // ===== 9. Bénéfices =====
  {
    const s = content(S3, "Trois bénéfices pour votre entreprise : simplifier, sécuriser et valoriser vos projets");
    const x1 = M, w1 = 2.7, x2 = 3.5, w2 = 4.75, x3 = 8.55, w3 = W - M - x3;
    T(s, "CE QUE FAIT CERCLE ÉNERGIE", { x: x2, y: TOP, w: w2, h: 0.3, fontSize: 11, bold: true, color: BLUE, charSpacing: 1, valign: "middle" });
    T(s, "CE QUE VOUS Y GAGNEZ", { x: x3, y: TOP, w: w3, h: 0.3, fontSize: 11, bold: true, color: BLUE, charSpacing: 1, valign: "middle" });
    const rows = [
      ["LuListChecks", "Simplifier", "Constitution, vérification et suivi de vos dossiers ; coordination avec les délégataires.", "Un partenaire unique pour vos démarches CEE : vous restez concentré sur votre métier."],
      ["LuShieldCheck", "Sécuriser", "Vérification des exigences documentaires et des conditions du dispositif.", "Des dossiers vérifiés et suivis jusqu'à leur traitement."],
      ["LuTrendingUp", "Valoriser", "Identification des aides CEE mobilisables et recherche des meilleures conditions de valorisation auprès de nos partenaires.", "Un financement CEE recherché aux meilleures conditions pour vos projets."],
    ];
    const rh = 1.3, y0 = TOP + 0.45, pitch = (BOTTOM - y0 - rh) / 2;
    for (let i = 0; i < 3; i++) {
      const [ic, verb, does, gain] = rows[i], y = y0 + i * pitch;
      box(s, M, y, CW, rh, TINT, "Bénéfice " + (i + 1));
      await iconCircle(s, ic, x1 + 0.25, y + (rh - 0.6) / 2, 0.6, GREEN, HEX.white);
      T(s, verb, { x: x1 + 1.05, y, w: w1 - 1.05, h: rh, fontSize: 18, bold: true, color: NAVY, valign: "middle" });
      T(s, does, { x: x2, y, w: w2 - 0.3, h: rh, valign: "middle" });
      T(s, gain, { x: x3, y, w: w3 - 0.3, h: rh, valign: "middle", color: NAVY, bold: true });
    }
  }

  // ===== 10. Avant / après =====
  {
    const s = content(S3, "Avec Cercle Énergie, la gestion de vos aides CEE ne repose plus sur vos seules équipes");
    const x1 = M, w1 = 2.6, x2 = 3.4, w2 = 4.2, x3 = 8.3, w3 = W - M - x3;
    T(s, "SANS ACCOMPAGNEMENT", { x: x2 + 0.3, y: TOP, w: w2 - 0.3, h: 0.3, fontSize: 11, bold: true, color: GREY, charSpacing: 1, valign: "middle" });
    T(s, "AVEC CERCLE ÉNERGIE", { x: x3 + 0.3, y: TOP, w: w3 - 0.3, h: 0.3, fontSize: 11, bold: true, color: BLUE, charSpacing: 1, valign: "middle" });
    const rows = [
      ["Aides mobilisables", "À identifier par vos soins, selon chaque chantier", "Identifiées selon les travaux envisagés"],
      ["Dossiers", "À constituer, vérifier et suivre en interne", "Constitués, vérifiés et suivis par Cercle Énergie"],
      ["Exigences du dispositif", "À maîtriser et à contrôler seul", "Exigences documentaires et conditions vérifiées"],
      ["Financement", "Acteurs du financement à identifier et à coordonner", "Un partenaire unique, en lien avec les délégataires"],
    ];
    const y0 = TOP + 0.45, gap = 0.12, rh = (BOTTOM - y0 - 3 * gap) / 4;
    rows.forEach(([topic, before, after], i) => {
      const y = y0 + i * (rh + gap);
      T(s, topic, { x: x1, y, w: w1, h: rh, fontSize: 15, bold: true, color: NAVY, valign: "middle" });
      box(s, x2, y, w2, rh, TINT, "Sans " + (i + 1));
      T(s, before, { x: x2 + 0.3, y, w: w2 - 0.6, h: rh, valign: "middle" });
      s.addShape(pres.ShapeType.rightArrow, { x: x2 + w2 + (x3 - x2 - w2 - 0.4) / 2, y: y + rh / 2 - 0.15, w: 0.4, h: 0.3, fill: { color: GREEN }, objectName: "Flèche " + (i + 1) });
      box(s, x3, y, w3, rh, NAVY, "Avec " + (i + 1));
      T(s, after, { x: x3 + 0.3, y, w: w3 - 0.6, h: rh, valign: "middle", color: WHITE, bold: true });
    });
  }

  // ===== 11. Démarrer un partenariat =====
  pres.addSection({ title: S4 });
  {
    const s = content(S4, "Démarrer un partenariat avec Cercle Énergie se fait en quatre étapes simples", CAVEAT);
    await photo(s, "dossier", 0.33, 0.80, M, TOP, 3.9, BOTTOM - TOP, "Une main complète un dossier au stylo");
    const steps = [
      ["Vous prenez contact", "Présentez-nous votre activité et les travaux que vous envisagez."],
      ["Nous étudions l'éligibilité", "Nous identifions les aides CEE mobilisables selon vos travaux."],
      ["Nous constituons le dossier", "Nous le constituons, le vérifions et en assurons le suivi."],
      ["Nous suivons le financement", "Nous coordonnons avec les délégataires jusqu'au versement des primes, sous réserve de validation du dossier."],
    ];
    const x = 5.1, d = 0.6, pitch = 1.2, tx = x + d + 0.35;
    s.addShape(pres.ShapeType.line, { x: x + d / 2, y: TOP + d, w: 0, h: 3 * pitch - d, line: { color: RULE, width: 2 } });
    steps.forEach(([title, text], i) => {
      const y = TOP + i * pitch;
      num(s, i + 1, x, y, d);
      T(s, title, { x: tx, y, w: W - M - tx, h: 0.4, fontSize: 17, bold: true, color: NAVY, valign: "middle" });
      T(s, text, { x: tx, y: y + 0.45, w: W - M - tx, h: 0.6 });
    });
  }

  // ===== 12. Message clé =====
  {
    const s = pres.addSlide({ masterName: "Message", sectionTitle: S4 });
    await photo(s, "pac-installation", 0.44, 0.82, 0, 0, 5.0, H, "Un installateur raccorde une pompe à chaleur");
    T(s, "NOTRE MESSAGE", { x: 5.8, y: 1.5, w: 5, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 2 });
    s.addText([
      { text: "« Vous réalisez les travaux, ", options: {} },
      { text: "Cercle Énergie vous accompagne dans la gestion et le financement de vos aides CEE. »", options: { color: BLUE } },
    ], { placeholder: "title" });
    T(s, "Le partenaire unique de vos projets", { x: 5.8, y: 5.5, w: 6.9, h: 0.4, fontSize: 16, italic: true, color: GREY });
  }

  // ===== 13. Clôture =====
  {
    const s = pres.addSlide({ masterName: "Cloture", sectionTitle: S4 });
    await photo(s, "remise-dossier", 0.56, 0.97, 8.2, 0, W - 8.2, H, "Un artisan échange avec une conseillère autour d'un dossier");
    s.addImage({ path: LOGO_FULL, x: M, y: 0.55, ...logoFull(2.2), altText: "Logo Cercle Énergie — Le partenaire unique de vos projets" });
    s.addText("Devenez partenaire\nde Cercle Énergie", { placeholder: "title" });
    T(s, "« Cercle Énergie : votre partenaire pour simplifier, sécuriser et valoriser vos projets d'économies d'énergie. »",
      { x: M, y: 3.7, w: 6.9, h: 0.95, fontSize: 16 });
    T(s, "CONTACTEZ-NOUS", { x: M, y: 5.0, w: 5, h: 0.3, fontSize: 12, bold: true, color: BLUE, charSpacing: 2 });
    const contacts = [["LuPhone", "[Téléphone]"], ["LuMail", "[E-mail]"], ["LuGlobe", "[Site web]"]];
    for (let i = 0; i < 3; i++) {
      const x = M + i * 2.35, y = 5.5;
      await iconCircle(s, contacts[i][0], x, y, 0.5, NAVY, HEX.white);
      T(s, contacts[i][1], { x: x + 0.65, y, w: 1.6, h: 0.5, color: NAVY, bold: true, valign: "middle" });
    }
    s.addNotes("Les coordonnées entre crochets ([Téléphone], [E-mail], [Site web]) sont des champs à compléter : elles n'ont pas été fournies.");
  }

  await pres.writeFile({ fileName: OUT });
  const applyThemePath = path.join(SKILL, "scripts/apply_theme.js");
  if (fs.existsSync(applyThemePath)) {
    await require(applyThemePath).applyTheme(OUT, THEME);
  } else {
    console.warn("ATTENTION : apply_theme.js introuvable — les couleurs du thème ne sont pas écrites (définir PPTX_SKILL_DIR).");
  }
  console.log("Écrit :", OUT, "| police :", FONT);
})().catch((e) => { console.error(e); process.exit(1); });
