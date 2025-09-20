import tkinter as tk
import math

# Set the size of the canvas for a wide display
CANVAS_WIDTH = 1200      # Wider screen for more trajectory coverage
CANVAS_HEIGHT = 800      # Taller screen
particle_size = 25       # Size of the projectile visualized

# Dictionary storing gravitational acceleration for supported planets
planets = {
    "mars": 3.71,
    "earth": 9.8,
    "moon": 1.62,
    "jupiter": 24.79
}

def cloudgenerator(canvas, i, cloud_color):
    """Draws clouds for environmental realism on the selected planet background."""
    canvas.create_oval(i, 150, i + 100, 250, fill=cloud_color, outline=cloud_color)
    canvas.create_oval(i + 50, 150, i + 150, 250, fill=cloud_color, outline=cloud_color)
    canvas.create_oval(i + 100, 150, i + 200, 250, fill=cloud_color, outline=cloud_color)
    canvas.create_oval(i + 25, 100, i + 125, 200, fill=cloud_color, outline=cloud_color)
    canvas.create_oval(i + 75, 100, i + 175, 200, fill=cloud_color, outline=cloud_color)

def load_environment(canvas, sky, ground):
    """Sets up the graphical background for the chosen simulation environment."""
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT - 200, fill=sky, outline=sky)                        # Sky area
    canvas.create_rectangle(0, CANVAS_HEIGHT - 200, CANVAS_WIDTH, CANVAS_HEIGHT, fill=ground, outline=ground)      # Ground area
    canvas.create_line(0, CANVAS_HEIGHT - 200, CANVAS_WIDTH, CANVAS_HEIGHT - 200, fill="black")                   # Ground boundary

def animate_projectile(canvas, x_init, y_init, u_x, u_y, g):
    """Animates the projectile flight and draws spaced blue trajectory lines."""
    t = 0
    interval = 10                                # Time between animation frames, in milliseconds
    projectile = canvas.create_oval(x_init, y_init, x_init + particle_size, y_init + particle_size, fill="blue")   # Projectile (drawn as blue oval)
    draw_spacing = 10                            # Draw blue trajectory line every N frames for spacing
    frame_count = 0
    def step():
        # Allow modification of variables from enclosing scope
        nonlocal t, frame_count
        # Projectile equations for horizontal (x) and vertical (y) positions
        x = u_x * t
        y = u_y * t - (0.5 * g * (t ** 2))
        # Transform simulation coordinates to canvas coordinates
        x_screen = x_init + x
        y_screen = y_init - y
        # Stop the animation if projectile hits ground or leaves canvas
        if y < 0 or x_screen > CANVAS_WIDTH:
            canvas.coords(projectile, x_screen, y_screen, x_screen + particle_size, y_screen + particle_size)
            return
        # Move projectile to the new location on canvas
        canvas.coords(projectile, x_screen, y_screen, x_screen + particle_size, y_screen + particle_size)
        # Draw a vertical blue line every draw_spacing frames
        if frame_count % draw_spacing == 0:
            canvas.create_line(x_screen, y_screen, x_screen, y_init, fill="blue")
        frame_count += 1
        # Advance the simulation time
        t += interval / 1000
        # Schedule next animation frame
        canvas.after(interval, step)
    step()

def main():
    """Main loop: manages user input, sets up each simulation run, draws environment and stats."""
    print("Welcome to 2-D projectile motion simulator")
    while True:
        # User selects planet or chooses custom settings
        print("\nEnter one of the following options")
        print("1. mars")
        print("2. earth")
        print("3. moon")
        print("4. jupiter")
        print("5. custom")
        try:
            planet = int(input("Enter your choice number: "))
        except:
            print("Invalid input, exiting.")
            break

        # Set up the graphics window for each simulation run
        root = tk.Tk()
        root.title("Projectile Motion Simulator")
        canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas.pack()

        # Draw the chosen planet's environment and get gravity and wind
        if planet == 1:         # Mars
            g = planets["mars"]
            load_environment(canvas, "#FF6F61", "#B22222")
            cloudgenerator(canvas, 0, "#C8C8C8")
            cloudgenerator(canvas, 400, "#C8C8C8")
            cloudgenerator(canvas, 900, "#C8C8C8")
            canvas.create_text(10, 30, text="2-D PROJECTILE MOTION SIMULATOR-MARS", anchor="nw", font=("Arial", 28))
            wind = 0
        elif planet == 2:       # Earth
            g = planets["earth"]
            load_environment(canvas, "#87CEEB", "#90EE90")
            cloudgenerator(canvas, 0, "white")
            cloudgenerator(canvas, 400, "white")
            cloudgenerator(canvas, 900, "white")
            canvas.create_text(10, 30, text="2-D PROJECTILE MOTION SIMULATOR-EARTH", anchor="nw", font=("Arial", 28))
            wind = float(input("Enter wind speed (m/s), positive for right, negative for left, 0 for none: "))
        elif planet == 3:       # Moon
            g = planets["moon"]
            load_environment(canvas, "#C0C0C0", "#A9A9A9")
            canvas.create_text(10, 30, text="2-D PROJECTILE MOTION SIMULATOR-MOON", anchor="nw", font=("Arial", 28))
            wind = 0
        elif planet == 4:       # Jupiter
            g = planets["jupiter"]
            load_environment(canvas, "#D2B48C", "#8B4513")
            cloudgenerator(canvas, 0, "#F0DCC0")
            cloudgenerator(canvas, 400, "#F0DCC0")
            cloudgenerator(canvas, 900, "#F0DCC0")
            canvas.create_text(10, 30, text="2-D PROJECTILE MOTION SIMULATOR-JUPITER", anchor="nw", font=("Arial", 28))
            wind = 0
        elif planet == 5:       # Custom settings
            g = float(input("Enter the acceleration due to gravity (m/s^2): "))
            load_environment(canvas, "#87CEEB", "#90EE90")
            cloudgenerator(canvas, 0, "white")
            cloudgenerator(canvas, 400, "white")
            cloudgenerator(canvas, 900, "white")
            canvas.create_text(10, 30, text="2-D PROJECTILE MOTION SIMULATOR-CUSTOM", anchor="nw", font=("Arial", 28))
            wind = float(input("Enter wind speed (m/s), positive for right, negative for left, 0 for none: "))
        else:
            print("Invalid option. Try again.")
            root.destroy()
            continue

        # Get initial conditions from user
        print(f"The acceleration due to gravity is {g}")
        u = float(input("Enter the initial velocity of object (m/s): "))
        theta = float(input("Enter the angle of projection in degrees: "))

        # Calculate initial velocity components (account for wind speed)
        radian = math.radians(theta)
        sin_theta = math.sin(radian)
        cos_theta = math.cos(radian)
        u_x = u * cos_theta + wind
        u_y = u * sin_theta

        # Physics computations for trajectory
        maximum_height = (u ** 2) * (sin_theta ** 2) / (2 * g)
        flight_time = 2 * u_y / g
        horizontal_range = u_x * flight_time

        # Initial particle location on the canvas
        x_particle = 50
        y_particle = CANVAS_HEIGHT - 200 - particle_size

        # Draw visualizations: range, max height, stats
        canvas.create_line(x_particle, y_particle + 20, x_particle + horizontal_range, y_particle + 20, fill="yellow", width=4)
        canvas.create_line(x_particle + (horizontal_range / 2), y_particle - maximum_height,
                           x_particle + (horizontal_range / 2), y_particle, fill="yellow", width=4)
        canvas.create_text(10, CANVAS_HEIGHT - 190, text=f"Horizontal range = {horizontal_range:.2f} m", anchor="nw", font=("Arial", 20))
        canvas.create_text(10, CANVAS_HEIGHT - 160, text=f"Maximum height = {maximum_height:.2f} m", anchor="nw", font=("Arial", 20))
        canvas.create_text(10, CANVAS_HEIGHT - 130, text=f"Time of flight = {flight_time:.2f} s", anchor="nw", font=("Arial", 20))
        if wind > 0:
            canvas.create_text(10, CANVAS_HEIGHT - 100, text=f"Wind Speed = {wind:.2f} m/s   Wind direction: Right", anchor="nw", font=("Arial", 20))
        elif wind < 0:
            canvas.create_text(10, CANVAS_HEIGHT - 100, text=f"Wind Speed = {wind:.2f} m/s   Wind direction: Left", anchor="nw", font=("Arial", 20))
        else:
            canvas.create_text(10, CANVAS_HEIGHT - 100, text=f"Wind Speed = {wind:.2f} m/s", anchor="nw", font=("Arial", 20))

        # Start projectile animation
        print("Simulation running: view the projectile motion window.")
        animate_projectile(canvas, x_particle, y_particle, u_x, u_y, g)
        root.mainloop()        # Tkinter main loop (close window to continue)

        # Prompt for next action
        try:
            choice = int(input("Enter 1 to exit or 0 to continue: "))
        except:
            break
        if choice == 1:
            break

if __name__ == '__main__':
    main()
