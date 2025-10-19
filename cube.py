import math
import time
import os

# Define the size of the cube
size = 10

# Create a function to draw the cube
def draw_cube(x, y, z):
    for i in range(size):
        for j in range(size):
            if (i - x) ** 2 + (j - y) ** 2 <= (z ** 2 / 4):
                print('*', end='')
            else:
                print(' ', end='')
        print()

# Create a function to rotate the cube
def rotate_cube(x, y, z):
    for _ in range(1000):  # Rotate 1000 times
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        draw_cube(int(size / 2) + int(math.sin(time.time()) * (size / 4)), int(size / 2) + int(math.cos(time.time()) * (size / 4)), size // 2)
        time.sleep(0.1)

# Run the rotation
rotate_cube(0, 0, 0)