import logging
import sys
import datetime
import json
import pandas
import copy

def readJson(fileName):
    logging.info(fileName)

    data = json.loads(open(fileName, "r").read())
    logging.debug(data)
    return data


def get_value(col, value):
    if '{current_timestamp}' == value[col]:
        rtnValue = str(datetime.datetime.now());
    elif '{epoch_id}' == value[col]:
        rtnValue = datetime.datetime.now().timestamp()
    else:
        rtnValue = value[col]

    return rtnValue

def populate_data(df, msgTemplate, p_file):

    try:
        p_file.write('[')
        rowId = 0
        prevMsgId = 0
        newData = {}
        for key, value in df.iterrows():
            curMsgId = value['msgId']
            logging.info('row {0}'.format(rowId))
            lstNewItems = {}
            newItem = {}

            if rowId != 0 and prevMsgId != curMsgId:
                p_file.writelines('{0}{1}'.format(json.dumps(newData), '\n'))
                p_file.write(',')

            if prevMsgId != curMsgId:
                newData = copy.deepcopy(msgTemplate)

            for col in value.index:
                if '->' in col:
                    lstVal = col.split('->')
                    if curMsgId != prevMsgId:
                        newData[lstVal[0]][0][lstVal[1]] = get_value(col, value)
                    else:
                        if (lstVal[0] in lstNewItems.keys()):
                            newItem = lstNewItems[lstVal[0]]
                        else:
                            newItem = {}

                        newItem[lstVal[1]] = get_value(col, value)
                        lstNewItems[lstVal[0]] = newItem

                elif '.' in col:
                    lstVal = col.split('.')
                    newData[lstVal[0]][lstVal[1]] = get_value(col, value)
                elif col in newData:
                    newData[col] = get_value(col, value)

            if prevMsgId == curMsgId:
                for key, aItem in lstNewItems.items():
                    newData[key].append(aItem)


            rowId = rowId + 1
            prevMsgId = curMsgId

        p_file.writelines('{0}{1}'.format(json.dumps(newData), '\n'))
        p_file.write(']')
    except Exception as err:
        logging.error(err)
        logging.error('row {0} col {1} value {2}'.format(rowId, col, value))
    finally:
        p_file.close()

def main(fileName, msgData, outputFile):
    try:
        logging.info('[{0}] [{1}] [{2}]'.format(fileName, msgData, outputFile))
        msgTemplate = readJson(fileName)
        df = pandas.read_excel(msgData, sheet_name='data')
        fileOut = open(outputFile, "w")
        populate_data(df, msgTemplate, fileOut)
    except Exception as err:
        logging.error(err)
        raise err


if __name__ == '__main__':
    try:
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.DEBUG)
        logging.info('start')

        templateFile = '../config/order_sample.json'
        dataFile = '../data/orders_w_id.xlsx'
        outfile = '../output/{0}.{1}.json'.format('orders', datetime.datetime.today().strftime('%Y%m%d'))
        main(templateFile, dataFile, outfile)
    except Exception as err:
        logging.error(err)
        exit(-1)

    logging.info('done')
    exit(0)