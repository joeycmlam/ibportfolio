import pika
import logging


p_host = 'myhost01'
p_queue = 'q_order'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=p_host))
    channel = connection.channel()

    channel.queue_declare(queue=p_queue)

    def callback(ch, method, properties, body):
        logging.info(" [x] Received %r" % body)

    channel.basic_consume(queue=p_queue, on_message_callback=callback, auto_ack=True)

    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    logging.basicConfig(
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
