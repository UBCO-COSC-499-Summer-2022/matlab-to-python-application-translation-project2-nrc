import csv


def save_results(file_path, headers, data):

    with file_path as file:
        csv_writer = csv.writer(file)
        # Write titles
        csv_writer.writerow(headers)
        # Write Plasmons results
        csv_writer.writerows(data)
