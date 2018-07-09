import requests

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJRCI6ImFkbWluIiwicGVybWlzc2lvbkxldmVsIjoiYWRtaW4iLCJpYXQiOjE1Mjc2NzM0NTgsImV4cCI6MTUyNzY3Mzc1OH0.8EUV_kL02YJRmPl2YHtVIsSrAg3LEGVLq0h0kfl4368"
def get_new_token(clientID,clientSecret):
    url = 'https://cam2-api-test.herokuapp.com/auth/?clientID=admin&clientSecret=admin'
    response = requests.get(url)
    print("new token ={} ".format(response.json()))
    return response.json()['token']

def do(line,token):
    global auth_token
    clientID="admin"
    clientSecret="admin"
    auth_token = token
    hed = {'Authorization': 'Bearer ' + auth_token}
    cam = {}
    geo = {}
    ret = {}
    data = line.split(',')
    # print(data)
    cam['legacy_cameraID'] = data[0];
    cam['type'] = data[1];
    cam['source'] = data[2];
    cam['longitude'] = data[4];
    cam['latitude'] = data[3];
    #  geo['type']="Point"
    #   geo['coordinates']=[data[4],data[3]]#(lng,lat)
    # cam['geometry']=geo
    # cam.geometry.type = "Point";
    # cam.geometry.coordinates = [data[4], data[3]];
    cam['country'] = data[5];
    cam['state'] = data[6];
    cam['city'] = data[7];
    cam['resolution_width'] = data[8];
    cam['resolution_height'] = data[9];
    if (data[10] != 'null'):
        cam['utc_offset'] = data[10];

    cam['timezone_id'] = data[11];
    cam['timezone_name'] = data[12];
    cam['reference_logo'] = data[13];
    cam['reference_url'] = data[14];
    if (data[1] == "non_ip"):
        cam['snapshot_url'] = data[15]
        ret['snapshot_url'] = data[15]
    if (data[16] == 'True'):
        cam['is_active_image'] = 'true'
    else:
        cam['is_active_image'] = 'false'
    if (data[17] == 'True'):
        cam['is_active_video'] = 'true'
    else:
        cam['is_active_video'] = 'false'

    if (data[1] == 'non_ip'):
        cam['retrieval'] = ret
    else:
        ret['ip'] = 'null'
        ret['port'] = 'null'
        ret['brand'] = 'null'
        ret['model'] = 'null'
        ret['image_path'] = 'null'
        ret['video_path'] = 'null'
        cam['retrieval'] = ret

    data = cam
    url = 'https://cam2-api-test.herokuapp.com/cameras/create'
    # print(data)
    # response = requests.post(url, json=data)
    response = requests.post(url, json=data, headers=hed)
    if(response.status_code==409):
        return
    if(response.status_code==401):
        print(response)
        auth_token=get_new_token(clientID,clientSecret)
        do(line,auth_token)
    print(response)
    #print(response.json())

def main():

    global auth_token
    hed = {'Authorization': 'Bearer ' + auth_token}
    i = 1
    with open('CleanedGoodCameras2') as f:
        next(f)
        for line in f:
            if(i >= 797):
                do(line,auth_token)
            i += 1


main()
#response = requests.post(url, json=data, headers=hed)
# response = requests.get(url, params=data)
# print(response)
# print(len(response.json()))
# print(response.json())
