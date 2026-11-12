# Les logos détourés du site (logo_*_t.png) gardent un voile quasi blanc (253/255) sur leur fond :
# sur un carton blanc pur cela dessine un rectangle à peine visible. On rend ce voile transparent.
# usage : python3 clean_logos.py <dossier du site assets/img>
import sys, os
from PIL import Image
import numpy as np
src=sys.argv[1]; here=os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets')
for n in ['logo_mark_t.png','logo_full_t.png']:
    a=np.array(Image.open(os.path.join(src,n)).convert('RGBA')).astype(float)
    al=a[...,3:4]/255; comp=a[...,:3]*al+255*(1-al)
    out=np.concatenate([comp,np.full(al.shape,255.)],-1)
    out[comp.min(-1)>=249,3]=0
    Image.fromarray(out.round().astype('uint8')).save(os.path.join(here,n))
    print(n,'pixels rendus transparents :',int((out[...,3]==0).sum()))
