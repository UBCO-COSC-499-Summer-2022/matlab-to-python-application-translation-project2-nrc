import numpy as np
from nrcemt.nanomi_optics.engine.lens import Lens

OPTICAL_DISTANCE = 0.00001
LAMBDA_ELECTRON = 0.0112e-6
SCATTERING_ANGLE = LAMBDA_ELECTRON / OPTICAL_DISTANCE

ray = np.array(
    [[0], [SCATTERING_ANGLE]]
)
sample = Lens(528.9, None, None, None, None)
objective = Lens(551.6, 19.67, sample, 3, True)
intermediate = Lens(706.4, 6.498, objective, 3, True)
projective = Lens(826.9, 6, intermediate, 2, True)
screen = Lens(972.7, None, projective, 1, False)


def test_ray_path():
    x_points = [
        528.89999999999997726, 551.60000000000002274,
        698.96270627062529002, 698.96270627062529002
    ]
    y_points = [
        0, 0.025424000000000047256,
        -6.9388939039072283776e-18, 0
    ]

    points = objective.ray_path(ray, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )

    intermediate.update_output_plane_location()
    x_points = [
        551.60000000000002274, 706.39999999999997726,
        757.85092865215824531, 757.85092865215824531
    ]

    y_points = [
        0.025424000000000047256, -0.0012831316725981922744,
        4.9656459499836103078e-17, 5.0306980803327405738e-17
    ]
    points = intermediate.ray_path(objective.ray_out_lens, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )

    projective.update_output_plane_location()
    x_points = [
        706.39999999999997726, 826.89999999999997726, 833.47098382625472368
    ]

    y_points = [
        -0.0012831316725981922744, 0.0017220107144984920025,
        -4.6078592330633938445e-18
    ]
    points = projective.ray_path(intermediate.ray_out_lens, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )

    screen.update_output_plane_location()
    x_points = [
        826.89999999999997726, 972.70000000000004547
    ]

    y_points = [
        0.0017220107144984920025, -0.036486752054132744194
    ]
    points = screen.ray_path(projective.ray_out_lens, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
