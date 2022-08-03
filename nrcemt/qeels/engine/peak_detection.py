import math
import numpy as np
import scipy
import scipy.signal
import scipy.optimize

SPEED_LIGHT = 3e8
PLANCK_CONSTANT = 4.1357e-15
# THIS VALUE IS MODIFIED BY DROPDOWN LIST
BULK_EV = 15
OMEGA = BULK_EV/PLANCK_CONSTANT/(2)**0.5
Q_PIXEL = 0.001165934e9


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
    return (rotation_angle_rad, rotation_angle_degrees)


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
def find_peaks(spectrogram_ycfit):
    # a = np.max(spectrogram_ycfit)-np.min(spectrogram_ycfit)
    # a = a/1.001
    # index, other = scipy.signal.find_peaks(
    #     spectrogram_ycfit
    # )
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

    return peak_position_x, peak_position_y, image


def calculation_e(e_bulk, peak_position_x):
    """ Calculates the sum of squares based of the ev/pixel
    and the peak positions """
    difference = peak_position_x-e_bulk
    sum_squares = np.sum(np.square(difference))
    return sum_squares


def bulk_calculations(peak_position_x, peak_position_y, spectrogram):
    max_index = np.argmax(spectrogram)
    max_index_x, max_index_y = np.unravel_index(max_index, spectrogram.shape)
    image = np.zeros(spectrogram.shape)
    e_bulk = scipy.optimize.least_squares(
        calculation_e, 200,
        args=(peak_position_x,)
    )
    # yfit is equal to e_bulk
    e_bulk = e_bulk['x'][0]

    # difference = peak_position_x - peak_position_x.mean()
    # SStot = np.sum(np.square(difference))

    # difference = peak_position_x - e_bulk
    # SSres = np.sum(np.square(difference))

    # WHY IS THIS CALCULATED (maybe used later on????)
    # rsq = 1-SSres/SStot

    for y in range(int(peak_position_y.min()), int(peak_position_y.max())+1):
        image[y+max_index_x-1:y+max_index_x+1,
              int(e_bulk+max_index_y)-1:int(e_bulk+max_index_y)+1] = 10000

    # e dispersion is equalt to e_pixel
    e_dispersion = BULK_EV/e_bulk
    return e_dispersion, image


def calculation_q(
    q_pixel, peak_position_x, peak_position_y, e_pixel
):
    """ function calculates the sum of squares based
    on the passed q and e pixels and the peak positions """
    yfit = calculate_yfit(q_pixel, peak_position_y)
    SSres = np.sum((peak_position_x*e_pixel - yfit)**2)
    return SSres


def calculate_yfit(q_pixel, peak_position_y):
    yfit = (
        ((OMEGA**2)/2 + (SPEED_LIGHT*q_pixel*peak_position_y)**2 -
            ((OMEGA**4)/4 + (SPEED_LIGHT*q_pixel*peak_position_y)**4)
            ** 0.5) ** 0.5 * PLANCK_CONSTANT
    )
    return yfit


# Produces a different(better) result than the matlab's optimization function
def surface_plasmon_calculations(
    peak_position_x, peak_position_y, e_pixel, spectrogram
):
    image = np.zeros(spectrogram.shape)
    q_pixel = scipy.optimize.least_squares(
        calculation_q, Q_PIXEL,
        args=(peak_position_x, peak_position_y, e_pixel)
    )
    q_pixel = q_pixel['x'][0]

    # SStot = np.sum((
    #     peak_position_x*e_pixel -
    #     np.mean(peak_position_x*e_pixel))**2
    # )
    # SSres = calculation_q(q_pixel, peak_position_x, peak_position_y, e_pixel)

    # rsq = 1-SSres/SStot
    image = draw_plasmon(
        spectrogram, peak_position_y,
        q_pixel, e_pixel
    )
    # sometimes q_pixel is 0
    dispersion_q = 0.0019687/(1/(abs(q_pixel)*10**-9))*10**6

    return dispersion_q, image, q_pixel


def draw_plasmon(spectrogram, peak_position_y, q_pixel, e_pixel):
    image = np.zeros(spectrogram.shape)
    max_index = np.argmax(spectrogram)
    max_index_x, max_index_y = np.unravel_index(max_index, spectrogram.shape)
    for y in range(10, int(spectrogram.shape[0]/3)+1):
        if peak_position_y.mean() < 0:
            y = y*-1

        x = calculate_yfit(q_pixel, y)/e_pixel
        image[int(y) + max_index_x][int(x) + max_index_y] = 10000
    return image


def peak_detection(
    plasmon_array, width_array,
    results_array, detect_array,
    spectrogram
):

    # retrieve average pixel, ev/pixel, microrad/pixel
    average_pixel = results_array[3]
    e_dispersion = results_array[0]
    peak_images = []

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

        # if both values are entered
        if detect and np.all([x1, x2, y1, y2]) > 0:
            # DOUBLE CHECK, BUT I DONT THINK THE RESULT FROM THIS ARE USED
            # calculated_corners = compute_rect_corners(x1, y1, x2, y2, width)

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

            if y1 > y2:
                temp = y1
                y1 = y2
                y2 = temp

            # rotate image so plasmon is vertical
            # differntiation between matlab and original
            spectrogram_rotated = rotate_spectrogram(
                spectrogram,
                rotation_angle_degrees
            )

            # Find absolute value of image
            spectrogram_signal = np.absolute(spectrogram_rotated)

            peak_position_x, peak_position_y, peak_image = mark_peaks(
                x1, y1, y2, spectrogram_signal, spectrogram, average_pixel,
                width, rotation_angle_rad, spectrogram_height,
                spectrogram_height
            )
            peak_images.append(peak_image)
            if i == 0:
                e_dispersion, bulk_image = bulk_calculations(
                    peak_position_x, peak_position_y,
                    spectrogram
                )
                results_array[0] = e_dispersion
                peak_images.append(bulk_image)

            else:
                dispersion_q, surface_image, _ = surface_plasmon_calculations(
                    peak_position_x, peak_position_y,
                    e_dispersion, spectrogram
                )
                peak_images.append(surface_image)

                if i == 2:
                    results_array[1] = dispersion_q
                else:
                    results_array[2] = dispersion_q

    result_image = np.maximum.reduce([spectrogram, *peak_images])

    return results_array, result_image
