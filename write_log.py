"""
This file will be used for recording log messages when:
after result from health_worker is processed.

"""
# TODO: we should figure out how should we store the log
# store in file? csv?
# store in local mongodb or sql

def write_log(cam, op, health, cat, api_res):

    if op == 'write':

        if api_res.hasKey('cameraID') is True and cam.hasKey('cameraID') is False:
            print 'successfully add camera ' + api_res['cameraID']
        elif api_res.hasKey('cameraID') is True and cam.hasKey('cameraID') is True:
            print 'successfully update camera ' + api_res['cameraID']
        else:
            print 'error ' + api_res

    elif op == 'ignore':

        if cat == 'new':
            # when this new camera should not be added to the db
            print 'ignore ' + cam + ' because ' + str(health)

    else:
        print 'Error: Multiple cameras in db with same retrieval method.'

