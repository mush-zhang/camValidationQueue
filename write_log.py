"""
This file will be used for recording log messages when:
after result from health_worker is processed.

"""
# TODO: we should figure out how should we store the log
# store in file? csv?
# store in local mongodb or sql

def write_log(cam, op, health, cat, api_res):

    if op == 'add':

        if api_res.hasKey('cameraID'):
            print 'successfully add camera ' + api_res['cameraID']
        else:
            print 'error ' + api_res

    elif op == 'update':
        
        if api_res.hasKey('cameraID'):
            print 'successfully updated camera ' + api_res['cameraID']
        else:
            print 'error ' + api_res

    elif op == 'ignore':

        if cat == 'new':
            # when this new camera should not be added to the db
            print 'ignore ' + cam + ' because ' + str(health)

        elif cat == 'old':
            # when an old camera is working correctly
            print 'camera ' + cam['cameraID'] + ' works fine.'
        else:
            print 'error'
    else:
        print 'error'

