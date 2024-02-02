# Import modules to give our program the functionality we want
import neopixel                             # Control WS2812 LEDs
import board                                # Use functionality of the pins on the controller
from adafruit_circuitplayground import cp   # Access CPX sensors and outputs
import time                                 # Get data from system clock

# Update to match the number of NeoPixels in the LED string
npixels     = 20
pixel_pin   = board.A1
# Create the pixel array object to control the LED string
string = neopixel.NeoPixel(pixel_pin, npixels, brightness=0.2, auto_write=False)

# The Circuit Playground Express class, "cp" already has a built in pixel array.
# Let's set its brightness value to match the LED string, and turn off auto_write
cp.pixels.brightness = 0.2
cp.pixels.auto_write = False

# Neopixel colors are represented as RGB "tuples" where the value of the Red, Green
# and blue components of the color ranges from 0 to 255
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
BLACK   = (0, 0, 0)
MIX     = (100, 10, 300)

# Helper function to display a single color on both LED string & CPX
def set_leds(color):
    string.fill(color)
    cp.pixels.fill(color)
    string.show()
    cp.pixels.show()

# This loop will go on forever so the program never ends
while True:
    set_leds(RED)
    time.sleep(0.5)
    set_leds(GREEN)
    time.sleep(0.5)
    set_leds(BLUE)
    time.sleep(0.5)
