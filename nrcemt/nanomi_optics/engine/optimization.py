import numpy as np
import scipy.optimize
from .lens import Lens

def create_optimizable_funcion(
    mode, lens_i, lens_location, focal_lengths, rays
):
    def cf_function(x):
        sample = Lens(528.9, None, None, None)
        lenses = []
        print()
        for i, cf in enumerate(focal_lengths):
            lenses.append(
                Lens(
                    lens_location[i],
                    x if lens_i == i else cf,
                    sample if i == 0 else lenses[i - 1],
                    3 if i < 2 else 2     
                )
            )
        sc = Lens(
                972.7, 0, lenses[-1], 1
        )
        # print(f"\nRAYS:\n{rays}")
        if mode == "Image":
            opt_rays = [rays[0]]
        elif mode == "Diffraction":
            opt_rays = rays
        results = []
        print(f"RAYS FOR OPT: \n{opt_rays}")


        for ray in opt_rays:
            print(f"ray={ray}")
            for j, lens in enumerate(lenses):
                if j != 0:
                    lens.update_output_plane_location()
                print(f"j={j}")
                # print(str(lens))
                # print(ray if j == 0 else
                    # lenses[j - 1].ray_out_lens)
                sl, el, li = lens.ray_path(
                    ray if j == 0 else
                    lenses[j - 1].ray_out_lens,
                    None
                )
            sc.update_output_plane_location()
            sl, el, li =sc.ray_path(lenses[-1].ray_out_lens, 0)
            sl = ([x for x, y in sl], [y for x, y in sl])
            print(f"Y={sl}")
            results.append(sc.ray_in_vac[0][0])

        print(f"\nx={x}")
        if len(results) == 1:
            print(f"RESULT={results[0]}\n")
            return results[0]
        elif len(results) == 2:
            print(f"RESULT={results[0]} - {results[1]} = {results[0] - results[1]}\n")
            return results[0] - results[1]

    return cf_function

def optimize_focal_length(
    mode, lens, lens_locations, focal_lengths, rays
):
    print(
        f"optmode = {mode}\n",
        f"lens = {lens}\n",
        f"lens_locations = {lens_locations}\n",
        f"focal lengths = {focal_lengths}\n",
        f"rays = {rays}\n\n",
    )

    opt_function = create_optimizable_funcion(
        mode, lens, lens_locations, focal_lengths, rays
    )

    result = scipy.optimize.least_squares(
        opt_function, np.array(focal_lengths[lens])
    )
    print(result.x)
    return result.x[0]