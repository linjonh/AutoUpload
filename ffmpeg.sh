#水印字体，并设置字体大小,和颜色为#808080
ffmpeg -y -i input.mp4 -filter_complex "[0:v]split=2[v1][v2]; [v1]trim=0:6,setpts=PTS-STARTPTS,drawtext=fontfile='simhei.ttf':fontsize=40:fontcolor=white:text='爵醒影视':x=20:y=20[v1out];  [v2]trim=6:12,setpts=PTS-STARTPTS,drawtext=fontfile='simhei.ttf':fontsize=40:fontcolor=white:text='爵醒影视':x=w-tw-20:y=h-th-20[v2out];  [v1out][v2out]concat=n=2:v=1:a=0[outv]" -map [outv] -map 0:a -c:a copy output.mp4

#卡点变速

ffmpeg -i input.mp4 -filter_complex "
[0:v]trim=start=0:end=0.5,setpts=PTS/2[v1];
[0:v]trim=start=0.5:end=0.8,setpts=PTS/3.5[v2];
[0:v]trim=start=0.8:end=1.5,setpts=PTS*5[v3];
[0:v]trim=start=1.5,setpts=PTS*5[v4];
[0:a]atrim=start=0:end=0.5,atempo=2.0[a1];
[0:a]atrim=start=0.5:end=0.8,atempo=2.0,atempo=1.75[a2];
[0:a]atrim=start=0.8:end=1.5,asetpts=PTS-STARTPTS,atempo=0.5,atempo=0.5,atempo=0.8[a3];
[0:a]atrim=start=1.5,asetpts=PTS-STARTPTS,atempo=0.5,atempo=0.5,atempo=0.8[a4];
[a1][a2][a3][a4]concat=n=4:v=0:a=1[outa];
[v1][v2][v3][v4]concat=n=4:v=1:a=0[outv];" -map [outv] -map [outa] output.mp4


ffmpeg -i input.mp4 -vf "setpts='PTS/(1+0.5*sin(PI*T/10))'" output.mp4
