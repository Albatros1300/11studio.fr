#!/usr/bin/env python3
"""Monte les publicités vidéo Cercle Énergie (formats story 9:16 et fil 4:5).
Usage : python3 build_videos.py <dossier des plans mp4> <musique.mp3>"""
import subprocess, sys, os, json, urllib.parse
CL, MUSIC = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); W = 1080
FORMATS = {"story": (1920, 1080), "fil": (1350, 1010)}       # hauteur totale, hauteur vidéo
ADS = {
 "V1-vos-dossiers-cee": [
  ("1hero", .74, "Installateurs · Artisans", "Vos dossiers CEE,<br><em>on s’en occupe.</em>", ""),
  ("2combles", .52, "Vous", "Vous réalisez<br>les travaux.", ""),
  ("4industrie", .62, "Nous", "<em>Nous gérons<br>vos aides CEE.</em>", ""),
  ("6remise", .50, "Mandataire CEE", "Un seul interlocuteur,<br>des dossiers vérifiés.", ""),
  ("7clients", .55, "Cercle Énergie", "Devenez<br><em>partenaire.</em>", "En savoir plus")],
 "V2-moins-de-paperasse": [
  ("paperasse", .38, "Aides CEE", "Les CEE font gagner<br>des chantiers.", ""),
  ("paperasse2", .42, "Le problème", "<em>La paperasse vous<br>les fait payer.</em>", ""),
  ("6remise", .50, "La solution", "Confiez-nous<br>vos dossiers CEE.", ""),
  ("1hero", .74, "Résultat", "Vous restez<br><em>sur vos chantiers.</em>", ""),
  ("7clients", .55, "Cercle Énergie", "Devenez<br><em>partenaire.</em>", "En savoir plus")],
 "V3-tous-vos-terrains": [
  ("1hero", .74, "Résidentiel", "Pompes à chaleur,<br>chauffage, isolation.", ""),
  ("3tertiaire", .50, "Tertiaire", "Bureaux, commerces,<br>établissements.", ""),
  ("4industrie", .62, "Industrie", "Sites industriels.", ""),
  ("5agricole", .62, "Agricole", "Exploitations<br>et serres.", ""),
  ("6remise", .50, "Cercle Énergie", "<em>Vos aides CEE,<br>on s’en occupe.</em>", "Devenir partenaire")],
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
