# Main + téléphone (carte des opportunités, page « 01 ») : on retrouve la position de l'image d'origine (avec son
# masque alpha) dans le rendu 300 dpi par corrélation, puis on découpe le rendu avec ce masque.
# usage : python3 cut_hand.py <rendu p-07.png> <i-008.png> <i-009.png masque> <sortie.png>
import cv2, numpy as np, sys
P,I,M,O=sys.argv[1:5]
page=cv2.imread(P); img=cv2.imread(I); msk=cv2.imread(M,0)
best=None
for sc in np.linspace(1.9,2.6,36):   # 135 ppi -> 300 dpi ≈ 2.22
    t=cv2.resize(img,None,fx=sc/4,fy=sc/4,interpolation=cv2.INTER_AREA)
    m=cv2.resize(msk,None,fx=sc/4,fy=sc/4,interpolation=cv2.INTER_AREA)
    pg=cv2.resize(page,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
    if t.shape[0]>pg.shape[0] or t.shape[1]>pg.shape[1]: continue
    r=cv2.matchTemplate(pg,t,cv2.TM_CCORR_NORMED,mask=cv2.merge([m,m,m]))
    _,v,_,loc=cv2.minMaxLoc(r)
    if best is None or v>best[0]: best=(v,sc,loc)
v,sc,loc=best; print('corr',v,'échelle',sc,'pos',loc)
H,W=page.shape[:2]
m=cv2.resize(msk,None,fx=sc,fy=sc,interpolation=cv2.INTER_CUBIC)
x0,y0=loc[0]*4,loc[1]*4
h,w=m.shape; x1,y1=min(x0+w,W),min(y0+h,H)
crop=page[y0:y1,x0:x1]; a=m[:y1-y0,:x1-x0]
a=cv2.erode(a,np.ones((3,3),np.uint8))
cv2.imwrite(O,np.dstack([crop,a]))
print(crop.shape)
