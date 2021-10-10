import logging


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename='../log/ibportfolio.log', format=FORMAT, level=logging.DEBUG)

    logging.debug('debug test')
    logging.info('start!')

    logging.info('completed!')