import pika
import logging

p_host = 'localhost'
p_queue = 'Q_ORDER_T'


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(p_host))

    try:
        channel = connection.channel()
        channel.queue_declare(queue=p_queue)

        for i in range(0, 10):
            msg = 'order: ' + str(i)
            channel.basic_publish(exchange='', routing_key=p_queue, body=msg)
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
        main()
        logging.info('completed')
    except Exception as err:
        logging.error(err)
        sys.exit(-1)
