import logging
import json
import pandas as pd

jsonFile = "../data/sample-nest.json"
outFilename = "../output/data-nest.xlsx"

def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data

def main():
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)
    try:
        data = read_json(filename="../data/sample-nest.json")
        df = pd.json_normalize(data, max_level=2)
        df.to_excel(outFilename)
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('Done')

def main_list():
    try:
        data = read_json(filename="../data/sample-nest-list.json")
        df = pd.json_normalize(data, max_level=2)
        df.to_excel(outFilename)
    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('Done')

if __name__ == '__main__':
    main_list()

