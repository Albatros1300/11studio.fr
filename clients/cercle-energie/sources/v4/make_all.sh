#!/bin/bash
# Chaîne complète V4 (ordre d'exécution). W = dossier de travail (intermédiaires lourds).
set -e
H=$(cd "$(dirname "$0")" && pwd)
U=/root/.claude/uploads/85fbdb28-8fac-5f9b-81ec-450efc44e123
W=${W:-/tmp/claude-0/-home-user-11studio-fr/85fbdb28-8fac-5f9b-81ec-450efc44e123/scratchpad/v4}
PDF=$U/d499406f-Hitachi_x_Cercle_e_nergie.pdf
mkdir -p $W/sdr $W/fr/1232 $W/fr/1234 $W/fr/1242 $W/pdf $W/pdfimg $W/audio $W/frames
# 1. vidéos iPhone HDR (HLG) -> SDR, puis images
for f in 93a47efd-IMG_1232 a9dcdd39-IMG_1234 70ed5d2a-IMG_1242; do n=${f#*-}
  ffmpeg -y -v error -i $U/$f.MOV -an -vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" -c:v libx264 -crf 12 -preset fast $W/sdr/$n.mp4
  ffmpeg -y -v error -i $W/sdr/$n.mp4 -start_number 0 -q:v 2 $W/fr/${n#IMG_}/%04d.jpg
  python3 $H/detect_faces.py $W/sdr/$n.mp4 $H/track/faces_raw_$n.json
done
# 2. écran « Avenir Énergies » remplacé (IMG_1232)
python3 $H/screen/make_wallpaper.py $H/screen/wallpaper.png
python3 $H/screen/track_screen.py $W/fr/1232 10 112 $H/track/screen_1232_raw.json
python3 $H/screen/screen_replace.py $W/fr/1232 $H/track/screen_1232_raw.json 36 108 $W/scr1232
# 3. visages floutés
python3 $H/blur_faces.py $W/fr/1234 jpg 0 50 $H/track/faces_raw_IMG_1234.json - $W/bl1234
python3 $H/blur_faces.py $W/scr1232 png 36 108 $H/track/faces_raw_IMG_1232.json - $W/bl1232a
python3 $H/blur_faces.py $W/fr/1232 jpg 150 260 $H/track/faces_raw_IMG_1232.json - $W/bl1232b
python3 $H/blur_faces.py $W/fr/1242 jpg 40 145 $H/track/faces_raw_IMG_1242.json - $W/bl1242
# 4. captures de l'application (PDF 300 dpi)
pdftoppm -r 300 -f 6 -l 15 -png $PDF $W/pdf/p; pdfimages -f 6 -l 14 -png $PDF $W/pdfimg/i
python3 $H/inserts/cut_phones.py $W/pdf $H/inserts/png
python3 $H/inserts/make_extra.py $W/pdfimg $W/pdf $H/inserts/png
# 5. images, textes, voix, mixage
V4SCR=$W python3 $H/build_base.py $W
(cd $H && node render.js frames $W/frames 0 1263)
python3 $H/build_vo.py $W/audio/vo_paced.wav 50.5
$H/final.sh $W /home/user/11studio.fr/clients/cercle-energie/materiel/audio/musique.mp3 /home/user/11studio.fr/clients/cercle-energie/cercle-energie-presentation-v4.mp4
