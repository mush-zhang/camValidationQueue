"""
******************************
Authors: Jia En Chua,
Last Updated on: 7/18/2018
******************************
Example on how to run:
    cam = {
        'type': 'ip',
        'is_active_image': 'False',
        'image_path': "http://207.251.86.238/cctv261.jpg"
    }
    cam = check_active(cam, duration)

"""

import getFramerate


def check_active(cam, duration):
    """
    To check if a cam is active, we determine if the frame rate is more than 0.
    To get the frame rate, we need 3 files: getFramerate.py, camera.py, stream_parser.py (logic flows in this order)
    Basically the program use urllib.open function to download a stream of jpeg images and determine the time between
    first and second image.(which is start and end image)
    If frame rate is determined, we then set is_active to True.

    set isActive
    :param cam:
        A camera object

    :return:
        A camera object

    """
    url = None
    if cam['type'] == 'ip':
        # we need to check both image and video path in the future
        url = cam['image_path']
        cam['is_active_video'] = False

    elif cam['type'] == 'non_ip':
        url = cam['snapshot_url']
        cam['is_active_video'] = False

    else:
        url = cam['m3u8_url']
        cam['is_active_image'] = True
    try:
        framerate = getFramerate.setup(url=url, duration=duration)
    except Exception as e:
        print e
        
    if framerate > 0:
        if cam['type'] == 'ip' or cam['type'] == 'non_ip':
            # we need to check both image and video path in the future
            cam['is_active_image'] = True
        else:
            cam['is_active_video'] = True

    return cam

