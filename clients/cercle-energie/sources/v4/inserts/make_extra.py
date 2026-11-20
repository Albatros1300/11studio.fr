# - Téléphone « carte des opportunités » : capture d'écran du PDF (page 01 Opportunités) dans un cadre de téléphone dessiné.
# - Écran PC « Analyse automatique » (page 07 Montage et suivi) : découpe du contenu de l'écran dans le rendu 300 dpi.
# - Masquage du nom du particulier dans l'en-tête de la capture « photos » (page 02).
# usage : python3 make_extra.py <dossier_pdfimg> <dossier_pages> <sortie>
from PIL import Image, ImageDraw, ImageFilter
import sys, os
I,P,O=sys.argv[1:4]
# téléphone dessiné
scr=Image.open(os.path.join(I,'i-006.png')).convert('RGB')
k=3; sw,sh=scr.width*k,scr.height*k
scr=scr.resize((sw,sh),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2))
b=46; W,H=sw+2*b,sh+2*b; R=150
ph=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ph)
d.rounded_rectangle((0,0,W-1,H-1),R,fill=(12,12,14,255))
d.rounded_rectangle((6,6,W-7,H-7),R-6,outline=(58,60,66,255),width=3)
m=Image.new('L',(sw,sh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,sw-1,sh-1),R-b+8,fill=255)
ph.paste(scr,(b,b),m)
# l'île du téléphone est déjà visible dans la capture (barre d'état) : on ne dessine qu'une petite pastille
d=ImageDraw.Draw(ph); d.rounded_rectangle((W//2-150,b+20,W//2+150,b+100),40,fill=(8,8,10,255))
ph.save(os.path.join(O,'carte_opportunites.png'))
# écran PC
pg=Image.open(os.path.join(P,'p-14.png')).convert('RGB')
S=3.75; pc=pg.crop((int(549*S),int(281*S),int(1486*S),int(810*S)))
pc.save(os.path.join(O,'pc_analyse.png'))
# nom masqué sur la capture « photos »
q=Image.open(os.path.join(O,'qualif_photos.png')).convert('RGBA')
from PIL import ImageFont
c=q.getpixel((380,180)); dq=ImageDraw.Draw(q); dq.rectangle((215,128,1050,250),fill=c)
fnt=ImageFont.truetype('/home/user/11studio.fr/clients/cercle-energie/sources/v3/assets/montserrat-latin-600-normal.woff2',44)
dq.text((632,182),'Bilan maison',font=fnt,fill=(28,28,32,255),anchor='mm')
q.save(os.path.join(O,'qualif_photos.png')); print('nom masqué, couleur',c)
