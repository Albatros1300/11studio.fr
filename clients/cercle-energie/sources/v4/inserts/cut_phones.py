# Découpe des téléphones dans les pages du PDF rendues à 300 dpi : fond (bleu nuit ou cartes claires) relié au
# bord du cadre retiré par remplissage, bords adoucis -> PNG transparents.
# usage : python3 cut_phones.py <dossier_pages_png> <sortie>
import cv2, numpy as np, sys, os
P,O=sys.argv[1],sys.argv[2]; os.makedirs(O,exist_ok=True)
S=3.75  # vignette 1600x900 -> rendu 6000x3375
# nom, page, boîte approximative (coordonnées vignette x0,y0,x1,y1)
CUTS=[("qualif_photos","p-08.png",(1160,145,1512,848)),
      ("visite_pieces","p-09.png",(618,300,935,900)),
      ("visite_scan","p-09.png",(970,300,1286,900)),
      ("equipements","p-11.png",(777,145,1128,848))]
for name,pg,(x0,y0,x1,y1) in CUTS:
    im=cv2.imread(os.path.join(P,pg))
    X0,Y0,X1,Y1=[int(v*S) for v in (x0,y0,x1,y1)]
    c=im[Y0:Y1,X0:X1].copy(); h,w=c.shape[:2]
    b,g,r=[c[:,:,i].astype(int) for i in range(3)]
    luma=(0.11*b+0.59*g+0.3*r)
    bg=((b-r>22)|(luma>110)).astype(np.uint8)   # bleu nuit, turquoise, cartes blanches/vertes
    # remplissage depuis tous les pixels de bord qui sont « fond »
    mask=np.zeros((h+2,w+2),np.uint8); reach=np.zeros((h,w),np.uint8)
    seeds=[(x,0) for x in range(0,w,7)]+[(x,h-1) for x in range(0,w,7)]+[(0,y) for y in range(0,h,7)]+[(w-1,y) for y in range(0,h,7)]
    lab=bg.copy()*255
    for sx,sy in seeds:
        if lab[sy,sx]==255:
            cv2.floodFill(lab,mask,(sx,sy),128)
    phone=(lab!=128).astype(np.uint8)
    # garder la plus grande composante, boucher les trous
    n,L,st,_=cv2.connectedComponentsWithStats(phone)
    k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); phone=(L==k).astype(np.uint8)*255
    ff=phone.copy(); m2=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,m2,(0,0),255); phone|=cv2.bitwise_not(ff)
    phone=cv2.erode(phone,np.ones((5,5),np.uint8))
    a=cv2.GaussianBlur(phone,(0,0),1.6)
    ys,xs=np.where(a>0); c2=np.dstack([c,a])[ys.min():ys.max()+1,xs.min():xs.max()+1]
    cv2.imwrite(os.path.join(O,name+".png"),c2); print(name,c2.shape)
