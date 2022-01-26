import logging
import sys
import datetime
import json
import pandas

def readJson(fileName):
    logging.info(fileName)

    data = json.loads(open(fileName, "r").read())
    logging.debug(data)
    return data

def populateData(msgTemplate, msgData, p_outfile):
    # logging.info('{0} {1}'.format(msgTemplate, msgData))
    df = pandas.read_excel(msgData, sheet_name='data')
    fileOut = open(p_outfile, "w")

    try:
        idxRow = 0
        for key, value in df.iterrows():
            newData = msgTemplate
            for col in value.index:
                if '->' in col:
                    lstVal = col.split('->')
                    newData[lstVal[0]][0][lstVal[1]] = value[col]
                else:
                    newData[col] = value[col]
            fileOut.writelines('{0}{1}'.format(json.dumps(newData), '\n'))
            idxRow = idxRow + 1
    except Exception as err:
        logging.error(err)
        logging.error(value)
    finally:
        fileOut.close()

def main(fileName, msgData, outputFile):
    logging.info('[{0}] [{1}] [{2}]'.format(fileName, msgData, outputFile))
    msgTemplate = readJson(fileName)
    populateData(msgTemplate, msgData, outputFile)

if __name__ == '__main__':
    try:
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.DEBUG)
        logging.info('start')

        templateFile = '../config/order_sample.json'
        dataFile = '../data/orders_multiple.xlsx'
        outfile = '../output/{0}.{1}.json'.format('orders', datetime.datetime.today().strftime('%Y%m%d'))
        main(templateFile, dataFile, outfile)
    except Exception as err:
        logging.error(err)
        exit(-1)

    logging.info('done')
    exit(0)