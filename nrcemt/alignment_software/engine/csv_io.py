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


def write_marker_csv(filename, marker_data):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        marker_count = marker_data.shape[0]
        image_count = marker_data.shape[1]
        for i in range(image_count):
            row = []
            for m in range(marker_count):
                row.extend(marker_data[m][i])
            csvwriter.writerow(row)


def write_columns_csv(filename, columns):
    with open(filename, 'a+', newline='') as csvfile:
        csvfile.seek(0)
        dictreader = csv.DictReader(csvfile)
        fieldnames = dictreader.fieldnames
        if fieldnames is None:
            fieldnames = []
        rows = list(dictreader)
        for columnname, columndata in columns.items():
            if columnname not in fieldnames:
                fieldnames += [columnname]
            for i, value in enumerate(columndata):
                if value is None:
                    value = ""
                if i < len(rows):
                    rows[i][columnname] = value
                else:
                    rows.append({columnname: value})
            for i in range(len(columndata), len(rows)):
                rows[i][columnname] = ""
        csvfile.truncate(0)
        csvfile.seek(0)
        dictwriter = csv.DictWriter(csvfile, fieldnames)
        dictwriter.writeheader()
        while not any(rows[-1]):
            rows.pop()
        for row in rows:
            dictwriter.writerow(row)


def read_columns_csv(filename, columnnames):
    with open(filename, 'r', newline='') as csvfile:
        dictreader = csv.DictReader(csvfile)
        fieldnames = dictreader.fieldnames = dictreader.fieldnames
        intersection = list(set(fieldnames) & set(columnnames))
        if len(intersection) != len(columnnames):
            raise KeyError("not all columns are present in file")
        columns = {}
        for name in columnnames:
            columns[name] = []
        for row in dictreader:
            for name in columnnames:
                if name in row:
                    value = row[name]
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    columns[name].append(value)
                else:
                    columns[name].append(None)
        for name in columnnames:
            while len(columns[name]) > 0 and columns[name][-1] == "":
                columns[name].pop()
        return columns
