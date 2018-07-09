#!/usr/bin/env python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='v1', durable=True)

i = 0
with open('../CleanedGoodCameras2') as f:
    next(f)
    for line in f:
        cam = {}
        ret = {}
        data = line.split(',')
        cam['legacy_cameraID'] = data[0]
        cam['type'] = data[1]
        cam['source'] = data[2]
        cam['longitude'] = data[4]
        cam['latitude'] = data[3]
        cam['country'] = data[5]
        cam['state'] = data[6]
        cam['city'] = data[7]
        cam['resolution_width'] = data[8]
        cam['resolution_height'] = data[9]
        if (data[10] != 'null'):
            cam['utc_offset'] = data[10]

        cam['timezone_id'] = data[11]
        cam['timezone_name'] = data[12]
        cam['reference_logo'] = data[13]
        cam['reference_url'] = data[14]
        if (data[1] == "non_ip"):
            cam['snapshot_url'] = data[15]
            ret['snapshot_url'] = data[15]
        if (data[16] == 'True'):
            cam['is_active_image'] = True
        else:
            cam['is_active_image'] = False
        if (data[17] == 'True'):
            cam['is_active_video'] = True
        else:
            cam['is_active_video'] = False

        if (data[1] == 'non_ip'):
            cam['retrieval'] = ret
        else:
            ret['ip'] = None
            ret['port'] = 80
            ret['brand'] = None
            ret['model'] = None
            ret['image_path'] = None
            ret['video_path'] = None
            cam['retrieval'] = ret

        channel.basic_publish(exchange='',
                            routing_key='v1',
                            body=str(cam),
                            properties=pika.BasicProperties(
                                delivery_mode = 2, # make message persistent
                            ))
        print('camera No.' + str(i) + 'sent:\n' + line + '\n')
        i +=1
