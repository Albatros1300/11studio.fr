import json, subprocess
# sentence cut points (midpoints of detected silences) in source VO, and pause added after each
cuts=[0,4.27,12.05,14.40,21.52,31.89,34.83,44.27,47.03,52.70,59.79]
gaps=[0.35,0.9,0.9,0.6,0.7,0.5,0.7,0.3,1.0,0]
T0=0.8
segs=[];t=T0
for i in range(10):
    s,e=cuts[i],cuts[i+1]
    segs.append(dict(i=i+1,src0=s,src1=e,v0=round(t,3),v1=round(t+e-s,3)))
    t+=e-s+gaps[i]
json.dump(segs,open('vo_segs.json','w'),indent=1)
for s in segs: print(s)
# build audio: delay each segment to its video start
fc=[];ins=[]
for k,s in enumerate(segs):
    fc.append(f"[0:a]atrim={s['src0']}:{s['src1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={s['src1']-s['src0']-0.03}:d=0.03,adelay={int(s['v0']*1000)}:all=1[a{k}]")
    ins.append(f"[a{k}]")
fc.append("".join(ins)+f"amix=inputs={len(segs)}:normalize=0,highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7[out]")
subprocess.run(["ffmpeg","-y","-v","error","-i","audio/vo.mp3","-filter_complex",";".join(fc),"-map","[out]","-ar","48000","-ac","2","audio/vo_paced.wav"],check=True)
print(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","audio/vo_paced.wav"],capture_output=True,text=True).stdout)
