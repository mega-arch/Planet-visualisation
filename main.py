import pygame
import math

# Initialize pygame
pygame.init()

# Set up display parameters
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Color definitions
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Font for distance text
FONT = pygame.font.SysFont("comicsans", 16)

# Planet class representing each planet and its properties
class Planet:
    AU = 149.6e6 * 1000  # Astronomical Unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # Scale factor for display (1 AU = 250 pixels)
    TIMESTEP = 3600 * 24  # Time step for simulation (1 day)

    def __init__(self, x, y, radius, color, mass):
        self.x = x  # x position of the planet
        self.y = y  # y position of the planet
        self.radius = radius  # radius of the planet for drawing
        self.color = color  # color of the planet
        self.mass = mass  # mass of the planet

        self.orbit = []  # list to store the planet's orbital path
        self.sun = False  # if the planet is the sun
        self.distance_to_sun = 0  # distance from the planet to the sun

        self.x_vel = 0  # x velocity of the planet
        self.y_vel = 0  # y velocity of the planet

    def draw(self, win):
        """
        Draws the planet and its orbit on the window.
        """
        # Scale the planet's position based on the scale factor and the window size
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the orbit path if it has more than two points
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet as a circle
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # If the planet is not the sun, show the distance to the sun
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        """
        Calculates the gravitational attraction between this planet and another planet.
        Returns the x and y components of the force.
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        # Gravitational force equation
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)  # angle of force
        force_x = math.cos(theta) * force  # x component of force
        force_y = math.sin(theta) * force  # y component of force
        return force_x, force_y

    def update_position(self, planets):
        """
        Updates the planet's position based on gravitational attraction from all other planets.
        """
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocities based on the forces
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position based on velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))  # Store new position for orbit path

def main():
    """
    Main function to run the simulation.
    """
    run = True
    clock = pygame.time.Clock()

    # Initialize the sun and planets with their respective parameters
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)  # The sun
    sun.sun = True  # Mark the sun as the central star

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)  # Earth
    earth.y_vel = 29.783 * 1000  # Velocity of Earth in m/s

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)  # Mars
    mars.y_vel = 24.077 * 1000  # Velocity of Mars in m/s

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)  # Mercury
    mercury.y_vel = -47.4 * 1000  # Velocity of Mercury in m/s

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)  # Venus
    venus.y_vel = -35.02 * 1000  # Velocity of Venus in m/s

    planets = [sun, earth, mars, mercury, venus]  # List of planets

    # Main simulation loop
    while run:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        WIN.fill((0, 0, 0))  # Clear the screen (fill it with black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit the loop if the window is closed

        # Update and draw each planet
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()  # Update the display

    pygame.quit()  # Quit pygame when the loop ends

# Run the main function
main()
