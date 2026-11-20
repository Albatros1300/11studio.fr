# Remplacement du contenu de l'écran « Avenir Énergies » (IMG_1232) par un fond Cercle Énergie, en perspective suivie.
#  1. homographies gabarit->image (track_screen.py), images douteuses rejetées puis interpolées, lissage léger des coins
#  2. détourage de la tête qui passe devant l'écran : comparaison à l'écran de référence (médiane, sans la tête)
#     avec tolérance de décalage ; seuls les gros blocs (la tête) sont gardés
#  3. fond Cercle Énergie déformé par homographie, couleurs calées sur l'écran réel, léger flou + grain
# usage : python3 screen_replace.py <images_jpg> <track_raw.json> <f0> <f1> <sortie_png> [debug]
import cv2, numpy as np, json, sys, os
D,J,f0,f1,O=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
DBG=len(sys.argv)>6
HERE=os.path.dirname(os.path.abspath(__file__))
os.makedirs(O,exist_ok=True)
j=json.load(open(J)); fr=j['frames']
MG=60; TM=np.array([[1,0,MG],[0,1,MG],[0,0,1]],float)
ref=cv2.imread(os.path.join(HERE,'reference_ecran_median.png')).astype(np.float32)  # espace gabarit + marge 60
wall=cv2.imread(os.path.join(HERE,'wallpaper.png')).astype(np.float32)
WH,WW=wall.shape[:2]
# zone « bureau » (sans la barre des tâches) dans l'espace gabarit, rentrée de 3 px
desk=np.float32([[2,-4.5],[1271,-22.5],[1271,560],[2,709]])
G=cv2.getPerspectiveTransform(np.float32([[0,0],[WW,0],[WW,WH],[0,WH]]),desk)  # fond -> gabarit
TQ=np.float32([[0,0],[1280,0],[1280,720],[0,720]])

# --- 1. homographies validées, interpolées, lissées (via 4 points du gabarit)
def corners(H): return cv2.perspectiveTransform(TQ.reshape(-1,1,2),np.array(H)).reshape(-1,2)
C={}
for f in range(f0-6,f1+6):
    e=fr.get(str(f))
    if e and e['inliers']>=30: C[f]=corners(e['H'])
# rejet des sauts aberrants (écart > 12 px à la moyenne des voisins valides)
keys=sorted(C)
bad=set()
for k in keys:
    nb=[C[n] for n in (k-2,k-1,k+1,k+2) if n in C]
    if len(nb)>=2:
        if np.abs(C[k]-np.mean(nb,0)).max()>12: bad.add(k)
for k in bad: del C[k]
keys=sorted(C)
P={}
for f in range(f0-3,f1+3):
    if f in C: P[f]=C[f]; continue
    a=max([k for k in keys if k<f],default=None); b=min([k for k in keys if k>f],default=None)
    if a is None: P[f]=C[b]
    elif b is None: P[f]=C[a]
    else: t=(f-a)/(b-a); P[f]=C[a]*(1-t)+C[b]*t
S={f:(P[f-1]+2*P[f]+P[f+1])/4 for f in range(f0,f1)}
log={'rejetees':sorted(bad),'interpolees':[f for f in range(f0,f1) if f not in C]}
print('rejetées',log['rejetees'],'interpolées',log['interpolees'])
json.dump({str(f):S[f].tolist() for f in S},open(os.path.join(os.path.dirname(J),'screen_1232_corners_smoothed.json'),'w'))

k5=np.ones((5,5),np.uint8)
refB=cv2.GaussianBlur(ref,(0,0),1.2)
refMin=cv2.erode(refB,k5); refMax=cv2.dilate(refB,k5)
deskMaskT=np.zeros(ref.shape[:2],np.uint8)
cv2.fillPoly(deskMaskT,[np.round(desk+MG).astype(np.int32)],255)
# fond de l'écran de référence (hors logo) pour calage couleur
bgT=(deskMaskT>0)&(cv2.cvtColor(ref.astype(np.uint8),cv2.COLOR_BGR2HSV)[:,:,1]<60)&(ref.mean(2)>150)
rng=np.random.default_rng(7)
REFBG=np.median(ref[bgT],0)
for f in range(f0,f1):
    im=cv2.imread(f"{D}/{f:04d}.jpg").astype(np.float32); h,w=im.shape[:2]
    H=cv2.getPerspectiveTransform(TQ,np.float32(S[f]))           # gabarit -> image
    HT=H@np.linalg.inv(TM)                                          # gabarit+marge -> image
    rMin=cv2.warpPerspective(refMin,HT,(w,h),flags=cv2.INTER_LINEAR)
    rMax=cv2.warpPerspective(refMax,HT,(w,h),flags=cv2.INTER_LINEAR)
    dm=cv2.warpPerspective(deskMaskT,HT,(w,h),flags=cv2.INTER_LINEAR)
    bgm=cv2.warpPerspective(bgT.astype(np.uint8)*255,HT,(w,h),flags=cv2.INTER_NEAREST)
    imB=cv2.GaussianBlur(im,(0,0),1.2)
    # normalisation d'exposition : fond observé (pixels clairs du fond) / fond de la référence
    cand=im[bgm>0]; gcand=cand.mean(1); cand=cand[gcand>=np.percentile(gcand,55)]
    gref=np.median(cand,0)/REFBG
    rMin=rMin*gref[None,None,:]; rMax=rMax*gref[None,None,:]
    out_=np.maximum(rMin-imB,0)+np.maximum(imB-rMax,0)
    diff=out_.max(2)
    occ=((diff>26)&(dm>0)).astype(np.uint8)*255
    occ=cv2.morphologyEx(occ,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    # prolongement de la tête au-delà du bord de l'écran (évite un liseré au bord)
    ring=(cv2.dilate((dm>0).astype(np.uint8),np.ones((25,25),np.uint8))>0)&(dm==0)
    occ[ring&(cv2.dilate(occ,np.ones((25,25),np.uint8))>0)]=255
    n,lab,st,_=cv2.connectedComponentsWithStats(occ)
    keep=np.zeros_like(occ)
    for i in range(1,n):
        if st[i,cv2.CC_STAT_AREA]>2500: keep[lab==i]=255
    keep=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    # bouchage des trous intérieurs de la tête
    ff=keep.copy(); m2=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,m2,(0,0),255); keep=keep|cv2.bitwise_not(ff)
    # écran visible = bureau moins tête ; bords adoucis
    vis=((dm>127)&(keep==0)).astype(np.float32)
    vis=cv2.GaussianBlur(vis,(0,0),1.1)
    vis=np.minimum(vis,(dm/255.0))
    # calage couleur : gain par canal = fond réel observé / fond du gabarit
    sel=(bgm>0)&(keep==0)&(dm>250)
    if sel.sum()>500:
        obs=np.median(im[sel],0)
    else:
        obs=np.array([238,232,226.])
    gain=obs/np.array([251,247,244.])
    nw=cv2.warpPerspective(wall,H@G,(w,h),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_REPLICATE)
    nw=cv2.GaussianBlur(nw,(0,0),0.9)*gain[None,None,:]
    nw+=rng.normal(0,2.2,nw.shape).astype(np.float32)
    o=im*(1-vis[...,None])+nw*vis[...,None]
    cv2.imwrite(f"{O}/{f:04d}.png",np.clip(o,0,255).astype(np.uint8))
    if DBG:
        dbg=o.copy(); dbg[keep>0]=dbg[keep>0]*0.5+np.array([0,0,255.])*0.5
        cv2.polylines(dbg,[np.round(cv2.perspectiveTransform(desk.reshape(-1,1,2),H)).astype(np.int32)],True,(0,255,0),2)
        cv2.imwrite(f"{O}/dbg_{f:04d}.jpg",np.clip(dbg,0,255).astype(np.uint8))
print('ok',f0,f1)
