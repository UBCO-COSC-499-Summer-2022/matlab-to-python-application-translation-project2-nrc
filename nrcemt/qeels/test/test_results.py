from nrcemt.qeels.engine.results import save_results
from tempfile import TemporaryDirectory
import os
import csv
import numpy as np


def test_save_results():
    headers = ['A', 'B', 'C', 'D', 'E']
    rand_data = [
        ['1', '1', '1', '1', '1', '1'],
        ['2', '2', '2', '2', '2', '2'],
        ['3', '3', '3', '3', '3', '3']
        ]

    written_file = [headers] + rand_data

    with TemporaryDirectory() as directory:
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

