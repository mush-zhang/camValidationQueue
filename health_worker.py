#!/usr/bin/env python
import pika
import time
from utils.check_exist import check_exist
from utils.check_active import check_active
from ast import literal_eval

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='v1', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    # for converting str to dict
    cam = literal_eval(body)

    # should go through checking here
    
    # initialize 'exist' and 'active' to false
    exist = 'unchecked'
    active = 'unchecked'

    # camera active checking
    # initialize duration for checking to run (if checking ran too long, it raises error)
    duration = 10
    cam = check_active(cam, duration)
    active = cam['is_active_image'] or cam['is_active_video']

    # camera_exist checking

    # this fucntion should check if a new camera exist in db.
    # the returned value is None if already exist
    # returning a camera without camera id means that we add new camera
    # returning a camera with camera id means that we update old camera
    res = check_exist(**cam)

    # if returning an old camera
    if len(res) > 1 :
        op = 'error'
        cam = None
        exist = True
    elif len(res) == 1 and res[0].hasKey('camera_ID') is True:
        op = 'write' # combine add and update to one fucntion
        cam = res[0]
        exist = True
    elif len(res) == 1 and res[0].hasKey('camera_ID') is False:
        # new camera that does not exist on db
        # camera health checkng by retrieving images
        exist = False
        active = False

        if active is True:
            op = 'write'
        else:
            op = 'ignore'
    else:
        exist = False
        op = 'ignore'


    # after the checking, send processed result to another queue
    result = {
        'health': {
            'exist': exist,
            'active': active,
        },
        'cam': cam,
        'op': op,
        'cat': 'new'
    }
    result_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    result_channel = result_connection.channel()
    result_channel.queue_declare(queue='v1-2', durable=True)
    channel.basic_publish(exchange='',
                        routing_key='v1-2',
                        body=str(result),
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))

    print(" [x] Done")
    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='v1')

channel.start_consuming()
