import numpy as np
import scipy.optimize


def diff_raw_with_model(
    normalized_markers,
    x, y, z, tilt, phai, alpha, magnification
):
    # compute trig ratios
    tilt_cos = np.cos(np.deg2rad(tilt))
    tilt_sin = np.sin(np.deg2rad(tilt))
    phai_cos = np.cos(np.deg2rad(phai))
    phai_sin = np.sin(np.deg2rad(phai))
    alpha_cos = np.cos(np.deg2rad(alpha))
    alpha_sin = np.sin(np.deg2rad(alpha))

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

    # interleave modeled coords to match normalized markers
    modeled_markers = np.empty((*model_x.shape, 2), dtype=model_x.dtype)
    modeled_markers[:, :, 0] = model_x
    modeled_markers[:, :, 1] = model_y

    return (normalized_markers - modeled_markers).ravel()


def create_optimizeable_diff_function(
    normalized_markers,
    x_func, y_func, z_func, tilt_func, phai_func, alpha_func, mag_func
):
    def diff_function(input_vector):
        x = x_func(input_vector)
        y = y_func(input_vector)
        z = z_func(input_vector)
        tilt = tilt_func(input_vector)
        phai = phai_func(input_vector)
        alpha = alpha_func(input_vector)
        magnification = mag_func(input_vector)
        return diff_raw_with_model(
            normalized_markers,
            x, y, z, tilt, phai, alpha, magnification
        )
    return diff_function


def normalize_marker_data(markers):
    mean_marker_per_image = markers.mean(axis=0)
    return markers - mean_marker_per_image


def optimize_particle_model(
    normalized_markers, tilt, fixed_phai=None, fixed_alpha=None
):
    # 3 coords, xyz, per marker
    marker_count = normalized_markers.shape[0]
    input_vector_size = 3 * marker_count
    def x_func(x): return x[0:marker_count]
    def y_func(x): return x[marker_count:2*marker_count]
    def z_func(x): return x[2*marker_count:3*marker_count]

    # tilt values are given
    def tilt_func(x): return tilt

    # phai is either optimized or fixed
    if fixed_phai is not None:
        def phai_func(x): return fixed_phai
    else:
        phai_index = input_vector_size
        def phai_func(x): return x[phai_index]
        input_vector_size += 1

    # alpha is either optimized or fixed
    if fixed_alpha is not None:
        def alpha_func(x): return fixed_alpha
    else:
        alpha_index = input_vector_size
        def alpha_func(x): return x[alpha_index]
        input_vector_size += 1

    # maginfication is not considered for this optimization
    def mag_func(x): return 1

    # perform least-squares optimization
    x0 = np.zeros(input_vector_size)
    diff_function = create_optimizeable_diff_function(
        normalized_markers,
        x_func, y_func, z_func, tilt_func, phai_func, alpha_func, mag_func
    )
    result = scipy.optimize.least_squares(diff_function, x0)

    # extract and return results
    x = x_func(result.x)
    y = y_func(result.x)
    z = z_func(result.x)
    phai = phai_func(result.x)
    alpha = alpha_func(result.x)
    return x, y, z, phai, alpha
