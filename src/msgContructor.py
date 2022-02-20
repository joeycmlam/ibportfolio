import logging
import sys
import datetime
import json
import pandas
import copy
import time

def readJson(fileName):
    logging.info(fileName)

    data = json.loads(open(fileName, "r").read())
    logging.debug(data)
    return data

def get_value(col, value):
    if '{current_timestamp}' == value[col]:
        rtn_value = str(datetime.datetime.now().isoformat())
    elif '{epoch_id}' == value[col]:
        rtn_value = time.time_ns()
    else:
        rtn_value = value[col]

    return rtn_value

def populate_row (targetData, value, prevMsgId, lstNewItems):
    curMsgId = value['msgId']

    newItem = {}
    for col in value.index:
        if '->' in col:
            lstVal = col.split('->')
            if curMsgId != prevMsgId:
                targetData[lstVal[0]][0][lstVal[1]] = get_value(col, value)
            else:
                if (lstVal[0] in lstNewItems.keys()):
                    newItem = lstNewItems[lstVal[0]]
                else:
                    newItem = {}

                newItem[lstVal[1]] = get_value(col, value)
                lstNewItems[lstVal[0]] = newItem

        elif '.' in col:
            lstVal = col.split('.')
            targetData[lstVal[0]][lstVal[1]] = get_value(col, value)
        elif col in targetData:
            targetData[col] = get_value(col, value)

    return targetData

def populate_data(df, msgTemplate, p_file):
    row_id = 0
    prev_msg_id = 0
    newData = {}
    try:
        p_file.write('[')
        for key, value in df.iterrows():
            curMsgId = value['msgId']
            logging.info('row {0}'.format(row_id))
            lstNewItems = {}

            if row_id != 0 and prev_msg_id != curMsgId:
                p_file.writelines('{0}{1},'.format(json.dumps(newData), '\n'))

            if prev_msg_id != curMsgId:
                newData = copy.deepcopy(msgTemplate)

            newData = populate_row(newData, value, prev_msg_id, lstNewItems)

            if prev_msg_id == curMsgId:
                for key, aItem in lstNewItems.items():
                    newData[key].append(aItem)

            row_id = row_id + 1
            prev_msg_id = curMsgId
        #end for-loop

        p_file.writelines('{0}{1}]'.format(json.dumps(newData), '\n'))
    except Exception as err:
        logging.error(err)
        logging.error('row {0} col {1} value {2}'.format(row_id, col, value))
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