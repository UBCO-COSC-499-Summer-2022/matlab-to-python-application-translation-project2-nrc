from nrcemt.qeels.engine.results import save_results
from tempfile import TemporaryDirectory
import os
import csv
import numpy as np


def test_save_results():
    headers = ['A', 'B', 'C', 'D', 'E']
    rand_data = []
    for i in range(0, 3):
        rand_data.append(to_str(np.random.rand(6).tolist()))
    written_file = [headers] + rand_data

    with TemporaryDirectory('w+r') as directory:
        # Save temp data
        temp_path = os.path.join(directory, "tempFile.csv")
        save_results(temp_path, headers, rand_data)

        # Read temp data
        with open(temp_path, 'r') as temp:
            read_file = []
            csv_reader = csv.reader(temp)
            for lines in csv_reader:
                read_file.append(lines)

        # assert values
        assert written_file == read_file


def to_str(array):
    for i in range(len(array)):
        array[i] = str(array[i])
    return array
