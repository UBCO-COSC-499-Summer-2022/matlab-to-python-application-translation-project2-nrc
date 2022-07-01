
def save_results(file, name, pos1, pos2, width, result, result_label):
    file.write(
        str(name) + ',' + str(pos1[0]) + ','
        + str(pos1[1]) + ',' + str(pos2[0]) + ','
        + str(pos2[1]) + ',' + str(width) + ','
        + str(result) + ',' + str(result_label) + '\n'
    )


# Creates the file writer aswell as writes the first two rows of data/headers
def init_file(average_pixel, file_path):
    file_path = file_path[0:len(file_path)-4]
    file = open(file_path + "_Results.csv", 'w')
    file.write('Average Pixel, ' + str(average_pixel) + ' \n')
    file.write(" ,X1,Y1,X2,Y2,Width,Results\n")
    return file


def close_reader(file):
    file.close()
