import math
import numpy as np
import scipy
import scipy.signal


def compute_rect_corners(x1, y1, x2, y2, width):
    res = []
    tilt_angle = 0
    if x1 != x2:
        tilt_angle = math.atan((y1-y2)/(x1-x2)*-1)
    # 1 values
    x_calculated = x1+width/2*math.sin(tilt_angle)
    y_calculated = y1+width/2*math.cos(tilt_angle)
    res.append([round(x_calculated), round(y_calculated)])

    x_calculated = x1-width/2*math.sin(tilt_angle)
    y_calculated = y1-width/2*math.cos(tilt_angle)
    res.append([round(x_calculated), round(y_calculated)])

    # 2 values
    x_calculated = x2-width/2*math.sin(tilt_angle)
    y_calculated = y2-width/2*math.cos(tilt_angle)
    res.append([round(x_calculated), round(y_calculated)])

    x_calculated = x2+width/2*math.sin(tilt_angle)
    y_calculated = y2+width/2*math.cos(tilt_angle)
    res.append([round(x_calculated), round(y_calculated)])
    return res


def ycfit(signal, average_pixel, it, width, x1, sum):
    signal_sect = signal[
        int(it-average_pixel):int(it+average_pixel+1),
        int(x1-width/2):int(x1+width/2+1)
    ]
    signal_sect = signal_sect/sum
    ycfit = np.mean(signal_sect, axis=0)
    ycfit = ycfit[:].reshape(1, width+1)

    return ycfit


def calc_angle(x1, y1, x2, y2):
    delta_x = x1-x2
    delta_y = y1-y2

    # SHE DOES tan(x/y) in her code so is x/y in ours too ... for now
    rotation_angle_rad = math.atan2(delta_x, delta_y)
    rotation_angle_degrees = math.degrees(rotation_angle_rad)
    return(rotation_angle_rad, rotation_angle_degrees)


def rotate_points(x1, y1, x2, y2, rotation_angle_rad, width, height):
    x1_height = (x1-width/2)*math.cos(rotation_angle_rad)
    x1_width = (y1-height/2)*math.sin(rotation_angle_rad)
    x1_rotated = x1_height - x1_width + height/2

    y1_width = (x1-width/2)*math.sin(rotation_angle_rad)
    y1_height = (y1-height/2)*math.cos(rotation_angle_rad)
    y1_rotated = y1_width + y1_height + width/2

    x2_height = (x2-width/2)*math.cos(rotation_angle_rad)
    x2_width = (y2 - height/2)*math.sin(rotation_angle_rad)
    x2_rotated = x2_height-x2_width + height/2

    y2_width = (x2-width/2)*math.sin(rotation_angle_rad)
    y2_height = (y2 - height/2)*math.cos(rotation_angle_rad)
    y2_rotated = y2_width + y2_height + width/2

    return (x1_rotated, y1_rotated, x2_rotated, y2_rotated)


# AM VERY SUSPICIOUS OF THIS COME BACK TO IT LATER
def find_peaks(spectrogram_ycfit, tolerance):
    ycfit_max = np.max(spectrogram_ycfit)
    ycfit_min = np.min(spectrogram_ycfit)
    # threshold_calculated = (ycfit_max-ycfit_min)/tolerance
    # index, other = scipy.signal.find_peaks(
    #     spectrogram_ycfit
    # )

    index = np.argmax(spectrogram_ycfit)

    return (index, spectrogram_ycfit[index])

def peak_detection(
    plasmon_array, width_array,
    results_array, detect_array,
    spectrogram
):

    # retrieve average pixel, ev/pixel, microrad/pixel
    average_pixel = results_array[3]
    # e_dispersion = results_array[0]
    # q_dispersion_upper = results_array[1]

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
            Peak_position_x = []
            Peak_position_y = []

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
                reshape=False
            )

            # Find absolute value of image
            spectrogram_signal = np.absolute(spectrogram_rotated)

            # Ensure y1 is less than y2
            if y1 > y2:
                temp = y1
                y1 = y2
                y2 = temp

            # loops through rows of box
            for j in range(int(y1), int(y2)):
                spectrogram_ycfit = ycfit(
                    spectrogram_signal,
                    average_pixel,
                    j, width, x1,
                    np.sum(spectrogram_signal)
                )
                spectrogram_ycfit = spectrogram_ycfit[0]
                index, magnitude = find_peaks(spectrogram_ycfit, tolerance)

                Peak_position_x.insert(
                    j - int(y1) - 1,
                    (int(x1) - width/2 + index - spectrogram_width/2) *
                    math.cos(rotation_angle_rad*-1) +
                    (j - spectrogram_height/2) *
                    math.sin(rotation_angle_rad*-1) * -1 +
                    spectrogram_height/2+np.max(spectrogram)
                )
                Peak_position_y.insert(
                     j - int(y1) - 1,
                    (int(x1) - width/2 + index - spectrogram_width/2) *
                    math.sin(rotation_angle_rad*-1) +
                    (j - spectrogram_height/2) *
                    math.cos(rotation_angle_rad*-1) +
                    spectrogram_height/2+np.min(spectrogram)
                )
            print(len(Peak_position_y))

        else:
            pass
