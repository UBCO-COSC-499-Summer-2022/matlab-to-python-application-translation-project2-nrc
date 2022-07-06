import csv
import os
def save_results(file_path, data):
    headers = [
        " ",
        "X1", "Y1",
        "X2", "Y2",
        "Width",
        "Results"
    ]
    dir_path = os.path.dirname(file_path)
    new_path = os.path.join(dir_path, "qEELS_Results.csv")

    with open(new_path, 'w', newline='\n') as file:
        csv_writer = csv.writer(file)
        # Write titles
        csv_writer.writerow(headers)

        # Write Plasmons results
        csv_writer.writerows(data)
