# Planche de contrôle : détections de visages dessinées sur les images f0..f1 (pas s), vignettes avec numéro d'image.
import cv2, json, sys, numpy as np
D,J,f0,f1,st,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
ext=sys.argv[7] if len(sys.argv)>7 else 'jpg'; cols=int(sys.argv[8]) if len(sys.argv)>8 else 5; tw=int(sys.argv[9]) if len(sys.argv)>9 else 560
j=json.load(open(J)) if J!='-' else {}
th=[]
for f in range(f0,f1,st):
    im=cv2.imread(f"{D}/{f:04d}.{ext}")
    for b in j.get(str(f),[]):
        x,y,w,h,s=b; c=(0,255,0) if s>=0.6 else (0,255,255)
        cv2.rectangle(im,(int(x),int(y)),(int(x+w),int(y+h)),c,3)
    im=cv2.resize(im,(tw,tw*9//16),interpolation=cv2.INTER_AREA)
    cv2.putText(im,str(f),(5,25),0,0.8,(0,0,0),4); cv2.putText(im,str(f),(5,25),0,0.8,(255,255,255),2)
    th.append(im)
while len(th)%cols: th.append(np.zeros_like(th[0]))
rows=[np.hstack(th[i:i+cols]) for i in range(0,len(th),cols)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
