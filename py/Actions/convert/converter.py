import os

files = os.listdir('.')
for file in files:
    if file.endswith('.mp4') or file.endswith('.MOV'):
        os.popen(f"ffmpeg -i {file} -q:v 6 ./converted/{os.path.splitext(os.path.basename(file))[0]}.avi")
print('done.')