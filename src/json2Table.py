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
    row = {}  # dictionary
    for field in fields:
        row[field] = fields[field]
        addColumn(field)

    rows.append(row)

def newRow(aRow):
    logging.info('newRow')


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


def denormalizedRow(fields):
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
    for aRecord in jsonMsg:
        conv2Row(aRecord)

def flattenJson(jsonMsg):
    for aRecord in jsonMsg:
        denormalizedRow(aRecord)



def printTable():
    for aRecord in rows:
        pprint.pprint(aRecord)

def write2excel(fileName, sheetName):
    wb = xlwt.Workbook()
    sh = wb.add_sheet(sheetName)

    #header
    rowId = 0
    colId = 0
    for col in cols:
        sh.write(rowId, colId, col)
        colId += 1

    #content
    for row in rows:
        colId = 0
        rowId += 1
        for col in cols:
            sh.write(rowId, colId, row[col])
            colId += 1
    wb.save(fileName)

def main():
    try:
        data = utilJson.read_json(filename="../data/sample-nest-list.json")
        fileName = '../output/test2.xls'
        logging.info('Start')
        flattenJson(data)
        write2excel(fileName, 'Sheet1')
        logging.info('Done')
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('final.')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)
    main()
