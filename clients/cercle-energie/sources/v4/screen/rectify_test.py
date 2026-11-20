import cv2, numpy as np, sys
F=sys.argv[1]; out=sys.argv[2]
src=np.float32([[192,557],[681,528],[704,809],[215,838]])
W,H=1280,720
dst=np.float32([[0,0],[W,0],[W,H],[0,H]])
M=cv2.getPerspectiveTransform(src,dst)
im=cv2.imread(F)
r=cv2.warpPerspective(im,M,(W+0,H+0),flags=cv2.INTER_CUBIC)
cv2.imwrite(out,r)
