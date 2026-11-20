# Contrôle : relance la détection de visages sur les images traitées ; liste les visages encore détectés
# (score >= seuil) qui ne sont pas couverts par une zone floutée (boxes.json du dossier).
# usage : python3 check_faces.py <dossier_traité> <f0> <f1> [seuil]
import cv2, json, sys, os, numpy as np
D,f0,f1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); thr=float(sys.argv[4]) if len(sys.argv)>4 else 0.6
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'models','yunet.onnx')
det=cv2.FaceDetectorYN.create(M,"",(1920,1080),thr,0.3,5000); detT=cv2.FaceDetectorYN.create(M,"",(960,720),thr,0.3,5000)
B=json.load(open(os.path.join(D,'boxes.json')))
bad=[]
for f in range(f0,f1):
    im=cv2.imread(f"{D}/{f:04d}.png"); H,W=im.shape[:2]; found=[]
    _,d=det.detect(im)
    if d is not None: found+=[r[:4].tolist()+[float(r[-1])] for r in d]
    big=cv2.resize(im,None,fx=2,fy=2)
    for ty in range(0,2*H-720+1,540):
        for tx in range(0,2*W-960+1,480):
            _,d=detT.detect(big[ty:ty+720,tx:tx+960])
            if d is not None: found+=[[(r[0]+tx)/2,(r[1]+ty)/2,r[2]/2,r[3]/2,float(r[-1])] for r in d]
    for x,y,w,h,s in found:
        cx,cy=x+w/2,y+h/2
        cov=any(abs(cx-bx)<bw*0.8 and abs(cy-by)<bh*0.9 for bx,by,bw,bh in B.get(str(f),[]))
        if not cov: bad.append((f,round(cx),round(cy),round(w),round(s,2)))
print(D,'visages non couverts :',len(bad))
for b in bad: print(b)
