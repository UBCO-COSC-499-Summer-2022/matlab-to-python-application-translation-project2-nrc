from tkinter.messagebox import showerror, showinfo
from nrcemt.alignment_software.engine.particle_tracking import (
    ParticleLocationSeries,
    create_particle_mask,
    particle_search
)
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_locations = None  # stores actual particle locations
        self.tracking_locations = None  # stores locations to start looking
        self.properties = None

    def open(self, close_callback):
        # instantiate particle locations if they haven't already
        if self.particle_locations is None:
            self.particle_locations = [
                ParticleLocationSeries(self.image_count())
                for i in range(MAX_PARTICLES)
            ]
            self.tracking_locations = [None for i in range(MAX_PARTICLES)]

        # get some default search parameters based on the image resolution
        # for a 1024x1024 image search_size should 80
        # and marker_radius should be 20
        if self.properties is None:
            resolution = self.load_image(0).shape[0]
            search_size = round(resolution / 1024 * 80)
            marker_radius = round(resolution / 1024 * 20)
            self.properties = {
                "search_size": (search_size, search_size),
                "marker_radius": marker_radius
            }

        self.auto_track_window = AutoTrackWindow(
            self.main_window, MAX_PARTICLES
        )
        # register callbacks
        self.auto_track_window.properties.set_properties(self.properties)
        self.auto_track_window.table.set_mark_end_command(self.mark_end)
        self.auto_track_window.table.set_reset_command(self.reset_particle)
        self.auto_track_window.properties.set_command(self.update_properties)
        self.auto_track_window.track_button.config(command=self.track_selected)
        self.auto_track_window.reset_button.config(command=self.reset_all)

        # reset back to first image, because most particles should be tracked
        # starting from image 1
        self.main_window.image_select.set(1)

        # cleanup
        def close():
            self.auto_track_window.destroy()
            self.auto_track_window = None
            close_callback(reset=True)
        self.auto_track_window.protocol("WM_DELETE_WINDOW", close)

    def load_image(self, i):
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image)
        self.render_markers(i)
        self.main_window.image_frame.update()
        if self.auto_track_window is not None:
            self.auto_track_window.table.update_data(
                self.particle_locations, i
            )

    def render_markers(self, i):
        search_size = self.properties["search_size"]
        marker_radius = self.properties["marker_radius"]
        # TODO: avoid this call to create_particle_mask
        marker_size = create_particle_mask(marker_radius).shape
        for p, particle in enumerate(self.particle_locations):
            particle_location = particle[i]
            # check whether a particle is beginnning tracking in this slot
            if particle.get_first_frame() == i:
                tracking_location = self.tracking_locations[p]
            else:
                tracking_location = None
            # render some boxes to indicate search areas
            if tracking_location is not None:
                # search size rect
                self.main_window.image_frame.render_rect(
                    tracking_location, search_size, "#ff9800"
                )
                # marker size rect
                self.main_window.image_frame.render_rect(
                    tracking_location, marker_size, "#8bc34a"
                )
                # label
                self.main_window.image_frame.render_text(
                    tracking_location, p+1
                )
            elif particle_location is not None:
                # still draw the label even if no tracking_location
                self.main_window.image_frame.render_text(
                    particle_location, p+1
                )
            # render a blue bot for particle location
            if particle_location is not None:
                self.main_window.image_frame.render_point(
                    particle_location, "#03a9f4"
                )

    def track_selected(self):
        # create a circular particle mask
        particle_mask = create_particle_mask(
            self.properties["marker_radius"],
            self.auto_track_window.properties.get_invert_particle_color()
        )
        search_size = self.properties["search_size"]
        # hide the window temporarily so user can't interact with it
        self.auto_track_window.withdraw()
        try:
            for i in range(self.image_count()):
                image = self.load_image(i)
                for p in self.auto_track_window.table.get_tracked_particles():
                    particle = self.particle_locations[p]
                    # check whether particle is persent on this frame
                    # otherwise skip it
                    if i < particle.get_first_frame():
                        continue
                    if i > particle.get_last_frame():
                        continue
                    # using tracking location if first frame
                    # otherwise use previous particle location
                    if i == particle.get_first_frame():
                        search_location = self.tracking_locations[p]
                    else:
                        search_location = particle[i-1]
                    if search_location is None:
                        continue
                    # search for the particle and update its position!
                    particle[i] = particle_search(
                        image, particle_mask, search_location, search_size
                    )
                # show the user progress
                self.main_window.image_select.set(i+1)
                self.main_window.update()
            showinfo("Automatic Tracking", "Tracking Completed!")
            # reset back to frame 1
            self.main_window.image_select.set(1)
        except Exception as e:
            showerror("Coarse Alignment Error", str(e))
        finally:
            # bring the window back into view
            self.auto_track_window.deiconify()

    def update_properties(self):
        self.properties = self.auto_track_window.properties.get_properties()
        self.select_image(self.main_window.selected_image())

    def mark_end(self, particle_index):
        """Marks the final frame a particle appears on."""
        selected_image = self.main_window.selected_image()
        particle = self.particle_locations[particle_index]
        if selected_image >= particle.get_first_frame():
            particle.set_last_frame(selected_image)
            self.select_image(selected_image)
        else:
            showerror("Invalid Range", "Can't mark end before start frame")

    def canvas_click(self, x, y):
        """User indicates where to track the particle by clicking."""
        selected_image = self.main_window.selected_image()
        selected_particle = (
            self.auto_track_window.table.get_selected_particle()
        )
        self.tracking_locations[selected_particle] = (x, y)
        particle = self.particle_locations[selected_particle]
        if selected_image <= particle.get_last_frame():
            particle.set_first_frame(selected_image)
            self.auto_track_window.table.enable_tracking(selected_particle)
            self.select_image(selected_image)
        else:
            showerror("Invalid Range", "Can't mark start before end frame")

    def reset_all(self):
        """Nuke all particle data."""
        self.particle_locations = [
            ParticleLocationSeries(self.image_count())
            for i in range(MAX_PARTICLES)
        ]
        self.tracking_locations = [None for i in range(MAX_PARTICLES)]
        for i in range(MAX_PARTICLES):
            self.auto_track_window.table.disable_tracking(i)
        self.select_image(self.main_window.selected_image())

    def reset_particle(self, particle_index):
        """Nuke specific particle data."""
        self.particle_locations[particle_index] = (
            ParticleLocationSeries(self.image_count())
        )
        self.tracking_locations[particle_index] = None
        self.select_image(self.main_window.selected_image())

    def is_ready(self):
        return self.contrast_step.is_ready()
