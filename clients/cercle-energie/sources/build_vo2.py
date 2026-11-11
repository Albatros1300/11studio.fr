import json, subprocess, re
segs=json.load(open('vo_segs.json'))
def mean(args):
    o=subprocess.run(["ffmpeg","-hide_banner"]+args+["-af","volumedetect","-f","null","-"],capture_output=True,text=True).stderr
    return float(re.search(r"mean_volume: ([-\d.]+)",o).group(1))
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
# segments 3 and 10 are replaced by re-recorded lines saying "Cercle Énergie"
repl={3:("audio/vo_s3.mp3",2.05),10:("audio/vo_s10.mp3",6.85)}
ins=["-i","audio/vo.mp3"];fc=[];lab=[];k=1
for s in segs:
    d=int(s['v0']*1000)
    if s['i'] in repl:
        f,L=repl[s['i']]; L=min(L,dur(f))
        g=mean(["-ss",str(s['src0']),"-t",str(s['src1']-s['src0']),"-i","audio/vo.mp3"])-mean(["-t",str(L),"-i",f])
        print("seg",s['i'],"gain",round(g,2),"len",L)
        ins+=["-i",f]
        fc.append(f"[{k}:a]atrim=0:{L},asetpts=PTS-STARTPTS,volume={g}dB,afade=t=out:st={L-0.05}:d=0.05,adelay={d}:all=1[a{s['i']}]");k+=1
    else:
        L=s['src1']-s['src0']
        fc.append(f"[0:a]atrim={s['src0']}:{s['src1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={L-0.03}:d=0.03,adelay={d}:all=1[a{s['i']}]")
    lab.append(f"[a{s['i']}]")
fc.append("".join(lab)+f"amix=inputs={len(segs)}:normalize=0,highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7[out]")
subprocess.run(["ffmpeg","-y","-v","error"]+ins+["-filter_complex",";".join(fc),"-map","[out]","-ar","48000","-ac","2","audio/vo_paced.wav"],check=True)
print(dur("audio/vo_paced.wav"))
