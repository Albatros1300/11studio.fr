#!/usr/bin/env python3
"""Deux nouvelles vidéos publicitaires sur un seul axe : « les dossiers CEE, le soir après le chantier ».
Usage : python3 build_nouvelles.py <dossier plans verticaux> <voix-off.mp3> <musique.mp3>"""
import subprocess, sys, os, json, urllib.parse
CL, VO, MUSIC = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); W = 1080
FORMATS = {"story": (1920, 0), "fil": (1350, 250)}        # hauteur, décalage vertical du recadrage
def url(**k): return "file://" + os.path.join(HERE, "legende.html") + "?" + urllib.parse.urlencode(k)
def shots(jobs): subprocess.run(["node", os.path.join(HERE, "work", "r.js"), json.dumps(jobs)], check=True)
def ff(a): subprocess.run(["ffmpeg", "-y", "-v", "error"] + a, check=True)

# ---------- N1 : film court avec voix off (voix décalée de 0,3 s)
N1_CLIPS = [("a", 0.0, 5.1), ("b", 5.1, 9.75), ("c", 9.75, 11.75), ("d", 11.75, 16.25), ("e", 16.25, 19.3)]
N1_CAPS = [("hook", "21:00", 0.0, 1.5, "Le chantier est fini"), ("cap", "Le chantier est fini…", 1.5, 3.2, ""), ("cap", "<em>mais pas votre journée.</em>", 3.2, 5.1, ""),
           ("cap", "Il reste les dossiers CEE.", 5.1, 7.6, ""), ("cap", "Et si ce n’était plus<br>à vous de les faire ?", 7.6, 9.75, ""),
           ("cap", "<em>Transmettez-nous votre chantier.</em>", 9.75, 11.75, ""), ("cap", "Cercle Énergie vérifie l’éligibilité,", 11.75, 14.15, ""),
           ("cap", "monte le dossier,", 14.15, 15.15, ""), ("cap", "et suit la prime*.", 15.15, 16.25, ""), ("cap", "<em>Vous, vous rentrez chez vous.</em>", 16.25, 19.3, "")]
N1_END = (19.3, 22.6)
# ---------- N2 : liste « qui fait quoi » (musique seule)
ROWS = [["L’éligibilité", "Nous"], ["Le dossier", "Nous"], ["Les vérifications", "Nous"], ["Le suivi de la prime*", "Nous"], ["Les travaux", "Vous"]]
N2_BEATS = [(0.0, 1.7, 0), (1.7, 3.0, 1), (3.0, 4.3, 2), (4.3, 5.6, 3), (5.6, 6.9, 4), (6.9, 9.4, 5)]
N2_END = (9.4, 12.6)

jobs = []
for fmt, (H, _) in FORMATS.items():
    for i, (m, t, a, b, s) in enumerate(N1_CAPS):
        jobs.append({"H": H, "url": url(m=m, t=t, s=s), "out": os.path.join(HERE, "work", f"n1-{fmt}-{i}.png")})
    jobs.append({"H": H, "url": url(m="end", t="Vos dossiers CEE,<br><em>on s’en occupe.</em>", c="Devenir partenaire", s="* Sous réserve de validation du dossier."), "out": os.path.join(HERE, "work", f"n1-{fmt}-end.png")})
    for i, (a, b, n) in enumerate(N2_BEATS):
        jobs.append({"H": H, "url": url(m="list", dim=1, t="Dossier CEE :<br><em>qui fait quoi ?</em>", rows=json.dumps(ROWS), n=n), "out": os.path.join(HERE, "work", f"n2-{fmt}-{i}.png")})
    jobs.append({"H": H, "url": url(m="end", t="Vous posez.<br><em>On gère le dossier.</em>", c="Devenir partenaire", s="* Sous réserve de validation du dossier."), "out": os.path.join(HERE, "work", f"n2-{fmt}-end.png")})
shots(jobs)

def base(clips, H, yoff, total):
    """concatène les plans verticaux recadrés ; renvoie (entrées, filtres, étiquette)"""
    ins, fc = [], []
    for i, (c, a, b) in enumerate(clips):
        ins += ["-t", f"{b-a:.2f}", "-i", os.path.join(CL, c + ".mp4")]
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
    # ---- N2
    clips = [("b", 0.0, 4.9), ("a", 4.9, 6.9), ("e", 6.9, 9.4)]
    ins, fc = base(clips, H, yoff, N2_END[1]); n = len(clips); cur = "[bg]"
    ov = [(os.path.join(HERE, "work", f"n2-{fmt}-{i}.png"), a, b) for i, (a, b, _) in enumerate(N2_BEATS)] + [(os.path.join(HERE, "work", f"n2-{fmt}-end.png"), *N2_END)]
    for j, (p, a, b) in enumerate(ov):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{N2_END[1]}", "-i", p]
        fc.append(f"{cur}[{n+j}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{j}]"); cur = f"[v{j}]"
    k = n + len(ov); ins += ["-ss", "14", "-i", MUSIC]
    fc.append(f"[{k}:a]volume=-4dB,afade=t=in:d=0.3,afade=t=out:st={N2_END[1]-1.2:.2f}:d=1.2[a]")
    out = os.path.join(HERE, "videos", f"N2-qui-fait-quoi-{fmt}.mp4")
    ff(ins + ["-filter_complex", ";".join(fc), "-map", cur, "-map", "[a]", "-t", f"{N2_END[1]}", "-r", "30", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]); print("écrit", os.path.basename(out))
