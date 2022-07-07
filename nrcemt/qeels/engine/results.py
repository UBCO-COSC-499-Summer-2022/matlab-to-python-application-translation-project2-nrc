import csv


def save_results(file_path, data):
    headers = [
        " ",
        "X1", "Y1",
        "X2", "Y2",
        "Width",
        "Results"
    ]
    with file_path as file:
        csv_writer = csv.writer(file)
        # Write titles
        csv_writer.writerow(headers)
        # Write Plasmons results
        csv_writer.writerow(data)
