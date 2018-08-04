import pika
"""
This file will be used for recording log messages when:
after result from health_worker is processed.

"""
# TODO: we should figure out how should we store the log
# store in file? csv?
# store in local mongodb or sql

# currently a file. only one worker open. 
from ast import literal_eval

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='log', durable=True)

def callback(ch, method, properties, body):

    result = literal_eval(body)

    with open('health_log', 'a') as log_file:

        if result.hasKey('error'):
            log_file.write(result['error'])
        elif result['op'] == 'write':
            if result['cam'].hasKey('cameraID') is False:
                log_file.write('successfully add camera ' + result['api_res'])
            else:
                log_file.write('successfully update camera ' + result['api_res'])

        elif result['op'] == 'ignore':

            if result['cat'] == 'new':
                # when this new camera should not be added to the db
                log_file.write( 'ignore ' + result['cam'] + ' because ' + str(result['cam']['health'])

        else:
            log_file.write( 'Error: Multiple cameras in db with same retrieval method.')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='log')

channel.start_consuming()