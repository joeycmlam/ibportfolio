import json
import logging


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data


def normalize_json(data: dict) -> dict:
    new_data = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            new_data[key] = value
        else:
            for k, v in value.items():
                new_data[key + "_" + k] = v

    return new_data


def generate_csv_data(data: dict) -> str:
    # Defining CSV columns in a list to maintain
    # the order
    csv_columns = data.keys()

    # Generate the first row of CSV
    csv_data = ",".join(csv_columns) + "\n"

    # Generate the single record present
    new_row = list()
    for col in csv_columns:
        new_row.append(str(data[col]))

    # Concatenate the record with the column information
    # in CSV format
    csv_data += ",".join(new_row) + "\n"

    return csv_data


def write_to_file(data: str, filepath: str) -> bool:
    try:
        with open(filepath, "w+") as f:
            f.write(data)
    except:
        raise Exception(f"Saving data to {filepath} encountered an error")


def main():
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)

    try:
        # Read the JSON file as python dictionary
        data = read_json(filename="../data/sample.json")
        outFilename = "../output/data.csv"

        # Normalize the nested python dict
        allRecords = []
        for aRecord in data:
            new_data = normalize_json(data=aRecord)
            # Pretty print the new dict object
            print("New dict:", new_data)
            # Generate the desired CSV data
            csv_data = generate_csv_data(data=new_data)
            allRecords.extend(csv_data)


        # Save the generated CSV data to a CSV file
        write_to_file(data=allRecords, filepath=outFilename)

    except Exception as ex:
        logging.error(ex)
    finally:
        logging.info('Done')


if __name__ == '__main__':
    main()
