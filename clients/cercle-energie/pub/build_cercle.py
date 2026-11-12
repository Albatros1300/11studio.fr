#!/usr/bin/env python3
"""Monte les publicités vidéo Cercle Énergie (accroches du brief de marque) (formats story 9:16 et fil 4:5).
Usage : python3 build_reseau.py <dossier des plans mp4> <musique.mp3>"""
import subprocess, sys, os, json, urllib.parse
CL, MUSIC = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); W = 1080
FORMATS = {"story": (1920, 1080), "fil": (1350, 1010)}       # hauteur totale, hauteur vidéo
ADS = {
 "C1-a-chaque-etape": [
  ("1hero", .74, "Installateurs · Chauffagistes", "Vous installez.", ""),
  ("7clients", .55, "Étapes 1 et 2", "Le projet,<br>sa qualification.", ""),
  ("fournisseur", .50, "Étapes 3 et 4", "Visite technique,<br>équipements.", ""),
  ("6remise", .50, "Étapes 5 et 6", "Devis, chantier,<br>justificatifs.", ""),
  ("rge", .42, "Étapes 7 et 8", "Dossier suivi<br>jusqu’à la prime.", ""),
  ("visite", .36, "Des outils dédiés", "<em>Pour des dossiers<br>de qualité.</em>", ""),
  ("reseau", .47, "Cercle Énergie", "<em>Un seul cercle<br>de services.</em>", "Parlons de vos projets")],
 "C2-installateurs-pac": [
  ("1hero", .74, "Pompes à chaleur", "Vous posez des<br>pompes à chaleur.", ""),
  ("paperasse", .38, "Le soir", "Et les dossiers<br>de primes ?", ""),
  ("rge", .42, "Cercle Énergie", "<em>Préparés, contrôlés,<br>suivis.</em>", ""),
  ("fournisseur", .50, "Et aussi", "Les bons<br>équipements.", ""),
  ("reseau", .47, "Cercle Énergie", "Un partenaire<br><em>à vos côtés.</em>", "Parlons de vos projets")],
 "C3-artisan-local": [
  ("1hero", .74, "Artisans locaux", "Vos chantiers<br>sont soignés.", ""),
  ("paperasse", .38, "Mais le soir…", "Les dossiers<br>vous épuisent.", ""),
  ("rge", .42, "Cercle Énergie", "<em>Des dossiers suivis.<br>Des règles claires.</em>", ""),
  ("7clients", .55, "Cercle Énergie", "L’artisan local,<br><em>bien accompagné.</em>", "Parlons de vos projets")],
 "C4-moins-d-administratif": [
  ("paperasse2", .42, "Sur le terrain", "Moins de temps dans<br>l’administratif.", ""),
  ("1hero", .74, "Sur le terrain", "<em>Plus de temps<br>sur vos chantiers.</em>", ""),
  ("visite", .36, "Des outils dédiés", "Pour des dossiers<br>de qualité.", ""),
  ("6remise", .50, "Cercle Énergie", "Un interlocuteur<br>identifié.", ""),
  ("reseau", .47, "Cercle Énergie", "Le partenaire unique<br>de vos projets.", "Parlons de vos projets")],
}
D, X = 3.3, 0.4
def run(a): subprocess.run(["ffmpeg", "-y", "-v", "error"] + a, check=True)
node = r"""
const { chromium } = require('playwright');
(async () => { const jobs = JSON.parse(process.argv[2]); const b = await chromium.launch();
 for (const j of jobs) { const p = await b.newPage({ viewport: { width: 1080, height: j.H } }); await p.goto(j.url); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150); await p.screenshot({ path: j.out, omitBackground: true }); await p.close(); }
 await b.close(); })();"""
jobs = []
for ad, scenes in ADS.items():
    for fmt, (H, vh) in FORMATS.items():
        for i, (clip, cx, k, h, c) in enumerate(scenes):
            q = urllib.parse.urlencode({"vh": vh, "k": k, "h": h, "c": c, "i": i, "n": len(scenes)})
            jobs.append({"H": H, "url": "file://" + os.path.join(HERE, "panneau.html") + "?" + q, "out": os.path.join(HERE, "work", f"{ad}-{fmt}-{i}.png")})
open(os.path.join(HERE, "work", "r.js"), "w").write(node)
subprocess.run(["node", os.path.join(HERE, "work", "r.js"), json.dumps(jobs)], check=True)
for ad, scenes in ADS.items():
    for fmt, (H, vh) in FORMATS.items():
        ins, fc = [], []
        for i, (clip, cx, k, h, c) in enumerate(scenes):
            ins += ["-ss", "0.5", "-t", str(D + X), "-i", os.path.join(CL, clip + ".mp4"), "-i", os.path.join(HERE, "work", f"{ad}-{fmt}-{i}.png")]
            sw = round(vh * 16 / 9 / 2) * 2; x = max(0, min(sw - W, round(sw * cx - W / 2)))
            fc.append(f"[{2*i}:v]fps=30,scale={sw}:{vh}:flags=lanczos,crop={W}:{vh}:{x}:0,pad={W}:{H}:0:0:color=0x07264B,setsar=1[b{i}];[b{i}][{2*i+1}:v]overlay=0:0,format=yuv420p[s{i}]")
        cur = "[s0]"
        for i in range(1, len(scenes)):
            fc.append(f"{cur}[s{i}]xfade=transition=fade:duration={X}:offset={i*D:.2f}[x{i}]"); cur = f"[x{i}]"
        total = len(scenes) * D + X
        ins += ["-ss", "14", "-t", str(total), "-i", MUSIC]
        fc.append(f"[{2*len(scenes)}:a]afade=t=in:d=0.4,afade=t=out:st={total-1.2:.2f}:d=1.2,volume=-4dB[a]")
        out = os.path.join(HERE, "videos", f"{ad}-{fmt}.mp4")
        run(ins + ["-filter_complex", ";".join(fc), "-map", cur, "-map", "[a]", "-t", str(total), "-r", "30", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out])
        print("écrit", os.path.basename(out))
