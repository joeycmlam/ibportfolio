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

    idxRow = 0
    for key, value in df.iterrows():
        newData = msgTemplate
        for col in value.index:
            if '.' in col:
                lstVal = col.split('.')
                newData[lstVal[0]][0][lstVal[1]] = value[col]
            else:
                newData[col] = value[col]
        fileOut.writelines(json.dumps(newData))
        idxRow = idxRow + 1

    fileOut.close()

def main(fileName, msgData, outputFile):
    logging.info('[{0}] [{1}] [{2}]'.format(fileName, msgData, outputFile))
    msgTemplate = readJson(fileName)
    populateData(msgTemplate, msgData, outputFile)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)
    logging.info('start')
    outfile = '{0}.{1}.json'.format('orders', datetime.datetime.today().strftime('%Y%m%d'))
    main('../data/order_sample.json', '../data/orders_multiple.xlsx', '../output/{0}'.format(outfile))
    logging.info('done')