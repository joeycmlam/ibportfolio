import logging
import json
import pandas as pd
import xlwt
import dictUtil
import excelUtil


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data


def flatted(data) -> dict:
    record = {}
    for elm in data:
        record[elm] = data[elm]

    return record


def flattenRow(nestedRow, record, rows, parent, sep):

    for aRow in nestedRow:
        aCopyRecord = record.copy()
        for aCol in aRow:
            key = parent + sep + aCol
            aCopyRecord[key] = aRow[aCol]
        rows.append(aCopyRecord)

def denormalize(data) -> dict:
    logging.debug('DENORMALIZE')
    rows = []
    try:
        for row in data:
            record = {}
            nestedRow = {}
            for elm in row:
                value = row[elm]
                typeValue = type(value)
                if typeValue is list:
                    logging.debug('list')
                    parent = elm
                    nestedRow = denormalize(value)
                elif typeValue is dict:
                    nested = flatted(value)
                    record = dictUtil.Merge(record, nested)
                else:
                    record[elm] = value

            if len(nestedRow) > 0:
                flattenRow(nestedRow, record, rows, parent, '.')
            else:
                rows.append(record)
    except Exception as ex:
        logging.error('denormaized [%s]', ex)
        raise Exception(ex)

    return rows


def main():
    srcFile = 'sample-nest-list-mix.json'
    srcFullName = '../data/' + srcFile
    outFilePath = '../output/'
    outFileName = srcFile + '.xls'
    outFullName = outFilePath + outFileName

    try:
        jsonMsg = read_json(filename=srcFullName)
        table = denormalize(jsonMsg)
        write2excel(outFullName, 'output', table)
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('END')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    main()
