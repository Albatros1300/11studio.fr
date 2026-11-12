#!/bin/bash
# Mixage final V2 : plans + calque de textes + voix + musique (atténuée sous la voix).
# usage : final.sh <dossier_travail> <musique.mp3>
set -e
W="$1"; MUS="$2"; D=63
ffmpeg -y -v error -i "$W/out/base.mp4" -framerate 24 -i "$W/frames/f_%05d.png" -i "$W/audio/vo_paced.wav" -i "$MUS" -filter_complex "
[0:v][1:v]overlay=format=auto,format=yuv420p[v];
[2:a]apad=whole_dur=$D,asplit=2[vo][sc];
[3:a]atrim=0:$D,volume=-7dB,afade=t=in:d=0.4,afade=t=out:st=60.8:d=2.2[m];
[m][sc]sidechaincompress=threshold=0.015:ratio=7:attack=25:release=450:makeup=1[md];
[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.89[a]" \
 -map "[v]" -map "[a]" -t $D -r 24 -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 256k -ar 48000 "$W/out/cercle-energie-presentation-v2.mp4"
