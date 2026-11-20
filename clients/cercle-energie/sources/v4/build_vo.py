# Voix off V4 : chaque phrase est découpée dans la prise unique audio/vo.mp3 (coupes dans les silences) et posée
# pour que la parole commence à l'instant t de la vidéo.  usage : python3 build_vo.py <sortie.wav> <durée>
import json, subprocess, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT,DUR=sys.argv[1],float(sys.argv[2])
segs=json.load(open(os.path.join(HERE,'vo_segs.json'))); fc=[];lab=[]
for n,s in enumerate(segs):
    L=s['src1']-s['src0']; d=int(round((s['t']-(s['sp']-s['src0']))*1000)); assert d>=0
    fc.append(f"[0:a]atrim={s['src0']}:{s['src1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={L-0.05:.3f}:d=0.05,adelay={d}:all=1[a{n}]"); lab.append(f"[a{n}]")
fc.append("".join(lab)+f"amix=inputs={len(segs)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR},highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7[out]")
subprocess.run(["ffmpeg","-y","-v","error","-i",os.path.join(HERE,"audio","vo.mp3"),"-filter_complex",";".join(fc),"-map","[out]","-ar","48000","-ac","2",OUT],check=True)
print('ok',OUT)
