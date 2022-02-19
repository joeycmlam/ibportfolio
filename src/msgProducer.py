import logging
import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    try:
        channel = connection.channel()
        channel.queue_declare(queue='order')

        channel.basic_publish(exchange='',
                              routing_key='order',
                              body='Hello World!')
    except Exception as err:
        raise err
    finally:
        connection.close()

if __name__ == 'main':
    logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO)
    try:
        logging.info('start')
        main()
        logging.info('completed')
    except Exception as err:
        logging.error(err)
