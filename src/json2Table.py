import logging
import utilJson

cols = set()
rows = []


def addColumn(field):
    if field not in cols:
        cols.add(field)


def conv2Row(fields):
    row = {}  # dictionary
    for field in fields:
        row[field] = fields[field]
        addColumn(field)

    rows.append(row)

def nestValues(prefix, fields, aRow, level):
    for field in fields:
        aField = prefix + '.' + field
        addColumn(aField)
        value = fields[field]
        typeValue = type(value)
        if typeValue == dict:
            nestValues(field, value, 1)
        else:
            aRow[aField] = value


def denormalizedRow(fields):
    row = {}  # dictionary
    for field in fields:
        value = fields[field]
        typeValue = type(value)
        if typeValue == dict:
            nestValues(field, value, row, 1)
        else:
            addColumn(field)
            row[field] = value



    rows.append(row)

def convert2Table(jsonMsg):
    for aRecord in jsonMsg:
        conv2Row(aRecord)

def denormalizedJson(jsonMsg):
    for aRecord in jsonMsg:
        denormalizedRow(aRecord)


def printTable():
    for aRecord in rows:
        logging.info(aRecord)

def main():
    try:
        data = utilJson.read_json(filename="../data/sample-nest.json")
        logging.info('Start')
        denormalizedJson(data)
        printTable()
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
