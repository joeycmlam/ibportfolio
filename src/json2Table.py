import logging
import utilJson
import pprint
import xlwt

rows = []
cols = set()


def addColumn(field):
    if field not in cols:
        cols.add(field)


def conv2Row(fields):
    try:
        row = {}  # dictionary
        for field in fields:
            row[field] = fields[field]
            addColumn(field)

        rows.append(row)
    except Exception as ex:
        logging.error(ex)
        raise Exception(ex)


def nestValues(prefix, nestedRows, aRow):
    logging.debug('nestedValue')
    i = 0
    for row in nestedRows:
        for field in row:
            aField = prefix + '.' + str(i) + '.' + field
            addColumn(aField)
            value = row[field]
            typeValue = type(value)
            if typeValue == list:
                nestValues(field, value, aRow)
            else:
                aRow[aField] = value
        i += 1


def flattenRow(fields):
    row = {}  # dictionary
    for field in fields:
        value = fields[field]
        typeValue = type(value)
        if typeValue == list:
            nestValues(field, value, row)
        else:
            addColumn(field)
            row[field] = value

    rows.append(row)


def convert2Table(jsonMsg):
    logging.info('convert2Table')
    try:
        for aRecord in jsonMsg:
            conv2Row(aRecord)
    except Exception as ex:
        logging.error(ex)
        raise Exception(ex)


def flattenJson(jsonMsg):
    logging.info('flattenJson')
    for aRecord in jsonMsg:
        flattenRow(aRecord)


def write2excel(fileName, sheetName):
    logging.info('write2excel: [%s][%s]', fileName, sheetName)
    wb = xlwt.Workbook()
    sh = wb.add_sheet(sheetName)

    # header
    rowId = 0
    colId = 0
    for col in cols:
        sh.write(rowId, colId, col)
        colId += 1

    try:
        # content
        for row in rows:
            colId = 0
            rowId += 1
            for col in cols:
                if col in row:
                    sh.write(rowId, colId, row[col])
                colId += 1
    except Exception as ex:
        logging.error('Error at rowid = %d colid = %d', rowId, colId)
        raise Exception (ex)
    finally:
        wb.save(fileName)


def main():
    try:
        data = utilJson.read_json(filename="../data/sample-nest-list-v2.json")
        fileName = '../output/test2.xls'
        logging.info('Start')
        # flattenJson(data)
        convert2Table(data)
        write2excel(fileName, 'Sheet1')
        logging.info('Done')
    except Exception as ex:
        logging.error(ex.with_traceback())
    finally:
        logging.info('final.')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)
    main()
