import tkinter as tk
import math
import random

class AnimatedCanvas:
    def __init__(self, root, width, height):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.canvas.pack()

        self.elements = []
        self.line_ids = []

        # Convert centimeters to pixels (assuming 96 DPI)
        radius_cm = 0.01
        radius_pixels = int(radius_cm * 96 / 2.54)

        # Create elements
        for _ in range(500):
            x = random.uniform(radius_pixels, width - radius_pixels)
            y = random.uniform(radius_pixels, height - radius_pixels)
            element = self.canvas.create_oval(
                x - radius_pixels, y - radius_pixels,
                x + radius_pixels, y + radius_pixels,
                fill="white"
            )
            self.elements.append(element)

        # Initial velocities
        self.velocities = [(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(500)]

        # Start the animation
        self.animate()

    def animate(self):
        for i, element in enumerate(self.elements):
            # Move elements based on velocities
            dx, dy = self.velocities[i]
            self.canvas.move(element, dx, dy)

            # Check for collisions with walls
            x1, y1, x2, y2 = self.canvas.coords(element)
            if x1 <= 0 or x2 >= self.canvas.winfo_width():
                self.velocities[i] = (-dx, dy)  # Reverse x velocity on wall collision
            if y1 <= 0 or y2 >= self.canvas.winfo_height():
                self.velocities[i] = (dx, -dy)  # Reverse y velocity on wall collision

        # Check distance between elements
        self.check_distance()

        # Call the animate function after a delay
        self.root.after(30, self.animate)

    def check_distance(self):
        # Clear previous lines
        for line_id in self.line_ids:
            self.canvas.delete(line_id)

        self.line_ids = []

        # Check distance between elements and draw lines if they are close
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                x1, y1, _, _ = self.canvas.coords(self.elements[i])
                x2, y2, _, _ = self.canvas.coords(self.elements[j])

                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                if distance < 50:
                    line_id = self.canvas.create_line(x1, y1, x2, y2, fill="white")
                    self.line_ids.append(line_id)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Element Animation")
    
    app = AnimatedCanvas(root, width=800, height=800)
    
    root.mainloop()
