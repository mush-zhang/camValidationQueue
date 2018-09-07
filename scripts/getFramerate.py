"""
Description:
    This script determine the camera's frame rate by calling functions in camera.py and stream_parser.py

How to run:
    url = "http://207.251.86.238/cctv290.jpg"
    duration = 60
    framerate = setup(url=url, duration=duration)

"""


from __future__ import print_function
import os
import camera as importCameras
import time
import shutil


def assessFramerate(camera, duration):
    start_timestamp = time.time()
    framerate = 0
    try:
        while framerate == 0 and (duration > 0 and (time.time() - start_timestamp) < duration):
            camera.get_start_image()
            framerate = camera.get_end_image_and_framerate()
    except Exception as e:
        raise e

    return framerate


def setup(url=None, duration=None):
    if os.path.isdir("Pictures"):
        shutil.rmtree('Pictures')
    try:
        os.makedirs('Pictures')
    except OSError:
        raise OSError("Directory already existed")

    camera = importCameras.Camera(url=url)

    try:
        camera.get_ref_image()
    except Exception as e:
        raise e

    try:
        framerate = assessFramerate(camera, duration)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    return framerate


