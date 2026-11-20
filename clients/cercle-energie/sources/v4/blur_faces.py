# Floutage des visages d'un plan réel : détections YuNet reliées en pistes (comblement des trous, prolongement
# de 4 images aux extrémités), + pistes posées à la main (images clés interpolées). Flou gaussien fort sur une
# ellipse aux bords adoucis.
# usage : python3 blur_faces.py <images> <ext> <f0> <f1> <detections.json> <manuel.json|-> <sortie> [debug]
#   manuel.json : {"tracks":[{"name":..,"keys":{"<image>":[cx,cy,w,h],...}}], "exclude":[[x0,y0,x1,y1,f0,f1],...]}
import cv2, numpy as np, json, sys, os
D,EXT,f0,f1,J,MJ,O=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],sys.argv[6],sys.argv[7]
DBG=len(sys.argv)>8
os.makedirs(O,exist_ok=True)
det=json.load(open(J)); man=json.load(open(MJ)) if MJ!='-' else {"tracks":[]}
EXC=man.get('exclude',[])
def excluded(b,f):
    cx,cy=b[0]+b[2]/2,b[1]+b[3]/2
    return any(x0<=cx<=x1 and y0<=cy<=y1 and a<=f<=c for x0,y0,x1,y1,a,c in EXC)
# --- détections par image, fusion des doublons (deux passes de détection)
def nms(bs):
    bs=sorted(bs,key=lambda b:-b[4]); keep=[]
    for b in bs:
        ok=True
        for k in keep:
            ix=max(0,min(b[0]+b[2],k[0]+k[2])-max(b[0],k[0])); iy=max(0,min(b[1]+b[3],k[1]+k[3])-max(b[1],k[1]))
            if ix*iy>0.3*min(b[2]*b[3],k[2]*k[3]): ok=False;break
        if ok: keep.append(b)
    return keep
F={}
for f in range(f0-8,f1+8):
    bs=[b for b in det.get(str(f),[]) if b[4]>=0.5 and b[2]>=8 and b[2]<500 and 0.6<b[3]/max(b[2],1)<2.2]
    F[f]=[b for b in nms(bs) if not excluded(b,f)]
# --- pistes
tracks=[]
for f in range(f0-8,f1+8):
    for b in F[f]:
        cx,cy=b[0]+b[2]/2,b[1]+b[3]/2; best=None;bd=1e9
        for t in tracks:
            lf,lb=t['last']
            if 0<f-lf<=6:
                lcx,lcy=lb[0]+lb[2]/2,lb[1]+lb[3]/2
                d=np.hypot(cx-lcx,cy-lcy); lim=max(0.9*lb[2],30)*(1+0.3*(f-lf))
                if d<lim and d<bd and abs(np.log(b[2]/lb[2]))<0.7: best,bd=t,d
        if best is None: best={'pts':{},'last':None}; tracks.append(best)
        if f in best['pts'] and best['pts'][f][4]>=b[4]: continue
        best['pts'][f]=b; best['last']=(f,b)
boxes={f:[] for f in range(f0,f1)}
kept=0
for t in tracks:
    ks=sorted(t['pts'])
    if not (len(ks)>=4 or max(t['pts'][k][4] for k in ks)>=0.85): continue
    kept+=1
    for f in range(ks[0]-4,ks[-1]+5):
        if not f0<=f<f1: continue
        if f in t['pts']: b=t['pts'][f]
        else:
            a=max([k for k in ks if k<f],default=None); c=min([k for k in ks if k>f],default=None)
            if a is None: b=t['pts'][c]
            elif c is None: b=t['pts'][a]
            else:
                u=(f-a)/(c-a); b=[t['pts'][a][i]*(1-u)+t['pts'][c][i]*u for i in range(4)]+[0]
        boxes[f].append((b[0]+b[2]/2,b[1]+b[3]/2,b[2],b[3]))
# --- pistes manuelles
for t in man['tracks']:
    K={int(k):v for k,v in t['keys'].items()}; ks=sorted(K)
    for f in range(max(f0,ks[0]),min(f1,ks[-1]+1)):
        a=max([k for k in ks if k<=f]); c=min([k for k in ks if k>=f])
        u=0 if c==a else (f-a)/(c-a)
        boxes[f].append(tuple(K[a][i]*(1-u)+K[c][i]*u for i in range(4)))
print('pistes auto gardées',kept,'sur',len(tracks),'| manuelles',len(man['tracks']))
json.dump({str(f):[list(map(float,b)) for b in boxes[f]] for f in boxes},open(os.path.join(O,'boxes.json'),'w'))
# --- flou
for f in range(f0,f1):
    im=cv2.imread(f"{D}/{f:04d}.{EXT}"); h,w=im.shape[:2]; out=im.astype(np.float32)
    for cx,cy,bw,bh in boxes[f]:
        s=max(bw,bh*0.8)
        ax,ay=0.8*s*1.0,1.0*s*1.0          # demi-axes de l'ellipse (visage + cheveux proches)
        pad=int(2.2*s)+10
        x0,y0=int(max(cx-pad,0)),int(max(cy-pad,0)); x1,y1=int(min(cx+pad,w)),int(min(cy+pad,h))
        if x1<=x0 or y1<=y0: continue
        roi=out[y0:y1,x0:x1]
        sig=max(7,0.30*s)
        bl=cv2.GaussianBlur(roi,(0,0),sig); bl=cv2.GaussianBlur(bl,(0,0),sig*0.6)
        m=np.zeros(roi.shape[:2],np.float32)
        cv2.ellipse(m,(int(cx-x0),int(cy-y0-0.05*bh)),(max(int(ax),3),max(int(ay),3)),0,0,360,1,-1)
        m=cv2.GaussianBlur(m,(0,0),max(2.5,0.16*s))
        roi[:]=roi*(1-m[...,None])+bl*m[...,None]
    o=np.clip(out,0,255).astype(np.uint8)
    cv2.imwrite(f"{O}/{f:04d}.png",o)
    if DBG:
        for cx,cy,bw,bh in boxes[f]: cv2.rectangle(o,(int(cx-bw/2),int(cy-bh/2)),(int(cx+bw/2),int(cy+bh/2)),(0,0,255),2)
        cv2.imwrite(f"{O}/dbg_{f:04d}.jpg",o)
print('ok')
