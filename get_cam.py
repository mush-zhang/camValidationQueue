"""this script use python client function 
to get all cameras from db and send them to queue for health checking.
"""
import pika
# also import the python client

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='old', durable=True)

# initialize your client here

client = Client('clientID', 'clientSecret')

i = 0
while True: 
    camera_list = client.search_camera(offset=i)
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