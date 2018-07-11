#!/usr/bin/env python
import pika
import time
from ast import literal_eval
from write_log import write_log

"""
This file process the results passed from health worker after checking new cameras:

    cam: dict
        The camera infor, containing all fields required for API interaction.

    health: dict
        Results from health checking functions. cameraID?
        This should be checked when op='ignore' for logging why this camera is not saved.
        It should have 2 fields:
            exist: specify if there is already a camera with same retrieval method.
            active: if the camera is working.
    cat: str
        category of the camera, whether new or old
"""

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='v1-2', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    # for converting str to dict
    result = literal_eval(body)

    # decide on operations to take
    # op: str
    #    Operation to take. 
    #    Operation can be 'create', 'update', or 'ignore'.

    if result['cat'] == 'new':
        if (result['health']['exist'] == []]) and (result['health']['active'] is True):
            result['op'] = 'add'
        else:
            result['op'] = 'ignore'

    elif result['cat'] == 'old':
        if result['health']['active'] is True:
            result['op'] = 'ignore'
        else:
            result['op'] = 'update'
            # we should also modify the camera object here
            # set its 'is_active_*' fields to False
    else:
        print 'error'

    result['api_res'] = None
    if result['op'] == 'add':
        # this is where we add the camera to db with python client
        # api response should be added recorded here.

        print 'add with API'

    elif result['op'] == 'update':
        # this is where we update the camera to db with python client
        # api response should be added recorded here.
        
        print 'update'
    
    write_log(**result)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='v1-2')

channel.start_consuming()