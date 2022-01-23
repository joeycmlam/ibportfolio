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

    for key, value in df.iterrows():
        newData = msgTemplate
        logging.info('before: {0}'.format(newData))
        newData['funds'][0]['fund_id'] = value['funds.fund_id']
        newData['funds'][0]['txn_type'] = value['funds.txn_type']
        newData['funds'][0]['unit'] = value['funds.unit']
        for col in value.index:
            newData[col] = value[col]
        fileOut.writelines(str(newData))
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
    main('../data/order_sample.json', '../data/orders.xlsx', '../output/{0}.txt'.format(outfile))
    logging.info('done')