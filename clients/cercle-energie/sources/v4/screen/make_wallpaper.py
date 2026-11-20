# Fond d'écran Cercle Énergie (1920x1032 = bureau Windows sans barre des tâches) posé à la place de l'écran d'origine.
from PIL import Image, ImageDraw
import sys
A='/home/user/11studio.fr/clients/cercle-energie/sources/v3/assets/logo_full_t.png'
W,H=1920,1032
im=Image.new('RGB',(W,H),(244,247,251))
# léger dégradé radial clair
d=ImageDraw.Draw(im)
logo=Image.open(A); s=1100/logo.width; logo=logo.resize((1100,int(logo.height*s)),Image.LANCZOS)
im.paste(logo,((W-logo.width)//2,(H-logo.height)//2-10),logo)
im.save(sys.argv[1])
