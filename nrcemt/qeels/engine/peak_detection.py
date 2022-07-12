import math
from matplotlib.pyplot import switch_backend
import numpy as np
from nrcemt.alignment_software.engine.img_processing import(
    rotate_transform,
    transform_img
)
# Constants
# PLANCK_CONSTANT = 4.1357*10 ^ (-15)
# SPEED_LIGHT = 3*10 ^ (8)
# Q_PIXEL = 0.001165934*10 ^ (9)

# PROBS should rename this when i have a better understanding of the functionality
# performs a searies of angle calculations i think

def calculate_positions(x1, y1, x2, y2, width):
    res = []
    tilt_angle = math.atan((y1-y2)/(x1-x2)*-1)
    # #1 values
    # Not sure why rounded???? nor how mutch rounding so am going to leave for now
    x_calculated = x1+width/2*math.sin(tilt_angle)
    y_calculated = y1+width/2*math.cos(tilt_angle)
    res.append([x_calculated, y_calculated])

    x_calculated = x1-width/2*math.sin(tilt_angle)
    y_calculated = y1-width/2*math.cos(tilt_angle)
    res.append([x_calculated, y_calculated])

    # #2 values
    x_calculated = x2+width/2*math.sin(tilt_angle)
    y_calculated = y2+width/2*math.cos(tilt_angle)
    res.append([x_calculated, y_calculated])

    x_calculated = x2-width/2*math.sin(tilt_angle)
    y_calculated = y2-width/2*math.cos(tilt_angle)
    res.append([x_calculated, y_calculated])

    return res
# Change later,
def peak_detection(plasmon_array, width_array, results_array, spectrogram):
    # retrieve average pixel, ev/pixel, microrad/pixel
    average_pixel = results_array[3].result_var.get()
    e_dispersion = results_array[0].result_var.get()
    q_dispersion_upper = results_array[1].result_var.get()

    # loop through different rows
    for i in range(0, 6, 2):
        # retrieve data for more use later on
        x1 = plasmon_array[i].x_var.get()
        y1 = plasmon_array[i].y_var.get()
        x2 = plasmon_array[i+1].x_var.get()
        y2 = plasmon_array[i+1].y_var.get()
        width = width_array[int(i/2)].width_var.get()
        detect = width_array[int(i/2)].detect_var.get()
        [spectrogram_width, spectrogram_height] = np.shape(spectrogram)

        # Needs better names
        is_filled_1 = x1 > 0 or y1 > 0
        is_filled_2 = x2 > 0 or y2 > 0

        # if both values are entered
        if detect and is_filled_1 and is_filled_2:
            # Peak finding tolerance
            tolerance = 1.01
            # Confidence number
            cn = 2

            # DOUBLE CHECK, BUT I DONT THINK THE RESULT FROM THIS ARE USED
            calculated = calculate_positions(x1, y1, x2, y2, width)

            delta_x = x1-x2
            delta_y = y1-y2

            rotation_angle_rad = math.atan(delta_x/delta_y)
            rotation_angle_degrees = math.degrees(rotation_angle_rad)

            # apply rotation to the points
            x1 = (x1-spectrogram_width/2) * math.cos(rotation_angle_rad) + (y1 - spectrogram_height/2)*math.sin(rotation_angle_rad)*-1 + spectrogram_height/2
            y1 = (x1-spectrogram_width/2) * math.sin(rotation_angle_rad) + (y1 - spectrogram_height/2)*math.cos(rotation_angle_rad)*-1 + spectrogram_height/2
            x2 = (x2-spectrogram_width/2) * math.cos(rotation_angle_rad) + (y2 - spectrogram_height/2)*math.sin(rotation_angle_rad)*-1 + spectrogram_height/2
            y2 = (x2-spectrogram_width/2) * math.sin(rotation_angle_rad) + (y2 - spectrogram_height/2)*math.cos(rotation_angle_rad)*-1 + spectrogram_height/2

            # rotate image so plasmon is vertical???
            rotation_matrix = rotate_transform(rotation_angle_degrees*-1, 0, 0)
            spectrogram_rotated = transform_img(spectrogram, rotation_matrix)


            # Find absolute value of image
            spectrogram_signal = np.absolute(spectrogram_rotated)

            # Ensure y1 is less than y2
            if y1 > y2:
                temp = y1
                y1 = y2
                y2 = temp

            #loops through rows of box
            for j in range(int(y1), int(y2)):
                print(j)

        else:
            return
