# Montage des plans V2 (sans texte ni son) -> <travail>/out/base.mp4, 1920x1080, 24 i/s, 63 s.
# usage : python3 build_base.py <dossier_travail> <dossier_matiere>
#   <travail>/clips/ : formation.mp4, qualification.mp4, fournisseur.mp4, reseau.mp4 (plans générés depuis les photos)
#   <matiere>/ce/clips/, <matiere>/hv/ : plans de la V1
import subprocess, os, sys
W,M=sys.argv[1],sys.argv[2]
FPS=24
ENC=["-an","-c:v","libx264","-preset","fast","-crf","14","-pix_fmt","yuv420p","-r",str(FPS)]
NORM="fps=24,scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,format=yuv420p"
def run(args): subprocess.run(["ffmpeg","-y","-v","error"]+args,check=True)
os.makedirs(f"{W}/segs",exist_ok=True); os.makedirs(f"{W}/out",exist_ok=True)
f=lambda t: round(t*FPS)
C=lambda n:f"{M}/ce/clips/{n}.mp4"; H=lambda n:f"{M}/hv/{n}.mp4"; G=lambda n:f"{W}/clips/{n}.mp4"
# (nom, fichier, décalage source, début, fin, ralenti)
T=[("01",C("H1"),0,0,3.2,1),            # artisan sur pompe à chaleur
("02",C("K1"),0.3,3.2,6.4,1),           # chantier façade
("03",H("paperasse"),0.3,6.4,9.0,1),    # la paperasse
("04",H("paperasse2"),0.6,9.0,12.2,1,"crop=1422:800:200:130,"), # la paperasse, plan resserré
("05",None,0,12.2,13.1,1),              # blanc : logo
("06",G("reseau"),0,13.1,18.5,1.08),    # le réseau
("07",None,0,18.5,26.15,1),             # blanc : schéma
("08",C("K10"),0.2,26.15,30.8,1),       # volet 1 dossiers CEE
("09",C("K11"),0.5,30.8,34.4,1),        # volet 2 démarches administratives
("10",G("formation"),0.3,34.4,37.8,1),  # volet 3 formation
("11",G("qualification"),0.4,37.8,41.8,1), # volet 4 qualification RGE
("12",G("fournisseur"),0.1,41.8,46.6,1),# volet 5 tarifs fournisseurs
("13",H("6remise"),0,46.6,51.9,1.06),   # phrase directrice
("14",None,0,51.9,63.0,1)]              # blanc : carton final
lst=[]
for name,clip,off,t0,t1,slow,*pre in T:
    n=f(t1)-f(t0); out=f"{W}/segs/{name}.mp4"; lst.append(out)
    if clip is None:
        run(["-f","lavfi","-i","color=white:s=1920x1080:r=24","-frames:v",str(n)]+ENC+[out])
    else:
        vf=(pre[0] if pre else "")+(f"setpts={slow}*PTS," if slow!=1 else "")+NORM
        run(["-ss",str(off),"-i",clip,"-vf",vf,"-frames:v",str(n)]+ENC+[out])
    got=int(subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v","-show_entries","stream=nb_read_frames","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip())
    print(name,os.path.basename(clip or "blanc"),n,got,"OK" if got==n else "MISMATCH")
open(f"{W}/segs/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
run(["-f","concat","-safe","0","-i",f"{W}/segs/list.txt","-c","copy",f"{W}/out/base.mp4"])
print(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{W}/out/base.mp4"],capture_output=True,text=True).stdout)
