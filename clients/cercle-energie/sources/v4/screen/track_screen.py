# Suivi de l'écran (contenu plan) de IMG_1232 : homographie gabarit->image par SIFT + RANSAC, image par image.
# Le gabarit est l'écran redressé à l'image 75 (coins posés à la main), cheveux exclus par un polygone.
# usage : python3 track_screen.py <dossier_images_jpg> <f0> <f1> <sortie.json>
import cv2, numpy as np, sys, json
D,f0,f1,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
src=np.float32([[192,557],[681,528],[704,809],[215,838]]); TW,TH=1280,720
dst=np.float32([[0,0],[TW,0],[TW,TH],[0,TH]])
M=cv2.getPerspectiveTransform(src,dst)
ref=cv2.imread(f"{D}/0075.jpg")
tpl=cv2.warpPerspective(ref,M,(TW,TH),flags=cv2.INTER_CUBIC)
tmask=np.full((TH,TW),255,np.uint8)
hair=np.int32([[560,720],[640,520],[720,400],[800,250],[950,130],[1100,110],[1280,140],[1280,720]])
cv2.fillPoly(tmask,[hair],0); tmask[:3,:]=0; tmask[-25:,:]=0
sift=cv2.SIFT_create(nfeatures=4000,contrastThreshold=0.02)
g=lambda im:cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
kt,dt=sift.detectAndCompute(g(tpl),tmask)
bf=cv2.BFMatcher()
Hinit=np.linalg.inv(M)  # gabarit -> image 75
res={}; prevH=None
def solve(fr,Hguess):
    # zone de recherche : quadrilatère prédit, élargi
    q=cv2.perspectiveTransform(dst.reshape(-1,1,2),Hguess).reshape(-1,2)
    x0,y0=np.maximum(q.min(0)-160,0).astype(int); x1,y1=np.minimum(q.max(0)+160,[1919,1079]).astype(int)
    m=np.zeros(fr.shape[:2],np.uint8); m[y0:y1,x0:x1]=255
    kf,df=sift.detectAndCompute(g(fr),m)
    if df is None or len(kf)<8: return None,0
    mt=bf.knnMatch(dt,df,k=2); good=[a for a,b in (p for p in mt if len(p)==2) if a.distance<0.78*b.distance]
    if len(good)<10: return None,len(good)
    A=np.float32([kt[m.queryIdx].pt for m in good]); B=np.float32([kf[m.trainIdx].pt for m in good])
    H,inl=cv2.findHomography(A,B,cv2.RANSAC,3.0,maxIters=5000,confidence=0.999)
    if H is None: return None,0
    n=int(inl.sum())
    # raffinement : ré-estimation sur inliers (moindres carrés)
    H2,_=cv2.findHomography(A[inl.ravel()==1],B[inl.ravel()==1],0)
    return H2,n
order=list(range(75,f1))+list(range(74,f0-1,-1))
Hs={}
for f in order:
    fr=cv2.imread(f"{D}/{f:04d}.jpg")
    guess=Hs.get(f-1 if f>75 else f+1,Hinit)
    H,n=solve(fr,guess)
    if H is None: print(f,'ÉCHEC',n); continue
    Hs[f]=H; res[f]={'H':H.tolist(),'inliers':n}
    q=cv2.perspectiveTransform(dst.reshape(-1,1,2),H).reshape(-1,2)
    print(f,n,np.round(q).astype(int).tolist())
json.dump({'template_src':src.tolist(),'TW':TW,'TH':TH,'frames':res},open(out,'w'))
