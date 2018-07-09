#!/usr/bin/env python
import pika
import time
from ast import literal_eval

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='v1-2', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    # for converting str to dict
    result = literal_eval(body)

    if result['pass'] is True:
        # add camera to API
        print 'passed'
    else:
        print 'failed'
        print(result['data'])

    print(" [x] Done")
    
    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='v1-2')

channel.start_consuming()