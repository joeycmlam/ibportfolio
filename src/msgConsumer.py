import pika
import logging
import sys


p_host = 'localhost'
p_queue = 'Q_ORDER_T'

def on_message(ch, method, properties, body):
    msg = body.decode('UTF-8')
    logging.info('msg: [' + msg + ']')

def main():
    connection_params = pika.ConnectionParameters(host=p_host)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=p_queue)

    channel.basic_consume(queue=p_queue, on_message_callback=on_message, auto_ack=True)

    logging.info('subscribed to' + p_queue + ' waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    log_filename = '../log/consumer.log'
    logging.basicConfig(
        filename=log_filename, filemode='a',
        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO)
    try:
        logging.info('start')
        main()
        logging.info('completed.')
    except KeyboardInterrupt:
        logging.info('stop')
    except Exception as err:
        logging.error(err)
        sys.exit(-1)
    sys.exit(0)
