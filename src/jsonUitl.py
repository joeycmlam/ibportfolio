import logging
import json
import pandas as pd
import xlwt
import dictUtil


def write2excel(fileName, sheetName, data):
    logging.info('write2excel: [%s][%s]', fileName, sheetName)
    wb = xlwt.Workbook()
    sh = wb.add_sheet(sheetName)

    try:
        logging.debug('write2excl')
        header = {}
        hRowId = 0

        # values
        rowId = 1
        for vRow in data:
            colId = 0
            for vCol in vRow:
                if vCol in header.keys():
                    pos = header[vCol]
                else:
                    pos = len(header)
                    header[vCol] = pos
                    sh.write(hRowId, pos, vCol)
                sh.write(rowId, pos, vRow[vCol])
                # colId += 1
            rowId += 1

    except Exception as ex:
        logging.error('write2excel: [%s]', ex)
        raise Exception(ex)
    finally:
        wb.save(fileName)


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


def duplciateRow(nestedRow, record, rows, parent, sep):

    for aRow in nestedRow:
        for aCol in aRow:
            key = parent + sep + aCol
            record[key] = aRow[aCol]
        rows.append(record)

def denormalize(data) -> dict:
    logging.debug('DENORMALIZE')
    rows = []
    record = {}
    nestedRow = []
    try:
        for row in data:
            record = {}
            for elm in row:
                logging.debug(elm)
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
                duplciateRow(nestedRow, record, rows, parent, '.')
            else:
                rows.append(record)
    except Exception as ex:
        logging.error('denormaized [%s]', ex)
        raise Exception(ex)

    return rows


def main():
    srcFile = 'sample-nest-list-multi-with-null.json'
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
                        level=logging.DEBUG)
    main()
