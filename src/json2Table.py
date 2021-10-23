import logging
import utilJson
import pprint

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

def nestValues(prefix, nestedRows, aRow, level):
    logging.debug('nestedValue')
    i = 0
    for row in nestedRows:
        # need to clone a new row
        for field in row:
            aField = prefix + '.' + str(i) + '.' + field
            addColumn(aField)
            value = row[field]
            typeValue = type(value)
            if typeValue == list:
                nestValues(field, value, 1)
            else:
                aRow[aField] = value
        i += 1


def denormalizedRow(fields):
    row = {}  # dictionary
    for field in fields:
        value = fields[field]
        typeValue = type(value)
        if typeValue == list:
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
        pprint.pprint(aRecord)

def main():
    try:
        data = utilJson.read_json(filename="../data/sample-nest-list.json")
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
