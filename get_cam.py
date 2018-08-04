"""this script use python client function 
to get all cameras from db and send them to queue for health checking.
"""
import pika
from CAM2CameraDatabaseAPIClient.client import Client

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='old', durable=True)

# initialize your client here

client = Client('admin', 'admin')

i = 0
while True:
    try:
        camera_list = client.search_camera(offset=i)
    except Exception as e:
        print e
        break
    if len(camera_list) == 0:
        break
    for camera in camera_list:
        channel.basic_publish(exchange='',
                            routing_key='old',
                            body=str(camera),
                            properties=pika.BasicProperties(
                                delivery_mode = 2, # make message persistent
                            ))
    i += 100