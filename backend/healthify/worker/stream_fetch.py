# import pika
#
# from healthify.utils import logger
# from healthify.config import PIKA_RABBITMQ_HOST, PIKA_RABBITMQ_TYPE
#
# __author__ = 'rahul'
#
#
# def fetch_stream_messages(**kwargs):
#     print 'in stream'
#     channel_name = kwargs.get('channel_name'.replace(" ", "-"), 'public')
#     message_stream = []
#     connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host=PIKA_RABBITMQ_HOST))
#     pika_channel = connection.channel()
#
#     pika_channel.exchange_declare(exchange=channel_name,
#                                   type=PIKA_RABBITMQ_TYPE)
#
#     result = pika_channel.queue_declare(exclusive=True)
#     queue_name = result.method.queue
#
#     pika_channel.queue_bind(exchange=channel_name,
#                             queue=queue_name)
#
#     def callback_function(ch, method, properties, body):
#         message_stream.append(body)
#         print(body)
#         # return message_stream
#
#
#     pika_channel.basic_consume(callback_function,
#                           queue=queue_name,
#                           no_ack=True)
#
#     pika_channel.start_consuming()
