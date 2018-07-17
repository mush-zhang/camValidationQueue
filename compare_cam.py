from check_exist import auth_token
import requests

def compare_cam(res):
    """
    Todo: Compare by pixel wise
    Retrieval method is confirmed to be the same by check_exist function
    but there are other attributes like lat and long could be different between the old and new cam.
    If they are different, we return a flag to let the health worker to use the new cam.

    :param res:
        New camera object
    :return:
        Boolean to tell if the cam's attributes are different
    """
    if len(res) == 0:
        return False
    token = None
    if res['cameraID'] == None:
        raise TypeError("Camera exists in db but cameraID not found!")
    url = 'http://localhost:8080/cameras/'+res['cameraID']
    if token is None:
        token = auth_token()
    header = {'Authorization': 'Bearer ' + str(token)}
    response = requests.get(url, headers=header)
    for key, value in enumerate(response.json()):
        if key != 'retrieval' and res[key] != value:
            return True
    return False