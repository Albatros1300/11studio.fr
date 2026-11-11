// Version « diffusion » : chaque diapositive est une image pleine page,
// pour un rendu identique partout (iPhone, WhatsApp, Keynote, PowerPoint).
// Usage : NODE_PATH=<node_modules> node build_diffusion.js <dossier des pages JPEG>
const pptxgen = require('pptxgenjs'); const fs = require('fs'); const path = require('path');
const dir = process.argv[2]; const p = new pptxgen(); p.layout = 'LAYOUT_WIDE'; p.title = 'Cercle Énergie — Plaquette de présentation';
fs.readdirSync(dir).filter((f) => /^p-\d+\.jpg$/.test(f)).sort().forEach((f) => { const s = p.addSlide(); s.background = { color: 'FFFFFF' }; s.addImage({ path: path.join(dir, f), x: 0, y: 0, w: 13.333, h: 7.5 }); });
p.writeFile({ fileName: path.join(__dirname, 'Cercle-Energie-Plaquette-diffusion.pptx') }).then((f) => console.log('écrit', f));
