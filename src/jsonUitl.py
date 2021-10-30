import json
import logging

def denormalize(Data=jsonMsg):
    logging.debug('DENORMALIZE')


def main():
    srcFile = 'sample-nest-list-multi-with-null.json'
    srcFullName = '../data/' + srcFile

    data = read_json(filename=srcFullName)
    denormalize(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    main()