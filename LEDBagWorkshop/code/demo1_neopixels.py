# Demo code.py for Constellations 2024 workshop
# Lesson 1 shows how to use the pixel array to change pixel colors and
# to display those colors by calling the show() function

# Import modules to give our program the functionality we want
import neopixel
import board
from adafruit_circuitplayground import cp
import time


# Update to match the number of NeoPixels in the LED string
npixels     = 20
pixel_pin   = board.A1
# Create the pixel array object
string = neopixel.NeoPixel(pixel_pin, npixels, brightness=0.2, auto_write=False)

# The Circuit Playground Express already has a built in pixel array. Let's set
# its brightness value to match the LED string, and turn off auto_write

cp.pixels.brightness = 0.2
cp.pixels.auto_write = False


# Colors are represented as RGB (Red/Green/Blue) tuples
BLACK   = (0,0,0)
RED     = (255,0,0)
GREEN   = (0,255,0)
BLUE    = (0,0,255)


# Change pixel 0 in LED string
string[0] = RED   # We access individual elements of the array to set the colors in the pixel string
string.show()	  # When auto_write is off, calling show() pushes the colors to the LEDs

# Change pixel 0 in CPX
cp.pixels[0] = BLUE
cp.pixels.show()

# Define a function to take a pixel array, and move a single
# colored pixel around the string, pausing for "delay" pixels
# between each movement
def pixel_loop(pixels, color, delay = 0.2):
    for i in range(pixels.n):
        pixels[i] = color
        pixels.show()
        time.sleep(delay)
        pixels[i] = BLACK
        pixels.show()

# The infinite loop below prevents the program from exiting.
# if we put code in here to change the pixel color values, we
# can create an animation
while True:
    # Uncomment the lines below to show a simple animation of a pixel
    # moving around the CPX and around the string
    #pixel_loop(cp.pixels, GREEN)
    #pixel_loop(string, BLUE)
    pass
