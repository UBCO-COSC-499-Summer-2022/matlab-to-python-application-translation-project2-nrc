import os
import csv
from nanomi_optics.engine.save_results import save_csv

dirname = os.path.dirname(__file__)
test_filename = os.path.join(dirname, 'resources/test.csv')
output_filename = os.path.join(dirname, 'resources/output.csv')


def test_csv():
    col_1 = [1, 2, 3]
    col_2 = [4, 5, 6]
    col_3 = [7, 8, 9]
    col_act = [True, False, True]

    save_csv(
            col_1, col_act, col_2,
            col_1, col_act,
            col_3, col_2, 1,
            2, output_filename
        )
    test = []
    with open(test_filename, 'r') as csvfile:
        csv_test = csv.reader(csvfile)
        for row in csv_test:
            test.append(row)

    output = []
    with open(output_filename, 'r') as csvfile:
        csv_result = csv.reader(csvfile)
        for row in csv_result:
            output.append(row)

    print(test)
    print(output)

    assert test == output
