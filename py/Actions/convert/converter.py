import os

files = os.listdir('.')
for file in files:
    if file.endswith('.mp4'):
        os.popen(f"ffmpeg -i {file} -vcodec copy -acodec copy ./converted/{os.path.splitext(os.path.basename(file))[0]}.avi")
print('done.')