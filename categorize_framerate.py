import getFramerate
import client

url = "http://207.251.86.238/cctv290.jpg"
duration = 60
framerate = getFramerate.setup(url=url, duration=duration)

category = 0
if framerate == 1:
    category = 1
elif framerate <= 5:
    category = 5
elif framerate <= 10:
    category = 10
elif framerate <= 30:
    category = 30
elif framerate <= 60:
    category = 60
elif framerate <= 300:
    category = 300
elif framerate <= 600:
    category = 600
elif framerate <= 1200:
    category = 1200
elif framerate <= 1800:
    category = 1800
elif framerate > 1800:
    category = 3600

kwargs = {'camera_type': 'ip', 'frame_rate': category, 'video_path': 'path/video'}
client = client.Client()
client.write_camera(**kwargs)