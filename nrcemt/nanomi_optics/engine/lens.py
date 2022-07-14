import numpy as np

ONE_STEP = 1
TWO_STEP = 2
THREE_STEP = 3

class Lens:

    def __init__(
        self, location, focal_length,
        last_lense, type, start_origin
    ):
        self.source_distance = location
        self.focal_length = focal_length
        self.last_lense = last_lense
        if last_lense is None:
            self.last_lense_location = 0
            self.last_lense_distance = self.source_distance
            self.last_lense_output_location = 0 if start_origin \
                else self.source_distance
        else:
            self.last_lense_location = last_lense.source_distance
            self.last_lense_distance = self.source_distance \
                - last_lense.source_distance
            self.last_lense_output_location = 0
        self.type = type
        self.output_plane_location = 0

    def __str__(self):
        return (
            f"[source_distance={self.source_distance}, "
            f"focal_length = {self.focal_length}, "
            f"last_lense_location = {self.last_lense_location}, "
            f"last_lense_distance = {self.last_lense_distance}, "
            f"last_lense_output_location = {self.last_lense_output_location}, "
            f"type = {self.type}, "
            f"output_plane_location = {self.output_plane_location}]"
        )

    # transfer matrix for free space
    @staticmethod
    def transfer_free_space(distance):
        return np.array([[1, distance], [0, 1]], dtype=float)

    @staticmethod
    def vacuum_matrix(distance, ray_in_vector):
        """
        inputs:
        distance = distance in space traveled [mm]
        ray_in = height [mm] IN beam, angle of IN beam [rad]: column vector

        outputs:
        ray_out = height [mm] OUT-beam, angle of OUT beam [rad]: column vector
        ditance = distance beam traveled along z [mm]
        """
        # print(f"Transfer free matrix:\n {Lens.transfer_free_space(distance)}")
        # print(f"In beam vector:\n {in_beam_vector}")
        out_beam_vector = np.matmul(
            Lens.transfer_free_space(distance), ray_in_vector
        )
        return out_beam_vector, distance

    # transfer matrix for thin lens
    def transfer_thin_lense(self):
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
            self.transfer_thin_lense(),
            self.transfer_free_space(self.source_distance - obj_location)
        )
        print(temp_matrix)
        # lens-to-image [mm] # for thin lens # AA = A(f,z0)
        distance = -temp_matrix[0, 1]/temp_matrix[1, 1]
        # image-to-source Z [mm]
        self.output_plane_location = self.source_distance + distance
        # image_location = distance + self.source_distance

        # ray_out = [X, q] at OUT-face of lens
        overall_ray_out = np.matmul(
            self.transfer_free_space(distance),
            np.matmul(self.transfer_thin_lense(), ray_in)
        )
        # needed to vacuum propagation matrix and plot
        ray_out = np.matmul(self.transfer_thin_lense(), ray_in)

        # calculate magnification X_image / X_obj
        # for thin lens: mag_out = Mag(z0,d) % or mag_out = Mag(z0,A(f,z0))
        # mag_out = 1/temp_matrix[1, 1]
        return ray_out, overall_ray_out, distance

    def ray_path(self, ray_vector, c_mag):
        points = []

        points.append(
            (self.last_lense_location, ray_vector[0][0])
        )

        ray_in_vac, ray_in_vac_dist = self.vacuum_matrix(
            self.last_lense_distance, ray_vector
        )
        points.append(
            (self.last_lense_location + ray_in_vac_dist, ray_in_vac[0][0])
        )

        if self.type > ONE_STEP:
            self.ray_out_lense, self.overall_ray_out_lense, \
                ray_out_dist = self.thin_lens_matrix(
                    ray_in_vac, self.last_lense_output_location
                )
            if self.type == THREE_STEP:
                ray_out_vac, ray_out_vac_dist = Lens.vacuum_matrix(
                    ray_out_dist, self.ray_out_lense
                )
                points.append(
                    (
                        self.source_distance + ray_out_vac_dist,
                        ray_out_vac[0][0]
                    )
                )

            points.append(
                (self.output_plane_location, self.overall_ray_out_lense[0][0])
            )


        return points

    def crossover_point_location(self):
        return np.array(
            [self.source_distance + self.focal_length, 0]
        )

    def update_output_plane_location(self):
        if self.last_lense is not None:
            self.last_lense_output_location = \
                self.last_lense.output_plane_location
        # print(f"Update: {self.last_lense_output_location}")
