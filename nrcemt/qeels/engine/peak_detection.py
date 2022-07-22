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


def ycfit(signal, average_pixel, row, width, x1, sum):
    signal_sect = signal[
        int(row-average_pixel):int(row+average_pixel+1),
        int(x1-width/2):int(x1+width/2+1)
    ]
    signal_sect = signal_sect/sum
    ycfit = np.mean(signal_sect, axis=0)

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


def find_peaks(spectrogram_ycfit):
    # a = np.max(spectrogram_ycfit)-np.min(spectrogram_ycfit)
    # a = a/1.001
    # index, other = scipy.signal.find_peaks(
    #     spectrogram_ycfit,
    #     prominence=0
    # )
    # # print(index)
    # # print(other)
    # max = -math.inf
    # max_ind = -math.inf
    # for ind in index:
    #     if spectrogram_ycfit[ind] > max:
    #         max = spectrogram_ycfit[ind]
    #         max_ind = ind

    max_ind = np.argmax(spectrogram_ycfit)
    return (max_ind, spectrogram_ycfit[max_ind])


def rotate_spectrogram(spectrogram, rotation_angle_degrees):
    spectrogram_rotated = scipy.ndimage.rotate(
        spectrogram,
        rotation_angle_degrees*-1,
        reshape=False
    )

    # plt.imshow(spectrogram_rotated)
    # plt.show()
    # plt.imshow(rotated)
    # plt.show()

    return spectrogram_rotated


def mark_peaks(
    x1, y1, y2, spectrogram_signal, spectrogram, average_pixel, width,
    rotation_angle_rad, spectrogram_height, spectrogram_width
):
    peak_position_x = []
    peak_position_y = []

    index = np.argmax(spectrogram)
    x_max, y_max = np.unravel_index(index, spectrogram.shape)

    image = np.zeros((spectrogram_width, spectrogram_height))
    # loops through rows of box
    for j in range(int(y1), int(y2)+1):
        spectrogram_ycfit = ycfit(
            spectrogram_signal,
            average_pixel,
            j, width, x1,
            np.sum(spectrogram_signal)
        )
        peak_index, magnitude = find_peaks(spectrogram_ycfit)

        peak_position_x.append(
            (round(x1, 0) - width/2 + peak_index - spectrogram_width/2) *
            math.cos(rotation_angle_rad*-1) +
            (j - spectrogram_height/2) *
            math.sin(rotation_angle_rad*-1) * -1 +
            spectrogram_height/2-(y_max)
        )

        peak_position_y.append(
            (round(x1, 0) - width/2 + peak_index - spectrogram_height/2) *
            math.sin(rotation_angle_rad*-1) +
            (j - spectrogram_height/2) *
            math.cos(rotation_angle_rad*-1) +
            spectrogram_height/2-(x_max)
        )

        # Works when loading peak_position_x arrays are correct
        image[
            int(peak_position_y[j - int(y1)]+x_max),
            int(peak_position_x[j - int(y1)]+y_max)
        ] = 5000

    peak_position_x = np.round(peak_position_x)
    peak_position_y = np.round(peak_position_y)

    return (peak_position_x, peak_position_y, image)