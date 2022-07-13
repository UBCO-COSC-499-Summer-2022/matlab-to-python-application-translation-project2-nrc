import numpy as np

def diff_raw_with_model(
    raw_x, raw_y,
    x, y, z, tilt, phai, alpha, magnification
):
    # compute trig ratios
    tilt_cos = np.cos(tilt)
    tilt_sin = np.sin(tilt)
    phai_cos = np.cos(phai)
    phai_sin = np.sin(phai)
    alpha_cos = np.cos(alpha)
    alpha_sin = np.sin(alpha)

    # compute modeled x
    xx = x[:, np.newaxis] * (
        alpha_cos*tilt_cos +
        alpha_sin*phai_sin*tilt_sin
    )
    xy = y[:, np.newaxis] * (
        alpha_cos*tilt_sin*-phai_sin +
        alpha_sin*phai_cos*phai_cos +
        alpha_sin*phai_sin*phai_sin*tilt_cos
    )
    xz = z[:, np.newaxis] * (
        alpha_cos*tilt_sin*phai_cos +
        alpha_sin*phai_cos*phai_sin -
        alpha_sin*phai_sin*tilt_cos*phai_cos
    )
    model_x = (xx + xy + xz) * magnification

    # compute modeled y
    yx = x[:, np.newaxis] * (
        -alpha_sin*tilt_cos +
        alpha_cos*phai_sin*tilt_sin
    )
    yy = y[:, np.newaxis] * (
        alpha_sin*tilt_sin*phai_sin +
        alpha_cos*phai_cos*phai_cos +
        alpha_cos*phai_sin*phai_sin*tilt_cos
    )
    yz = z[:, np.newaxis] * (
        -alpha_sin*tilt_sin*phai_cos +
        alpha_cos*phai_cos*phai_sin -
        alpha_cos*phai_sin*tilt_cos*phai_cos
    )
    model_y = (yx + yy + yz) * magnification

    # compute difference between model and raw and return as residual vector
    diff_x = model_x - raw_x
    diff_y = model_y - raw_y
    return np.concatenate(diff_x, diff_y).flatten()


def create_optimizeable_function(
    raw_x, raw_y,
    x_func, y_func, z_func, tilt_func, phai_func, alpha_func, mag_func
):
    def optimizeable_function(input_vector):
        x = x_func(input_vector)
        y = y_func(input_vector)
        z = z_func(input_vector)
        tilt = tilt_func(input_vector)
        phai = phai_func(input_vector)
        alpha = alpha_func(input_vector)
        magnification = mag_func(input_vector)
        return diff_raw_with_model(
            raw_x, raw_y,
            x, y, z, tilt, phai, alpha, magnification
        )
    return optimizeable_function


