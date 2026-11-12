# Assemble la voix off V3 : chaque phrase est découpée dans la prise unique vo.mp3 (coupes au milieu des silences)
# et posée à l'instant t (début de parole dans la vidéo).
# usage : python3 build_vo.py <dossier_travail>   (attend <travail>/audio/vo.mp3)
import json, subprocess, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); W=sys.argv[1]
segs=json.load(open(os.path.join(HERE,'vo_segs.json')))
files=sorted({s['f'] for s in segs}); ins=[]
for f in files: ins+=["-i",os.path.join(W,"audio",f)]
fc=[];lab=[]
for n,s in enumerate(segs):
    k=files.index(s['f']); L=s['src1']-s['src0']; d=int(round((s['t']-(s['sp']-s['src0']))*1000))
    assert d>=0
    fc.append(f"[{k}:a]atrim={s['src0']}:{s['src1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={L-0.06:.3f}:d=0.06,adelay={d}:all=1[a{n}]")
    lab.append(f"[a{n}]")
fc.append("".join(lab)+f"amix=inputs={len(segs)}:normalize=0,highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7[out]")
out=os.path.join(W,"audio","vo_paced.wav")
subprocess.run(["ffmpeg","-y","-v","error"]+ins+["-filter_complex",";".join(fc),"-map","[out]","-ar","48000","-ac","2",out],check=True)
print(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout)
