from ffmpy import FFmpeg

ff = FFmpeg(inputs={'IMG_0827.mp4': None}, outputs={"Icons/Thumbnail.png": ['-ss', '00:00:4', '-vframes', '1']})

print (ff.cmd)

# Print result
# ffmpeg -i input.mp4 -ss 00:00:10 -vframes 1 output.png

ff.run()