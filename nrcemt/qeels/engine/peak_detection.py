import math
import numpy as np
import scipy
import scipy.signal
import scipy.optimize
import matplotlib.pyplot as plt

SPEED_LIGHT = 3e8
PLANCK_CONSTANT = 4.1357e-15
OMEGA_SP = 15/PLANCK_CONSTANT/(2)**0.5

# tested
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


# tested
def ycfit(signal, average_pixel, row, width, x1, sum):
    signal_sect = signal[
        int(row-average_pixel):int(row+average_pixel+1),
        int(x1-width/2):int(x1+width/2+1)
    ]
    signal_sect = signal_sect/sum
    ycfit = np.mean(signal_sect, axis=0)

    return ycfit


# tested
def calc_angle(x1, y1, x2, y2):
    delta_x = x1-x2
    delta_y = y1-y2

    # SHE DOES tan(x/y) in her code so is x/y in ours too ... for now
    rotation_angle_rad = math.atan2(delta_x, delta_y)
    rotation_angle_degrees = math.degrees(rotation_angle_rad)
    return(rotation_angle_rad, rotation_angle_degrees)


# untested
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


# Section commented out because if "peak" is on very edge
# of ycfit it will not be the returned value. The matlab code returns
# the max value of the array not necissarily a "peak". It now behaves
# the same way the matlab code does.
# tested
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


# tested
def rotate_spectrogram(spectrogram, rotation_angle_degrees):
    spectrogram_rotated = scipy.ndimage.rotate(
        spectrogram,
        rotation_angle_degrees,
        reshape=False
    )

    return spectrogram_rotated


# tested
def mark_peaks(
    x1, y1, y2, spectrogram_signal, spectrogram, average_pixel, width,
    rotation_angle_rad, spectrogram_height, spectrogram_width
):
    peak_position_x = []
    peak_position_y = []

    index = np.argmax(spectrogram)
    x_max, y_max = np.unravel_index(index, spectrogram.shape)

    image = np.zeros((spectrogram_width, spectrogram_height))
    # image = spectrogram
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


# tested
def calculation_e(E_bulk, peak_position_x):
    difference = peak_position_x-E_bulk
    SSres = np.sum(np.square(difference))
    return SSres


# tested
def bulk_calculations(Peak_position_x, Peak_position_y, bulk_ev, spectrogram):
    index = np.argmax(spectrogram)
    x_max, y_max = np.unravel_index(index, spectrogram.shape)
    image2 = np.zeros(spectrogram.shape)
    e_bulk = scipy.optimize.least_squares(
        calculation_e, 200,
        args=(Peak_position_x,)
    )
    # yfit is equal to e_bulk
    e_bulk = e_bulk['x'][0]

    difference = Peak_position_x - Peak_position_x.mean()
    SStot = np.sum(np.square(difference))

    difference = Peak_position_x - e_bulk
    SSres = np.sum(np.square(difference))

    # WHY IS THIS CALCULATED (maybe used later on????)
    rsq = 1-SSres/SStot

    for y in range(Peak_position_y.min(), Peak_position_y.max()):
        image2[y+y_max][int(e_bulk)+x_max] = 10000

    # e dispersion is equalt to e_pixel
    e_dispersion = bulk_ev/e_bulk
    return e_dispersion, image2


# tested
def calculation_q(
    q_p, Peak_position_x, Peak_position_y, e_pixel
):
    yfit = calculate_yfit(q_p, Peak_position_x, Peak_position_y)
    SSres = np.sum((Peak_position_x*e_pixel - yfit)**2)
    return SSres


def calculate_yfit(q_p, Peak_position_x, Peak_position_y):
    yfit = (
        ((OMEGA_SP**2)/2 + (SPEED_LIGHT*q_p*Peak_position_y)**2 -
            ((OMEGA_SP**4)/4 + (SPEED_LIGHT*q_p*Peak_position_y)**4)
            ** 0.5) ** 0.5 * PLANCK_CONSTANT
    )

    return yfit


# untested
# Produces a different(better) result than the matlab's optimization function
def surface_plasmon_calculations(
    Peak_position_x, Peak_position_y, q_pixel, e_pixel, spectrogram
):

    image2 = np.zeros(spectrogram.shape)
    res = scipy.optimize.least_squares(
        calculation_q, q_pixel,
        args=(Peak_position_x, Peak_position_y, e_pixel)
    )
    res = res['x'][0]
    SStot = np.sum((
        Peak_position_x*e_pixel -
        np.mean(Peak_position_x*e_pixel))**2
    )
    SSres = calculation_q(res, Peak_position_x, Peak_position_y, e_pixel)

    rsq = 1-SSres/SStot

    image2 = draw_plasmon(
        spectrogram, Peak_position_y,
        Peak_position_x, res, e_pixel
    )

    dispersionQ = 0.0019687/(1/(abs(res)*10**-9))*10**6

    return dispersionQ, image2


# untested
def draw_plasmon(spectrogram, Peak_position_y, Peak_position_x, res, e_pixel):
    image2 = np.zeros(spectrogram.shape)
    index = np.argmax(spectrogram)
    x_max, y_max = np.unravel_index(index, spectrogram.shape)
    for y in range(10, int(spectrogram.shape[0]/3)):
        if Peak_position_y.mean() < 0:
            y = y*-1
        x = calculate_yfit(res, Peak_position_x, y)/e_pixel
        image2[int(y + x_max)][int(x + y_max)] = 10000
    return image2
