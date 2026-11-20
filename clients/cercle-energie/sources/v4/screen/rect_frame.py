# Redresse une image dans l'espace du gabarit d'écran (avec marge) pour contrôle.
import cv2, numpy as np, sys, json
J,D,f,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]; mg=int(sys.argv[5]) if len(sys.argv)>5 else 60
j=json.load(open(J)); H=np.array(j['frames'][str(f)]['H'])
T=np.array([[1,0,mg],[0,1,mg],[0,0,1]],float)
im=cv2.imread(f"{D}/{f:04d}.jpg")
r=cv2.warpPerspective(im,T@np.linalg.inv(H),(j['TW']+2*mg,j['TH']+2*mg),flags=cv2.INTER_CUBIC)
cv2.rectangle(r,(mg,mg),(mg+j['TW'],mg+j['TH']),(0,255,0),1)
cv2.imwrite(out,r)
