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
    if len(res) == 0:
        p = True
    else:
        p = False

    # after the checking, send processed result to another queue
    result = {
        'pass': p,
        'data': cam
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
