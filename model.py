import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# This class contains the rules for how light behaves near a black hole
class BlackHolePhysics:
    def __init__(self, mass=1.0, spin=0.7):
        self.M = mass                    # Mass of the black hole
        self.a = spin * mass             # How fast the black hole is spinning
        self.rs = 2 * self.M             # Event horizon radius (edge of the black hole)
        self.c = 1                       # Speed of light (set to 1 for simplicity)

    def schwarzschild_metric_effects(self, r):
        # Simulate how time slows down and space gets stretched near a black hole
        time_dilation = np.sqrt(np.maximum(1 - self.rs/r, 0.01))
        spatial_curvature = 1.0 / np.maximum(1 - self.rs/r, 0.01)
        return time_dilation, spatial_curvature

    def gravitational_lensing(self, x, y):
        # Simulate how the black hole bends the paths of light
        r = np.sqrt(x**2 + y**2)
        r = np.maximum(r, 0.1)  # Prevent divide-by-zero

        deflection_strength = 4 * self.M / r  # More bending closer to the black hole

        # Deflection is perpendicular to the direction of incoming light
        cos_theta = x / r
        sin_theta = y / r
        deflection_x = -deflection_strength * sin_theta
        deflection_y = deflection_strength * cos_theta

        return deflection_x, deflection_y

    def doppler_shift(self, x, y, rotation_angle):
        # Simulate how spinning stretches and compresses the light (Doppler effect)
        r = np.sqrt(x**2 + y**2)
        omega_drag = 2 * self.M * self.a / (r**3 + self.a**2 * r)

        phi = np.arctan2(y, x)
        v_phi = omega_drag * r

        # Brighter when parts rotate toward us, dimmer when moving away
        doppler_factor = 1.0 / (1 + v_phi * np.sin(phi + rotation_angle))
        return np.clip(doppler_factor, 0.3, 2.0)


# This class handles the image and animation logic
class GravitationalLensingAnimation:
    def __init__(self, grid_size=300):
        self.black_hole = BlackHolePhysics(mass=2.0, spin=0.8)
        self.grid_size = grid_size
        self.setup_coordinates()
        self.create_background_pattern()

    def setup_coordinates(self):
        # Set up a 2D grid of points in space
        extent = 8
        x = np.linspace(-extent, extent, self.grid_size)
        y = np.linspace(-extent, extent, self.grid_size)
        self.X, self.Y = np.meshgrid(x, y)
        self.R = np.sqrt(self.X**2 + self.Y**2)

    def create_background_pattern(self):
        # Make a starry background pattern to get distorted by the black hole
        grid_freq = 8
        pattern1 = np.sin(self.X * grid_freq) * np.sin(self.Y * grid_freq)
        pattern2 = np.sin(self.X * grid_freq * 0.7) * np.cos(self.Y * grid_freq * 1.3)
        self.background = 0.5 + 0.3 * pattern1 + 0.2 * pattern2

        # Add a faint radial glow
        radial_pattern = np.sin(self.R * 2) * np.exp(-self.R / 10)
        self.background += 0.2 * radial_pattern

    def calculate_lensed_image(self, rotation_angle):
        # Create a new image showing how light is bent
        lensed_image = np.zeros_like(self.X)

        # Get how light is bent near the black hole
        deflection_x, deflection_y = self.black_hole.gravitational_lensing(self.X, self.Y)

        # Adjust bending based on rotation
        cos_rot = np.cos(rotation_angle)
        sin_rot = np.sin(rotation_angle)
        deflection_x_rot = deflection_x * cos_rot - deflection_y * sin_rot
        deflection_y_rot = deflection_x * sin_rot + deflection_y * cos_rot

        # Figure out where light is coming from
        source_x = self.X + deflection_x_rot
        source_y = self.Y + deflection_y_rot

        # For each pixel, look up what background light should appear there
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                sx, sy = source_x[i, j], source_y[i, j]

                # Block out the inside of the black hole
                if self.R[i, j] < self.black_hole.rs * 1.1:
                    lensed_image[i, j] = 0
                    continue

                if abs(sx) < 8 and abs(sy) < 8:
                    grid_x = int((sx + 8) * self.grid_size / 16)
                    grid_y = int((sy + 8) * self.grid_size / 16)

                    if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                        lensed_image[i, j] = self.background[grid_y, grid_x]

        return lensed_image

    def apply_relativistic_effects(self, image, rotation_angle):
        # Make light dimmer/redder near the black hole
        time_dilation, _ = self.black_hole.schwarzschild_metric_effects(self.R)
        doppler_factor = self.black_hole.doppler_shift(self.X, self.Y, rotation_angle)

        relativistic_image = image * time_dilation * doppler_factor

        # Add some brightening near the black hole (light gets focused)
        brightening = np.where(
            self.R > self.black_hole.rs, 
            1.0 + 2.0 * self.black_hole.M / self.R**2, 
            1.0
        )
        relativistic_image *= brightening

        return np.clip(relativistic_image, 0, 2)

    def create_photon_sphere_glow(self, rotation_angle):
        # Draw a glowing ring around the black hole
        photon_radius = 1.5 * self.black_hole.rs
        ring_distance = np.abs(self.R - photon_radius)
        ring_intensity = np.exp(-ring_distance**2 / 0.5) * 2.0

        phi = np.arctan2(self.Y, self.X)
        rotation_pattern = 1.0 + 0.5 * np.sin(3 * phi + rotation_angle * 4)

        return ring_intensity * rotation_pattern


# This function builds the animation
def create_physics_animation():
    lensing_sim = GravitationalLensingAnimation(grid_size=200)

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Color scheme: dark red to white
    colors = ['black', 'darkred', 'red', 'orange', 'yellow', 'white']
    cmap = LinearSegmentedColormap.from_list('blackhole', colors, N=256)

    def animate(frame):
        ax.clear()
        ax.set_facecolor('black')

        rotation_angle = frame * 0.05

        lensed_image = lensing_sim.calculate_lensed_image(rotation_angle)
        relativistic_image = lensing_sim.apply_relativistic_effects(lensed_image, rotation_angle)
        photon_glow = lensing_sim.create_photon_sphere_glow(rotation_angle)

        final_image = relativistic_image + photon_glow

        # Make the black hole region completely black
        final_image[lensing_sim.R <= lensing_sim.black_hole.rs] = 0

        ax.imshow(final_image, extent=[-8, 8, -8, 8], cmap=cmap, origin='lower', vmin=0, vmax=2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

        # Optional red ring to show where the event horizon is
        circle = plt.Circle((0, 0), lensing_sim.black_hole.rs, fill=False, color='red', linewidth=1, alpha=0.5)
        ax.add_patch(circle)

        ax.set_title('Rotating Black Hole with Gravitational Lensing', color='white', fontsize=16, pad=20)

    print("Rendering black hole animation...")
    anim = animation.FuncAnimation(fig, animate, frames=400, interval=100, blit=False)

    return fig, anim


# Run the animation
if __name__ == "__main__":
    fig, anim = create_physics_animation()
    plt.show()
    anim.save('clear_rotating_black_hole.gif', writer='pillow', fps=10)