import csv
import json
import random


def csv_to_dict(csv_file) -> list:
    """
    Opens a CSV file, first line are keys for dict
    Every other line becomes a dict in the returned list
    :param csv_file: path to csv file
    :return: list of dicts
    """
    csv_dict = {}
    csv_list = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        line_count = 0
        for line in reader:
            if line_count == 0:
                # get first line as keys
                line_count += 1
                keys = line
            else:
                key_count = 0
                for key in keys:
                    csv_dict[key] = line[key_count]
                    key_count += 1
                csv_list.append(json.dumps(csv_dict))
    line_count = 0
    for line in csv_list:
        csv_list[line_count] = json.loads(line)
        line_count += 1
    return csv_list


def generate_random(length: int):
    chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*()?'
    pw = ''.join(random.sample(chars, length))
    return pw
