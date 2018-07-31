from check_exist import auth_token
import requests


# Todo: Compare in pixel wise
def compare_cam(newCam, oldCam):
    """
    This function is to check if the new camera already existed in database.
    Retrieval method of a camera object is confirmed to be the same by check_exist function
    but there are other attributes like lat and long could be different between the old and new cam.
    If any of the old camera's attributes is null, we update it and return a camera object.
    Otherwise, return None.

    :param newCam:
        New camera object

    :param oldCam:
        Old camera object

    :return:
        Camera object or None.

    """
    updated = False
    for key, value in enumerate(oldCam):
        if key != 'retrieval' and value == 'null':
            oldCam[key] = newCam[key]
            updated = True
    if updated:
        return oldCam
    return None
