import csv
def save_results(file_path, data):
    with open(file_path+ "SENDSHELP.csv",'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)
