from getFramerate import *


def check_active(cam):
    url = None
    if cam['type'] == 'ip':
        url = cam['video_path']
    elif cam['type'] == 'non_ip':
        url = cam['snapshot_url']
    else:
        url = cam['m3u8_url']

    framerate = setup(url=url, duration=60)
    print(framerate)
    if framerate > 0:
        return True
    return False


if __name__ == "__main__":
    cam = {
        'type': 'non_ip',
        'snapshot_url': "http://www.nestcamdirectory.com/view.php?cam=147"
        # 'snapshot_url': "http://207.251.86.238/cctv290.jpg"
    }
    print(check_active(cam))
