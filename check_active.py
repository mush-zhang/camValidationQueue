from getFramerate import *


def check_active(cam):
    """
    To check if a cam is active, we determine if the frame rate is more than 0.
    To get the frame rate, we need 3 files: getFramerate.py, camera.py, stream_parser.py (logic flows in this order)
    Basically the program use urllib.open function to download a stream of jpeg images and determine the time between
    first and second image.(which is start and end image)

    :param cam:
        A camera object

    :return:
        A boolean to tell if the camera is active

    """
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
