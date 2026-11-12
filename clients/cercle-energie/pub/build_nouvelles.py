#!/usr/bin/env python3
"""Film publicitaire N1 : « 21 h, le chantier est fini… mais pas votre journée » (voix off et sous-titres).
Usage : python3 build_nouvelles.py <dossier plans verticaux> <voix-off.mp3> <musique.mp3>"""
import subprocess, sys, os, json, urllib.parse
CL, VO, MUSIC = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); W = 1080
FORMATS = {"story": (1920, 0), "fil": (1350, 250)}        # hauteur, décalage vertical du recadrage
def url(**k): return "file://" + os.path.join(HERE, "legende.html") + "?" + urllib.parse.urlencode(k)
def shots(jobs): subprocess.run(["node", os.path.join(HERE, "work", "r.js"), json.dumps(jobs)], check=True)
def ff(a): subprocess.run(["ffmpeg", "-y", "-v", "error"] + a, check=True)

# ---------- N1 : film court avec voix off (voix décalée de 0,3 s)
N1_CLIPS = [("a", 0.0, 4.7, 0), ("b", 4.7, 9.35, 0), ("c", 9.35, 11.2, 0), ("d", 11.2, 15.95, 0), ("c", 15.95, 18.0, 2.6), ("e", 18.0, 20.0, 0)]
N1_CAPS = [("hook", "21:00", 0.0, 1.5, "Le chantier est fini"), ("cap", "Le chantier est fini…", 1.55, 3.05, ""), ("cap", "<em>mais pas votre journée.</em>", 3.05, 4.7, ""),
           ("cap", "Il reste les dossiers<br>de financement.", 4.7, 6.85, ""), ("cap", "Et si vous n’étiez plus seul<br>pour les faire ?", 6.9, 9.35, ""),
           ("cap", "<em>Transmettez-nous votre chantier.</em>", 9.35, 11.2, ""), ("cap", "Cercle Énergie monte<br>le dossier avec vous,", 11.2, 13.5, ""),
           ("cap", "via nos services ou<br>nos applications dédiées,", 13.5, 15.95, ""), ("cap", "et le suit jusqu’à la prime*.", 15.95, 18.0, ""), ("cap", "<em>Vous, vous rentrez chez vous.</em>", 18.0, 20.0, "")]
N1_END = (20.0, 23.4)

jobs = []
for fmt, (H, _) in FORMATS.items():
    for i, (m, t, a, b, s) in enumerate(N1_CAPS):
        jobs.append({"H": H, "url": url(m=m, t=t, s=s), "out": os.path.join(HERE, "work", f"n1-{fmt}-{i}.png")})
    jobs.append({"H": H, "url": url(m="end", t="Vos dossiers de financement,<br><em>montés avec vous.</em>", c="Parlons de vos projets", s="* Selon les conditions contractuelles et la validation des dossiers."), "out": os.path.join(HERE, "work", f"n1-{fmt}-end.png")})
shots(jobs)

def base(clips, H, yoff, total):
    """concatène les plans verticaux recadrés ; renvoie (entrées, filtres, étiquette)"""
    ins, fc = [], []
    for i, (c, a, b, ss) in enumerate(clips):
        ins += ["-ss", f"{ss}", "-t", f"{b-a:.2f}", "-i", os.path.join(CL, c + ".mp4")]
        fc.append(f"[{i}:v]fps=30,scale={W}:1920:flags=lanczos,crop={W}:{H}:0:{yoff},setsar=1,setpts=PTS-STARTPTS[c{i}]")
    fc.append("".join(f"[c{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1,tpad=stop_mode=clone:stop_duration=6[bg]")
    return ins, fc

for fmt, (H, yoff) in FORMATS.items():
    # ---- N1
    ins, fc = base(N1_CLIPS, H, yoff, N1_END[1]); n = len(N1_CLIPS); cur = "[bg]"
    ov = [(os.path.join(HERE, "work", f"n1-{fmt}-{i}.png"), a, b) for i, (_, _, a, b, _) in enumerate(N1_CAPS)] + [(os.path.join(HERE, "work", f"n1-{fmt}-end.png"), *N1_END)]
    for j, (p, a, b) in enumerate(ov):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{N1_END[1]}", "-i", p]
        fc.append(f"[{n+j}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.18:alpha=1[o{j}];{cur}[o{j}]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{j}]"); cur = f"[v{j}]"
    k = n + len(ov); ins += ["-i", VO, "-ss", "14", "-i", MUSIC]
    fc.append(f"[{k}:a]adelay=300:all=1,apad=whole_dur={N1_END[1]},loudnorm=I=-15:TP=-1.5,asplit[vo][sc];[{k+1}:a]volume=-9dB,afade=t=in:d=0.4,afade=t=out:st={N1_END[1]-1.3:.2f}:d=1.3[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=25:release=400[md];[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.9[a]")
    out = os.path.join(HERE, "videos", f"N1-21h-le-chantier-est-fini-{fmt}.mp4")
    ff(ins + ["-filter_complex", ";".join(fc), "-map", cur, "-map", "[a]", "-t", f"{N1_END[1]}", "-r", "30", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]); print("écrit", os.path.basename(out))
