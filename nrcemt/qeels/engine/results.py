

def save_results(file, name, pos1, pos2, width, result, result_label):
    file.write(str(name) +','+ str(pos1[0]) +',' + str(pos1[1]) +','+ str(pos2[0]) +','+str(pos2[1]) +','+ str(width) +','+ str(result) + ',' +str(result_label)+'\n')
    # file.write("Bulk Plasmon,A,B,C,D,E,F, ev/Pixel\n")
    # file.write("Surface Plasmon Upper,G,H,I,J,K,L, microRad/Pixel\n")
    # file.write("Surface Plasmon Lower,1,2,3,4,5,6, microRad/Pixel")


def init_file(average_pixel):
    file = open('qeels.csv', 'w')
    file.write('Average Pixel, '+ str(average_pixel)+' \n')
    file.write(" ,X1,Y1,X2,Y2,Width,Results\n")
    return file


def close_reader(file):
    file.close()
