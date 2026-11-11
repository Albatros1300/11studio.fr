set -e
ffmpeg -y -v error -i out/base.mp4 -framerate 24 -i mg/frames/f_%05d.png -i audio/vo_paced.wav -i audio/music2.mp3 -filter_complex "
[0:v][1:v]overlay=format=auto,format=yuv420p[v];
[2:a]apad=whole_dur=72,asplit=2[vo][sc];
[3:a]atrim=0:72,volume=-7dB,afade=t=in:d=0.4,afade=t=out:st=70.6:d=1.4[m];
[m][sc]sidechaincompress=threshold=0.015:ratio=7:attack=25:release=450:makeup=1[md];
[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.89[a]" \
 -map "[v]" -map "[a]" -t 72 -r 24 -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 256k -ar 48000 out/cercle-energie-presentation.mp4
