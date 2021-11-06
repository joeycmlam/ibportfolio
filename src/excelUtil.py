import logging
import xlwt

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
            for vCol in vRow:
                if vCol in header.keys():
                    pos = header[vCol]
                else:
                    pos = len(header)
                    header[vCol] = pos
                    sh.write(hRowId, pos, vCol)
                sh.write(rowId, pos, vRow[vCol])

            rowId += 1

    except Exception as ex:
        logging.error('write2excel: [%s]', ex)
        raise Exception(ex)
    finally:
        wb.save(fileName)

