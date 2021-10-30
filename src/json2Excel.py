import logging
import json
import pandas as pd
import xlwt



def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data

def write2excel(fileName, sheetName, data):
    logging.info('write2excel: [%s][%s]', fileName, sheetName)
    wb = xlwt.Workbook()
    sh = wb.add_sheet(sheetName)

    try:
        logging.debug('write2excl')

        #header
        colId = 0
        rowId = 0
        for hCol in data.columns:
            sh.write(rowId, colId, hCol)
            colId += 1

        #values
        rowId += 1
        for vRow in data.values:
            colId = 0
            for vCol in vRow:
                sh.write(rowId, colId, vCol)
                colId += 1
            rowId += 1

    except Exception as ex:
        logging.error('write2excel: [%s]', ex)
        raise Exception (ex)
    finally:
        wb.save(fileName)


def main():
    try:

        srcFile = 'sample-nest-list-multi-with-null.json'
        srcFullName = '../data/' + srcFile
        outFilePath = '../output/'
        outFileName = srcFile + '.xls'
        outFullName = outFilePath + outFileName

        data = read_json(filename=srcFullName)

        # df = pd.json_normalize(data)

        df = pd.json_normalize(data,
                               meta=['id', 'firstName', 'lastName', 'country', ['contacts', 'email'],
                                     ['contacts', 'Mob']]
                               , max_level=1, sep='.'
                               , record_path=['funds'])

        write2excel(outFullName, 'S1', df)
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('Done')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    main()
