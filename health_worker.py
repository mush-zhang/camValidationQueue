#!/usr/bin/env python
import pika
import time
from check_exist import check_exist
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

    # camera_exist checking

    res = check_exist(**cam)
    # TODO: we should write a scirpt to compare the new camera
    # with existing camera of same retrieval (if there is any)
    # and see if we need to update the existing one
    cat = 'new'
    # if we need to update the existing camera according to the new one
    # we should set 'cat' to 'old' and 'cam' to the modified camera (with cameraID)

    
    # camera health checkng by retrieving images


    # after the checking, send processed result to another queue
    result = {
        'health': {
            'exist': res,
            'active': False,
        },
        'cam': cam,
        'cat': cat
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
