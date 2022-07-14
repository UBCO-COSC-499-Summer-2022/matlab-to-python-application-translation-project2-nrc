import csv


def save_results(file_path, headers, data):
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        # write headers to file
        csv_writer.writerow(headers)
        # write results
        csv_writer.writerows(data)
