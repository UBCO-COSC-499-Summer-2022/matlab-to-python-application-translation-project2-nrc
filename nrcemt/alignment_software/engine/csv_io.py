import csv

import numpy as np


def load_marker_csv(filename):
    marker_data = None
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if marker_data is None:
                marker_count = len(row) // 2
                marker_data = [[] for i in range(marker_count)]
            for i in range(marker_count):
                marker_position = (int(row[i*2]), int(row[i*2+1]))
                marker_data[i].append(marker_position)
    return np.array(marker_data)
