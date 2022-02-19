import pika
import logging

p_host = 'myhost01'
p_queue = 'q_order'


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(p_host))

    try:
        channel = connection.channel()
        channel.queue_declare(queue=p_queue)

        channel.basic_publish(exchange='',
                              routing_key=p_queue,
                              body='Hello World!')
    except Exception as err:
        raise err
    finally:
        connection.close()

if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO)
    try:
        logging.info('start')
        # main()
        logging.info('completed')
    except Exception as err:
        logging.error(err)
