import csv


def save_results(file_path, headers, data):
    """Saves the data to the provided file path"""
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        # Write titles
        csv_writer.writerow(headers)
        # Write Plasmons results
        csv_writer.writerows(data)
