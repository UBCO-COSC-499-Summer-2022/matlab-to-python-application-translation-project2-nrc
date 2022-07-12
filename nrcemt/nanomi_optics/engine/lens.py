import numpy as np


class Lens:

    def __init__(
        self, location, focal_length,
        input_image_location, input_image_distance
    ):
        self.source_distance = location
        self.focal_length = focal_length
        self.input_plane_location = input_image_location
        self.input_plane_distance = input_image_distance

    def __str__(self):
        return (
            f"[source_distance={self.source_distance}, "
            f"focal_length = {self.focal_length}, "
            f"input_plane_location = {self.input_plane_location}, "
            f"input_plane_distance = {self.input_plane_distance}]"
        )

    # transfer matrix for free space
    @staticmethod
    def transfer_free(distance):
        return np.array([[1, distance], [0, 1]], dtype=float)

    @staticmethod
    def vacuum_matrix(distance, in_beam_vector):
        """
        inputs:
        distance = distance in space traveled [mm]
        ray_in = height [mm] IN beam, angle of IN beam [rad]: column vector

        outputs:
        ray_out = height [mm] OUT-beam, angle of OUT beam [rad]: column vector
        ditance = distance beam traveled along z [mm]
        """
        out_beam_vector = np.matmul(
            Lens.transfer_free(distance), in_beam_vector
        )
        return out_beam_vector, distance

    # transfer matrix for thin lens
    def transfer_thin(self):
        return np.array([[1, 0], [-1/self.focal_length, 1]], dtype=float)

    # In matlab the location was used to plot the line

    def thin_lens_matrix(self, ray_in, obj_location):
        """
        inputs:
        location = lens distance from source [mm]
        focal_length = focal length [mm]
        ray_in = [height of IN beam [mm], angle of IN beam [rad]]
        obj_location = location of object [mm] from source
        **lens = string name of the lens

        outputs:
        height_out = [height of OUT-beam-at-image, angle of OUT-beam [rad]]
        image_location = image location Z [mm] from source
        distance = lens centre-image distance along z [mm]
        mag_out = magnification image/object
        """

        # locate image z & crossover
        # temporary matrix calculating transfer vacuum to lens, and lens
        temp_matrix = np.matmul(
            self.transfer_thin(),
            self.transfer_free(self.source_distance - obj_location)
        )
        # lens-to-image [mm] # for thin lens # AA = A(f,z0)
        distance = -temp_matrix[0, 1]/temp_matrix[1, 1]
        # image-to-source Z [mm]
        # image_location = distance + self.source_distance

        # ray_out = [X, q] at OUT-face of lens
        # needed to vacuum propagation matrix and plot
        ray_out = np.matmul(self.transfer_thin(), ray_in)

        # calculate magnification X_image / X_obj
        # for thin lens: mag_out = Mag(z0,d) % or mag_out = Mag(z0,A(f,z0))
        # mag_out = 1/temp_matrix[1, 1]
        return ray_out, distance

    def ray_path(self, ray_vector, c_mag):
        points = []

        points.append(
            (self.input_plane_location, ray_vector[0][0])
        )

        out_beam_vect, beam_dist = self.vacuum_matrix(
            self.input_plane_distance, ray_vector
        )
        points.append(
            (self.input_plane_location + beam_dist, out_beam_vect[0][0])
        )

        self.out_beam_lense_vect, beam_lense_dist = self.thin_lens_matrix(
            out_beam_vect, 0
        )
        points.append(
            (self.source_distance, self.out_beam_lense_vect[0][0])
        )

        out_beam_image_vect, beam_image_dist = Lens.vacuum_matrix(
            beam_lense_dist, self.out_beam_lense_vect
        )
        points.append(
            (self.source_distance + beam_image_dist, out_beam_image_vect[0][0])
        )

        return points

    def crossover_point_location(self):
        return np.array(
            [self.source_distance + self.focal_length, 0]
        )