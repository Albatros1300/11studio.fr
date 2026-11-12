# Montage des plans V3 (sans texte ni son) -> <travail>/out/base.mp4, 1920x1080, 24 i/s, 70 s.
# usage : python3 build_base.py <dossier_travail> <dossier_matiere>
#   <travail>/clips/ : reseau.mp4, qualification.mp4, fournisseur.mp4, formation.mp4 (plans V2) ; visite.mp4, devis.mp4, chauffe_eau.mp4 (plans générés pour la V3)
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
T=[("01",C("H1"),0,0,2.7,1),                 # pose d'une pompe à chaleur
("02",G("chauffe_eau"),0.2,2.7,4.2,1),       # chauffe-eau thermodynamique (plan généré V3)
("03",H("2combles"),0.3,4.2,6.0,1),          # isolation des combles
("04",C("H2"),0.1,6.0,10.75,1),              # l'artisan et ses clients
("05",H("paperasse"),0.3,10.75,13.3,1),      # la paperasse
("06",H("paperasse2"),0.6,13.3,15.7,1,"crop=1422:800:200:130,"), # la paperasse, plan resserré
("07",None,0,15.7,17.6,1),                   # blanc : logo
("08",G("reseau"),0,17.6,22.4,1),            # titre : le partenaire unique
("09",None,0,22.4,26.1,1),                   # blanc : le cercle et ses huit étapes
("10",C("K13"),0.2,26.1,29.7,1),            # 01 opportunité + 02 qualification du projet
("11",G("visite"),0.1,29.7,32.8,1),          # 03 visite technique (plan généré V3)
("12",G("fournisseur"),0.1,32.8,35.9,1),     # 04 choix des équipements
("13",G("devis"),0.1,35.9,39.2,1),           # 05 devis et financement (plan généré V3)
("14",H("1hero"),0.1,39.2,42.7,1),           # 06 chantier et justificatifs
("15",G("qualification"),0.4,42.7,46.4,1),   # 07 montage et suivi CEE
("16",H("6remise"),0.2,46.4,50.4,1),         # 08 versement de la prime
("17",G("formation"),0,50.4,55.8,1.1),       # accroche 1 : des règles expliquées
("18",C("K1"),0.3,55.8,60.2,1),              # accroche 2
("19",None,0,60.2,70.0,1)]                   # blanc : carton final
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
