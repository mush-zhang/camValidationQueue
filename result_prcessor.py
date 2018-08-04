#!/usr/bin/env python
import pika
import time
from ast import literal_eval
from CAM2CameraDatabaseAPIClient.client import Client

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

channel.queue_declare(queue='result', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    # for converting str to dict
    result = literal_eval(body)

    # decide on operations to take
    # op: str
    #    Operation to take. 
    #    Operation can be 'write', or 'ignore'.

    if result['op'] == 'write':
        # call api method here to create/update camera

        try:
            result['api_res'] = client.write_camera(**result['cam'])
        except Exception as e:
            result['error'] = e
    # other results are processed in write log   

    result_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    result_channel = result_connection.channel()
    result_channel.queue_declare(queue='log', durable=True)
    channel.basic_publish(exchange='',
                        routing_key='log',
                        body=str(result),
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='result')

channel.start_consuming()