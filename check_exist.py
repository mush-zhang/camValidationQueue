
# TODO: we should add functionality to compare the new camera
# with existing camera of same retrieval (if there is any)
# and see if we need to update the existing one
# this function should return a camera object or None
# 1. no camera in db has the same ret with new camera
#    return old camera, this camera does not have id
# 2. identical camera already exist
#    return none.
# 3. there is camera in db that has the same ret with new camera
#    but new camera has more info.
#    return old camera with updated field(s).
#    this camera has camera ID.
# 4. if we get more than one identical cameras, write to error log.
import requests

def auth_token():
    # setup client
    clientID = 'admin'
    clientSecret = 'admin'
    url = 'http://localhost:8080/auth'
    param = {'clientID': clientID, 'clientSecret': clientSecret}
    response = requests.get(url, params=param)
    return response.json()['token']

def check_exist(**cam):
    ret_param = get_ret(**cam)
    token = None
    url = 'http://localhost:8080/cameras/exist/'
    if token is None:
        token = auth_token()
    header = {'Authorization': 'Bearer ' + str(token)}
    response=requests.get(url, headers=header, params=ret_param)
    if response.status_code == 401:
        check_exist(**ret_param)
    else:
        return response.json()

def get_ret(**cam):
    ret = {}
    ret['type'] = cam['type']
    if ret['type'] == 'ip':
        ret['port'] = cam['retrieval']['port']
        ret['image_path'] = cam['retrieval']['image_path']
        ret['video_path'] = cam['retrieval']['video_path']
    elif ret['type'] == 'non_ip':
        ret['snapshot_url'] = cam['retrieval']['snapshot_url']
    else:
        ret['m3u8_url'] = cam['retrieval']['m3u8_url']
    return ret
