from tkinter.messagebox import showerror, showinfo
from nrcemt.alignment_software.engine.particle_tracking import (
    ParticleLocationSeries,
    create_particle_mask,
    particle_search
)
from nrcemt.common.gui.async_handler import AsyncHandler
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_locations = None
        self.tracking_locations = None
        self.properties = {
            "search_size": (80, 80),
            "marker_radius": 20
        }

    def open(self, close_callback):
        if self.particle_locations is None:
            self.particle_locations = [
                ParticleLocationSeries(self.image_count())
                for i in range(MAX_PARTICLES)
            ]
            self.tracking_locations = [None for i in range(MAX_PARTICLES)]

        self.auto_track_window = AutoTrackWindow(
            self.main_window, MAX_PARTICLES
        )
        self.auto_track_window.properties.set_properties(self.properties)
        self.auto_track_window.table.set_mark_end_command(self.mark_end)
        self.auto_track_window.table.set_reset_command(self.reset_particle)
        self.auto_track_window.properties.set_command(self.update_properties)
        self.auto_track_window.track_button.config(
            command=AsyncHandler(self.track_selected)
        )
        self.auto_track_window.reset_button.config(command=self.reset_all)
        self.main_window.image_select.set(1)

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
            if particle.get_first_frame() == i:
                tracking_location = self.tracking_locations[p]
            else:
                tracking_location = None
            if tracking_location is not None:
                self.main_window.image_frame.render_rect(
                    tracking_location, search_size, "#ff9800"
                )
                self.main_window.image_frame.render_rect(
                    tracking_location, marker_size, "#8bc34a"
                )
                self.main_window.image_frame.render_text(
                    tracking_location, p+1
                )
            elif particle_location is not None:
                self.main_window.image_frame.render_text(
                    particle_location, p+1
                )
            if particle_location is not None:
                self.main_window.image_frame.render_point(
                    particle_location, "#03a9f4"
                )

    def track_selected(self):
        particle_mask = create_particle_mask(self.properties["marker_radius"])
        search_size = self.properties["search_size"]
        try:
            for i in range(self.image_count()):
                image = self.load_image(i)
                for p in self.auto_track_window.table.get_tracked_particles():
                    particle = self.particle_locations[p]
                    if i < particle.get_first_frame():
                        continue
                    if i > particle.get_last_frame():
                        continue
                    if i == particle.get_first_frame():
                        search_location = self.tracking_locations[p]
                    else:
                        search_location = particle[i-1]
                    if search_location is None:
                        continue
                    found_location = particle_search(
                        image, particle_mask, search_location, search_size
                    )
                    particle[i] = found_location
                self.main_window.image_select.set(i+1)
                self.main_window.update_idletasks()
            showinfo("Automatic Tracking", "Tracking Completed!")
            self.main_window.image_select.set(1)
        except Exception as e:
            showerror("Coarse Alignment Error", str(e))

    def update_properties(self):
        self.properties = self.auto_track_window.properties.get_properties()
        self.select_image(self.main_window.selected_image())

    def mark_end(self, particle_index):
        selected_image = self.main_window.selected_image()
        particle = self.particle_locations[particle_index]
        particle.set_last_frame(selected_image)
        self.select_image(selected_image)

    def canvas_click(self, x, y):
        selected_image = self.main_window.selected_image()
        selected_particle = (
            self.auto_track_window.table.get_selected_particle()
        )
        self.tracking_locations[selected_particle] = (x, y)
        particle = self.particle_locations[selected_particle]
        particle.set_first_frame(selected_image)
        self.auto_track_window.table.enable_tracking(selected_particle)
        self.select_image(selected_image)

    def reset_all(self):
        self.particle_locations = [
            ParticleLocationSeries(self.image_count())
            for i in range(MAX_PARTICLES)
        ]
        self.tracking_locations = [None for i in range(MAX_PARTICLES)]
        for i in range(MAX_PARTICLES):
            self.auto_track_window.table.disable_tracking(i)
        self.select_image(self.main_window.selected_image())

    def reset_particle(self, particle_index):
        self.particle_locations[particle_index] = (
            ParticleLocationSeries(self.image_count())
        )
        self.tracking_locations[particle_index] = None
        self.select_image(self.main_window.selected_image())

    def is_ready(self):
        return self.contrast_step.is_ready()
