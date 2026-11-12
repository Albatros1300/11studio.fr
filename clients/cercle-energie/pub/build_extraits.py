#!/usr/bin/env python3
"""Découpe des extraits de la vidéo de présentation aux formats réseaux (9:16 et 4:5)."""
import subprocess, os, json, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "..", "cercle-energie-presentation.mp4")
EX = [("E1-le-lien", 14.0, 24.6, "Notre rôle", "Le lien entre vos chantiers<br><em>et le financement CEE.</em>"),
      ("E2-nos-terrains", 24.9, 35.8, "Nos terrains", "PAC, chauffage, isolation,<br><em>tertiaire, industrie, agricole.</em>"),
      ("E3-cinq-services", 39.5, 49.4, "Nos services", "De l’éligibilité<br><em>au suivi des primes*.</em>"),
      ("E4-message", 49.6, 59.0, "Mandataire CEE", "Vous réalisez les travaux.<br><em>Nous gérons vos aides CEE.</em>")]
FORMATS = {"story": (1920, 800), "fil": (1350, 480)}
jobs = []
for name, a, b, k, h in EX:
    for fmt, (H, vy) in FORMATS.items():
        q = urllib.parse.urlencode({"vy": vy, "k": k, "h": h, "c": "Rejoindre le réseau", "s": "* Sous réserve de validation du dossier." if "*" in h else "Cercle Énergie · Le partenaire unique de vos projets"})
        jobs.append({"H": H, "url": "file://" + os.path.join(HERE, "extrait.html") + "?" + q, "out": os.path.join(HERE, "work", f"{name}-{fmt}.png")})
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
open(os.path.join(HERE, "work", "r.js"), "w").write("""const { chromium } = require('playwright');
(async () => { const jobs = JSON.parse(process.argv[2]); const b = await chromium.launch();
 for (const j of jobs) { const p = await b.newPage({ viewport: { width: 1080, height: j.H } }); await p.goto(j.url); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400); console.log(j.out.split('/').pop(), await p.title()); await p.screenshot({ path: j.out, omitBackground: true }); await p.close(); }
 await b.close(); })();""")
subprocess.run(["node", os.path.join(HERE, "work", "r.js"), json.dumps(jobs)], check=True)
for name, a, b, k, h in EX:
    for fmt, (H, vy) in FORMATS.items():
        out = os.path.join(HERE, "videos", f"{name}-{fmt}.mp4"); d = b - a
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", os.path.join(HERE, "work", f"{name}-{fmt}.png"), "-ss", str(a), "-t", str(d), "-i", SRC,
          "-filter_complex", f"[1:v]fps=30,scale=1080:608:flags=lanczos[v];[0:v][v]overlay=0:{vy}:shortest=1,fade=t=in:d=0.3,fade=t=out:st={d-0.4:.2f}:d=0.4,format=yuv420p[o];[1:a]afade=t=in:d=0.25,afade=t=out:st={d-0.5:.2f}:d=0.5[a]",
          "-map", "[o]", "-map", "[a]", "-t", str(d), "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out], check=True)
        print("écrit", os.path.basename(out))
