#!/usr/bin/env python

import sys
from os import path
sys.path.append(path.dirname(path.abspath(__file__)))
import pika
import time
from utils.check_exist import check_exist
from utils.check_active import check_active
from ast import literal_eval

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='old', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    # for converting str to dict
    cam = literal_eval(body)

    # should go through checking here
    
    # camera active checking
    # initialize duration for checking to run (if checking ran too long, it raises error)
    duration = 10
    new_cam = check_active(cam, duration)

    if new_cam['is_active_image'] != cam['is_active_image'] or new_cam['is_active_video'] != cam['is_active_video']:
        op = 'write'
    else:
        op = 'ignore'

    # after the checking, send processed result to another queue
    result = {
        'cam': new_cam,
        'op': op,
        'cat': 'old'
    }
    result_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    result_channel = result_connection.channel()
    result_channel.queue_declare(queue='result', durable=True)
    channel.basic_publish(exchange='',
                        routing_key='result',
                        body=str(result),
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))

    print(" [x] Done")
    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='old')

channel.start_consuming()
