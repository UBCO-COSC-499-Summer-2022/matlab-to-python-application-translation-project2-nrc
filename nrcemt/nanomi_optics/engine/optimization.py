import math
import numpy as np
import scipy.optimize
from .lens import Lens


def create_optimizable_funcion(
    mode, lens_i, lens_location, focal_lengths, rays, active
):
    def cf_function(x):
        if abs(x[0]) > 300 or abs(x[0]) < 6:
            return math.inf

        sample = Lens(528.9, None, None, None)
        lenses = []
        for i, cf in enumerate(focal_lengths):
            if active[i]:
                lenses.append(
                    Lens(
                        lens_location[i],
                        x[0] if lens_i == i else cf,
                        lenses[-1] if len(lenses) else sample,
                        3 if i < 2 else 2
                    )
                )

        if len(lenses):
            sc = Lens(972.7, 0, lenses[-1], 1)

        if mode == "Image":
            opt_rays = [rays[0]]
        elif mode == "Diffraction":
            opt_rays = rays
        results = []

        for ray in opt_rays:
            for j, lens in enumerate(lenses):
                if j != 0:
                    lens.update_output_plane_location()
                sl, el, li = lens.ray_path(
                    ray if j == 0 else
                    lenses[j - 1].ray_out_lens,
                    None
                )
            sc.update_output_plane_location()
            sc.ray_path(lenses[-1].ray_out_lens, 0)
            sl = ([x for x, y in sl], [y for x, y in sl])
            results.append(sc.ray_in_vac[0][0])

        if len(results) == 1:
            return results[0]
        elif len(results) == 2:
            return results[0] - results[1]

    return cf_function


def optimize_focal_length(
    mode, lens, lens_locations, focal_lengths, rays, active
):
    opt_function = create_optimizable_funcion(
        mode, lens, lens_locations, focal_lengths, rays, active
    )

    result = scipy.optimize.least_squares(
        opt_function, focal_lengths[lens], bounds=(6, 300)
    )
    return result.x[0]
