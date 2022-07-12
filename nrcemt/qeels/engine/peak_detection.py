import math
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
def peak_detection(plasmon_array, width_array, results_array):
    # loop through different rows
    for i in range(3):
        print('sup')

