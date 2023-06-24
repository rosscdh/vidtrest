#!/usr/bin/sh
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "path to video file is required, $# provided"

ffmpeg  -i /src/media/video/fae1b8c5-43be-4cd2-b226-da56311e7760/german-ag-film-2023.mp4 -r 1 -s 320x200 -vsync passthrough -pix_fmt yuvj422p -an -vf select='gt(scene\,0.7)',showinfo thumbs-%02d.jpg  -f null - 2>&1 | grep 'pts_time' | awk -F'pts_time:' '{print $2}' | awk -F'pos:' '{print $1}' > thumbs_timestamp.txt

ffmpeg -i /src/media/video/fae1b8c5-43be-4cd2-b226-da56311e7760/german-ag-film-2023.mp4 -c:v copy -c:a copy german-ag-film-2023__.mp4

ffprobe -i /src/media/video/fae1b8c5-43be-4cd2-b226-da56311e7760/german-ag-film-2023.mp4 -select_streams v:0 -show_entries stream=start_time


ffmpeg -i /src/media/video/fae1b8c5-43be-4cd2-b226-da56311e7760/german-ag-film-2023.mp4 -ss 00:00:00 -vf scale=dstw=320:dsth=200:flags=accurate_rnd,setdar=3/1 -vcodec libx264  -level 21 -refs 2 -pix_fmt yuv420p -profile:v high -crf 10 -level 3.1 -color_primaries 1 -color_trc 1 -colorspace 1 -movflags +faststart -r 24 -an -sn -dn d.mp4