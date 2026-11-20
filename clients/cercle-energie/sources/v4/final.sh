#!/bin/bash
# Mixage final V4 : images + calque de textes + voix + musique (atténuée sous la voix ; la commande
# d'atténuation est avancée de 0,2 s pour que la musique baisse avant chaque phrase).
# usage : final.sh <dossier_travail> <musique.mp3> <sortie.mp4>
set -e
W="$1"; MUS="$2"; OUT="$3"; D=50.5
ffmpeg -y -v error -i "$W/out/base.mp4" -framerate 25 -i "$W/frames/f_%05d.png" -i "$W/audio/vo_paced.wav" -i "$MUS" -filter_complex "
[0:v][1:v]overlay=format=auto,format=yuv420p[v];
[2:a]asplit=2[vo][sc0];
[sc0]atrim=start=0.2,asetpts=PTS-STARTPTS[sc];
[3:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=-14dB,afade=t=in:d=0.6,afade=t=out:st=47.6:d=2.9[m];
[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=650:makeup=1[md];
[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.89[a]" \
 -map "[v]" -map "[a]" -t $D -r 25 -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -ar 48000 "$OUT"
