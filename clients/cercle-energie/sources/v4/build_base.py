# Montage des images V4 (sans textes ni son) -> <travail>/out/base.mp4, 1920x1080, 25 i/s.
# Plans réels : images déjà traitées (écran remplacé, visages floutés) lues image par image, 30 i/s joués à 25 i/s
# (léger ralenti, aucune image inventée). Plans générés : 24 -> 25 i/s. Inserts d'applications composés ici.
# usage : python3 build_base.py <travail>
import cv2, numpy as np, subprocess, sys, os, json
W=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__))
PL='/home/user/11studio.fr/clients/cercle-energie/materiel/plans-paysage'
INS=os.path.join(HERE,'inserts','png')
FPS=25; OW,OH=1920,1080; XF=5   # fondu enchaîné : 5 images (0,2 s)
os.makedirs(f"{W}/out",exist_ok=True)

# ---------- étalonnage
def lut(fn):
    x=np.arange(256)/255.0; return np.clip(fn(x)*255,0,255).astype(np.uint8)
S_CURVE=lut(lambda x: x+0.06*np.sin(2*np.pi*x)*(0.5-abs(x-0.5))*2)
def grade_real(im):
    im=cv2.LUT(im,S_CURVE).astype(np.float32)
    im[...,2]*=1.035; im[...,0]*=0.965           # un peu plus chaud (BGR)
    g=im.mean(2,keepdims=True); im=g+(im-g)*1.08  # saturation +8 %
    return np.clip(im,0,255).astype(np.uint8)
def grade_gen(im):
    im=im.astype(np.float32); im[...,2]*=0.985; im[...,0]*=1.01
    g=im.mean(2,keepdims=True); im=g+(im-g)*0.93
    return np.clip(im,0,255).astype(np.uint8)
VIG=None
def vignette(im):
    global VIG
    if VIG is None:
        yy,xx=np.mgrid[0:OH,0:OW]; r=np.hypot((xx-OW/2)/(OW/2),(yy-OH/2)/(OH/2))
        VIG=(1-0.16*np.clip(r-0.55,0,1)**1.6/0.66)[...,None].astype(np.float32)
    return np.clip(im*VIG,0,255).astype(np.uint8)

# ---------- sources
class Seq:   # images numérotées (plans réels traités)
    def __init__(s,d,ext,a,b): s.d,s.ext,s.a,s.b=d,ext,a,b; s.c={}
    def get(s,i):
        i=int(min(max(i,s.a),s.b))
        if i not in s.c:
            if len(s.c)>40: s.c.clear()
            s.c[i]=cv2.imread(f"{s.d}/{i:04d}.{s.ext}")
        return s.c[i]
class Clip:  # vidéo générée, décodée une fois
    def __init__(s,path):
        cap=cv2.VideoCapture(path); s.f=[]
        while True:
            ok,f=cap.read()
            if not ok: break
            s.f.append(cv2.resize(f,(1934,1080),interpolation=cv2.INTER_AREA)[:,7:1927])
    def get(s,i): return s.f[int(min(max(i,0),len(s.f)-1))]

def kb(im,z,cx=0.5,cy=0.5):   # zoom lent (Ken Burns) centré sur (cx,cy)
    if abs(z-1)<1e-4: return im
    M=np.float32([[z,0,(1-z)*cx*OW],[0,z,(1-z)*cy*OH]])
    return cv2.warpAffine(im,M,(OW,OH),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
def ease(u): u=min(max(u,0),1); return u*u*(3-2*u)
def eout(u): u=min(max(u,0),1); return 1-(1-u)**3

def load_rgba(name,h):
    im=cv2.imread(os.path.join(INS,name),cv2.IMREAD_UNCHANGED); s=h/im.shape[0]
    return cv2.resize(im,(int(im.shape[1]*s),h),interpolation=cv2.INTER_AREA)
def paste(dst,rgba,x,y,alpha=1.0,shadow=True):
    """colle rgba (BGRA) avec coin haut-gauche (x,y) flottants ; ombre portée douce"""
    h,w=rgba.shape[:2]; ix,iy=int(np.floor(x)),int(np.floor(y)); fx,fy=x-ix,y-iy
    if fx or fy:
        rgba=cv2.warpAffine(rgba,np.float32([[1,0,fx],[0,1,fy]]),(w+1,h+1),flags=cv2.INTER_LINEAR); h,w=rgba.shape[:2]
    a=rgba[...,3:4].astype(np.float32)/255*alpha
    if shadow:
        pad=60; sh=np.zeros((h+2*pad,w+2*pad),np.float32); sh[pad:pad+h,pad:pad+w]=a[...,0]
        sh=cv2.GaussianBlur(sh,(0,0),26)*0.55
        _blend(dst,np.zeros((h+2*pad,w+2*pad,3),np.float32),sh[...,None],ix-pad,iy-pad+26)
    _blend(dst,rgba[...,:3].astype(np.float32),a,ix,iy)
def _blend(dst,src,a,x,y):
    h,w=src.shape[:2]; x0,y0=max(x,0),max(y,0); x1,y1=min(x+w,OW),min(y+h,OH)
    if x1<=x0 or y1<=y0: return
    s=src[y0-y:y1-y,x0-x:x1-x]; aa=a[y0-y:y1-y,x0-x:x1-x]
    d=dst[y0:y1,x0:x1].astype(np.float32); dst[y0:y1,x0:x1]=np.clip(d*(1-aa)+s*aa,0,255).astype(np.uint8)
def rounded(im,r):
    h,w=im.shape[:2]; m=np.zeros((h,w),np.uint8)
    cv2.rectangle(m,(r,0),(w-r,h),255,-1); cv2.rectangle(m,(0,r),(w,h-r),255,-1)
    for cx,cy in ((r,r),(w-r-1,r),(r,h-r-1),(w-r-1,h-r-1)): cv2.circle(m,(cx,cy),r,255,-1,cv2.LINE_AA)
    return np.dstack([im,m])

V4=os.environ.get('V4SCR')   # dossier des images réelles traitées
R1=Seq(f"{V4}/bl1234",'png',0,49); R2=Seq(f"{V4}/bl1232a",'png',36,107)
R3=Seq(f"{V4}/bl1232b",'png',150,259); R4=Seq(f"{V4}/bl1242",'png',40,144)

# ---------- plans : (début, durée, fonction(k, n) -> image BGR)
shots=[]
def shot(t0,d):
    def deco(fn): shots.append((t0,d,fn)); return fn
    return deco
src=lambda seq,start: (lambda k,n: vignette(grade_real(seq.get(start+k))))
shots.append((0.00,1.92,src(R1,0)))
shots.append((1.92,2.68,src(R2,41)))
shots.append((4.60,3.24,src(R3,168)))
shots.append((7.84,3.40,src(R4,50)))

PC=cv2.imread(os.path.join(INS,'pc_analyse.png'))
@shot(11.24,5.00)
def pc_shot(k,n):
    # fond : le plateau réel (déjà flouté) très flou et assombri ; fenêtre du logiciel qui monte puis zoom lent
    bg=grade_real(R3.get(170+int(k*0.75)))
    bg=cv2.GaussianBlur(cv2.resize(bg,(480,270),interpolation=cv2.INTER_AREA),(0,0),5)
    bg=cv2.resize(bg,(OW,OH),interpolation=cv2.INTER_CUBIC).astype(np.float32)
    bg=bg*0.42+np.array([75,38,7],np.float32)*0.58*0.55
    out=np.clip(bg,0,255).astype(np.uint8)
    t=k/FPS; u=eout(t/0.9)
    z=1.0+0.10*ease(t/n*FPS)            # zoom lent dans la capture, vers la colonne « Contrôles »
    ww=int(1500); hh=int(ww*PC.shape[0]/PC.shape[1])
    # recadrage dans la capture (zoom) puis mise à l'échelle
    sw,sh=PC.shape[1]/z,PC.shape[0]/z; cx=PC.shape[1]*(0.5+0.18*(z-1)/0.10*0.5); cy=PC.shape[0]*0.5
    x0=min(max(cx-sw/2,0),PC.shape[1]-sw); y0=min(max(cy-sh/2,0),PC.shape[0]-sh)
    M=np.float32([[ww/sw,0,-x0*ww/sw],[0,hh/sh,-y0*hh/sh]])
    win=cv2.warpAffine(PC,M,(ww,hh),flags=cv2.INTER_AREA)
    win=rounded(win,22)
    paste(out,win,(OW-ww)/2,(OH-hh)/2-30+60*(1-u),alpha=u)
    return vignette(out)

CARTE=load_rgba('carte_opportunites.png',840)
VISITE=Clip(f"{PL}/v3-visite.mp4")
@shot(16.24,4.80)
def visite(k,n):
    im=grade_gen(kb(VISITE.get(5+k*24/25),1.0+0.05*k/n,0.35,0.45))
    t=k/FPS; u=eout((t-0.35)/0.9)
    x=1270+(1-u)*700; y=(OH-CARTE.shape[0])/2+10+(1-u)*120
    paste(im,CARTE,x,y,alpha=min(1,u*1.5),shadow=True)
    return vignette(im)

PH=[load_rgba('qualif_photos.png',800),load_rgba('visite_scan.png',800),load_rgba('equipements.png',800)]
DEVIS=Clip(f"{PL}/v3-devis.mp4")
@shot(21.04,5.40)
def trio(k,n):
    bg=grade_gen(kb(DEVIS.get(3+k*24/25),1.04+0.04*k/n))
    bg=cv2.GaussianBlur(bg,(0,0),7).astype(np.float32)*0.62+np.array([75,38,7],np.float32)*0.38*0.6
    im=np.clip(bg,0,255).astype(np.uint8)
    t=k/FPS
    # téléphones : bilan (0,8 s), visite technique (1,2 s), devis/équipements (2,1 s) — calés sur la voix
    for i,(t0,cx) in enumerate(((0.80,560),(1.20,960),(2.10,1360))):
        u=eout((t-t0)/0.75)
        if u<=0: continue
        p=PH[i]; x=cx-p.shape[1]/2; y=(OH-p.shape[0])/2+20+(1-u)*260
        paste(im,p,x,y,alpha=min(1,u*1.6))
    return vignette(im)

def plan(path,off,z0,z1,cx=0.5,cy=0.5):
    C=Clip(f"{PL}/{path}")
    return lambda k,n: vignette(grade_gen(kb(C.get(off+k*24/25),z0+(z1-z0)*k/n,cx,cy)))
shots.append((26.44,2.80,plan('7clients.mp4',4,1.0,1.05)))
shots.append((29.24,3.00,plan('6remise.mp4',4,1.04,1.0)))
shots.append((32.24,3.00,plan('1hero.mp4',3,1.0,1.05,0.55,0.55)))
shots.append((35.24,3.80,plan('rge.mp4',2,1.0,1.05)))

@shot(39.04,11.46)
def fin(k,n):   # fond du carton final : le bureau réel (écran Cercle Énergie), très flou, bleu nuit
    bg=grade_real(R2.get(70+int(k*0.12)))
    bg=cv2.GaussianBlur(cv2.resize(bg,(480,270),interpolation=cv2.INTER_AREA),(0,0),4)
    bg=cv2.resize(bg,(OW,OH),interpolation=cv2.INTER_CUBIC).astype(np.float32)
    bg=bg*0.30+np.array([75,38,7],np.float32)*0.70
    return np.clip(bg,0,255).astype(np.uint8)

TOTAL=50.5; N=int(round(TOTAL*FPS))
ff=subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","bgr24","-s",f"{OW}x{OH}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","medium","-crf","13","-pix_fmt","yuv420p",f"{W}/out/base.mp4"],stdin=subprocess.PIPE)
starts=[round(t0*FPS) for t0,_,_ in shots]
for f in range(N):
    # plan courant = dernier plan commencé ; fondu sur les XF premières images du plan suivant
    i=max(j for j,s in enumerate(starts) if s<=f)
    t0,d,fn=shots[i]; n=round(d*FPS); k=f-starts[i]
    fr=fn(k,n)
    if i+1<len(shots) and f>=starts[i+1]-XF:   # anticipation du plan suivant
        pass
    if i>0 and k<XF:
        tp,dp,fp=shots[i-1]; kp=f-starts[i-1]; np_=round(dp*FPS)
        a=(k+1)/(XF+1); fr=cv2.addWeighted(fp(kp,np_),1-a,fr,a,0)
    ff.stdin.write(fr.tobytes())
    if f%100==0: print(f,'/',N,flush=True)
ff.stdin.close(); ff.wait(); print('base ok',N,'images')
