import subprocess, os
FPS=24
ENC=["-an","-c:v","libx264","-preset","fast","-crf","14","-pix_fmt","yuv420p","-r",str(FPS)]
NORM="fps=24,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
def run(args): subprocess.run(["ffmpeg","-y","-v","error"]+args,check=True)
os.makedirs("segs",exist_ok=True)
# clean fake brand labels (blur patch) on K3 (moving) and K4 (static)
run(["-i","clips/K3.mp4","-filter_complex","[0:v]split[a][b];[b]crop=150:100:'1522-1.9*n':98,boxblur=14:2[bl];[a][bl]overlay=x='1522-1.9*n':y=98"]+ENC+["clips/K3c.mp4"])
run(["-i","clips/K4.mp4","-filter_complex","[0:v]split[a][b];[b]crop=156:70:1042:404,boxblur=12:2[bl];[a][bl]overlay=1042:404"]+ENC+["clips/K4c.mp4"])
f=lambda t: round(t*FPS)
# (name, clip, src offset, t_start, t_end, extra)
T=[("01","H1",0,0,5.25,"tpad=start_mode=clone:start_duration=0.3"),
("02","K1",0,5.25,10.30,"tpad=stop_mode=clone:stop_duration=0.3"),
("03","K2",0.9,10.30,14.0,None),
("04",None,0,14.0,24.55,None),
("05","K3c",0,24.55,26.25,None),
("06","K4c",0.3,26.25,27.10,None),
("07","K5",0.5,27.10,28.05,None),
("08","K12",1.5,28.05,29.60,None),
("09","K6",0.5,29.60,30.90,None),
("10","K7",0.5,30.90,31.70,None),
("11","K8",1.0,31.70,32.75,None),
("12","MOS",0,32.75,35.90,None),
("13","K9",0.5,35.90,39.45,None),
("14","K10",0,39.45,44.45,"tpad=stop_mode=clone:stop_duration=0.3"),
("15","H3",0,44.45,49.45,None),
("16","H2",0.8,49.45,52.65,None),
("17","K11",0.5,52.65,56.0,None),
("18","K13",0.2,56.0,59.55,None),
("19",None,0,59.55,72.0,None)]
lst=[]
for name,clip,off,t0,t1,extra in T:
    n=f(t1)-f(t0); out=f"segs/{name}.mp4"; lst.append(out)
    if clip is None:
        run(["-f","lavfi","-i",f"color=white:s=1920x1080:r=24","-frames:v",str(n)]+ENC+[out])
    elif clip=="MOS":
        tiles=[("K3c",1.8),("K5",1.6),("K12",0.0),("K6",1.8),("K7",1.4),("K8",0.0)]
        ins=[];fc=[]
        for i,(c,o) in enumerate(tiles):
            ins+=["-ss",str(o),"-i",f"clips/{c}.mp4"]
            fc.append(f"[{i}:v]fps=24,scale=960:540:flags=lanczos,crop=640:540,setsar=1[t{i}]")
        fc.append("".join(f"[t{i}]" for i in range(6))+"xstack=inputs=6:layout=0_0|640_0|1280_0|0_540|640_540|1280_540,format=yuv420p[o]")
        run(ins+["-filter_complex",";".join(fc),"-map","[o]","-frames:v",str(n)]+ENC+[out])
    else:
        vf=NORM+(","+extra if extra else "")
        run(["-ss",str(off),"-i",f"clips/{clip}.mp4","-vf",vf,"-frames:v",str(n)]+ENC+[out])
    got=int(subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v","-show_entries","stream=nb_read_frames","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip())
    print(name,clip,n,got,"OK" if got==n else "MISMATCH")
open("segs/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
run(["-f","concat","-safe","0","-i","segs/list.txt","-c","copy","out/base.mp4"])
print(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","out/base.mp4"],capture_output=True,text=True).stdout)
