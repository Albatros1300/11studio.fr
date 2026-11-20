# Détection de visages (YuNet, OpenCV) sur toutes les images d'un plan SDR -> JSON {frame:[[x,y,w,h,score],...]}
# usage : python3 detect_faces.py <video_sdr.mp4> <sortie.json> [seuil]
import cv2, json, sys, os
src,out=sys.argv[1],sys.argv[2]; thr=float(sys.argv[3]) if len(sys.argv)>3 else 0.45
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'models','yunet.onnx')
cap=cv2.VideoCapture(src); res={}; i=0
# deux passes : image entière à 1920 et image agrandie x1.5 par tuiles pour les petits visages
det=cv2.FaceDetectorYN.create(M,"",(1920,1080),thr,0.3,5000)
detT=cv2.FaceDetectorYN.create(M,"",(960,720),thr,0.3,5000)
while True:
    ok,f=cap.read()
    if not ok: break
    H,W=f.shape[:2]; boxes=[]
    det.setInputSize((W,H)); _,d=det.detect(f)
    if d is not None: boxes+= [[float(x) for x in r[:4]]+[float(r[-1])] for r in d]
    big=cv2.resize(f,None,fx=2,fy=2)
    for ty in range(0,2*H-720+1,540):
        for tx in range(0,2*W-960+1,480):
            t=big[ty:ty+720,tx:tx+960]; _,d=detT.detect(t)
            if d is not None:
                for r in d: boxes.append([float((r[0]+tx)/2),float((r[1]+ty)/2),float(r[2]/2),float(r[3]/2),float(r[-1])])
    res[i]=boxes; i+=1
json.dump(res,open(out,'w'))
print(src,i,'images', sum(len(v)>0 for v in res.values()),'avec visage')
