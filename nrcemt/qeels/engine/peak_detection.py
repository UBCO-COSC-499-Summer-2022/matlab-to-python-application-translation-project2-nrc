import math
from matplotlib.pyplot import switch_backend
import numpy as np
from nrcemt.alignment_software.engine.img_processing import(
    rotate_transform,
    transform_img
)
from scipy import signal
import scipy
from scipy.io import loadmat
# Constants
# PLANCK_CONSTANT = 4.1357*10 ^ (-15)
# SPEED_LIGHT = 3*10 ^ (8)
# Q_PIXEL = 0.001165934*10 ^ (9)

# PROBS should rename this when i have a better understanding of the functionality
# performs a searies of angle calculations i think


def compute_rect_corners(x1, y1, x2, y2, width):
    res = []
    tilt_angle = 0
    if x1 != x2:
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
def peak_detection(plasmon_array, width_array, results_array, detect_array, spectrogram):

    # retrieve average pixel, ev/pixel, microrad/pixel
    average_pixel = results_array[3]
    e_dispersion = results_array[0]
    q_dispersion_upper = results_array[1]

    # loop through different rows
    for i in range(0, 6, 2):
        # retrieve data for more use later on
        x1 = plasmon_array[i][0]
        y1 = plasmon_array[i][1]
        x2 = plasmon_array[i+1][0]
        y2 = plasmon_array[i+1][1]
        width = width_array[int(i/2)]
        detect = detect_array[int(i/2)]
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
            calculated_corners = compute_rect_corners(x1, y1, x2, y2, width)

            delta_x = x1-x2
            delta_y = y1-y2

            rotation_angle_rad = math.atan2(delta_y, delta_x)
            rotation_angle_degrees = math.degrees(rotation_angle_rad)

            rotation_angle_rad, rotation_angle_degrees = calc_angle(
                x1, y1,
                x2, y2
            )

            # apply rotation to the points
            x1, y1, x2, y2 = rotate_points(
                x1, y1, x2, y2,
                rotation_angle_rad,
                spectrogram_width,
                spectrogram_height
            )

            # rotate image so plasmon is vertica
            spectrogram_rotated = scipy.ndimage.rotate(
                spectrogram,
                rotation_angle_degrees*-1,
                reshape = False
            )

            # Find absolute value of image
            spectrogram_signal = np.absolute(spectrogram_rotated)

            # Ensure y1 is less than y2
            if y1 > y2:
                temp = y1
                y1 = y2
                y2 = temp

            #loops through rows of box
            print(np.sum(spectrogram_signal))
            for j in range(int(y1), int(y2)):
                # mean of the row?
                spectrogram_ycfit = ycfit(
                    spectrogram_signal,
                    average_pixel,
                    j, width, x1
                )

                index, _ = signal.find_peaks(spectrogram_ycfit, threshold=tolerance)

        else:
            pass


# potentially rename
def ycfit(signal, average_pixel, it, width, x1):
    signal_sect = signal[
        int(it-average_pixel):int(it+average_pixel),
        int(x1-width/2):int(x1+width/2)
    ]
    signal_sect = signal_sect/np.sum(signal)
    ycfit = np.mean(signal_sect, axis=1)
    return ycfit


def calc_angle(x1, y1, x2, y2):
    delta_x = x1-x2
    delta_y = y1-y2

    rotation_angle_rad = math.atan2(delta_y, delta_x)
    rotation_angle_degrees = math.degrees(rotation_angle_rad)

    return(rotation_angle_rad, rotation_angle_degrees)


def rotate_points(x1, y1, x2, y2, rotation_angle_rad, width, height):
    x1_height = (x1-width/2) * math.cos(rotation_angle_rad)
    x1_width = (y1 - height/2)*math.sin(rotation_angle_rad)*-1
    x1 = x1_height + x1_width + height/2

    y1_width = (x1-width/2) * math.sin(rotation_angle_rad)
    y1_height = (y1 - height/2)*math.cos(rotation_angle_rad)
    y1 = y1_width + y1_height + height/2

    x2_height = (x2-width/2) * math.cos(rotation_angle_rad)
    x2_width = (y2 - height/2)*math.sin(rotation_angle_rad)*-1
    x2 = x2_height + x2_width + height/2

    y2_width = (x2-width/2) * math.sin(rotation_angle_rad)
    y2_height = (y2 - height/2)*math.cos(rotation_angle_rad)
    y2 = y2_width + y2_height + height/2

    return (x1, y1, x2, y2)
