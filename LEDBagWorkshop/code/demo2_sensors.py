########################################################################################
# CircuitPlayground Express LED Backpack Code
# Constellations 2024 - Portland Winter Light Festival
# CETI Institute
#
# Debra Ansell
########################################################################################
# The modules we import here provide extra functionality for the code
import time
import board
import neopixel
import random
import touchio      # Needed for capacative touch pins
import analogio     # For reading value from light sensor

from adafruit_circuitplayground import cp
from math import floor


### Code to set up the neopixels ########################################################
# The circuit plaground express uses the NEOPIXEL pin to control the 10
# LEDs on its front. We will attach a pixel pixel string of 20 addtional
# addressable LEDs to pin A0
cp_pixel_pin        = board.NEOPIXEL
string_pixel_pin    = board.A1

# The number of NeoPixels on the attached LED string
npix_str   = 20
npix_cp    = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

# Create a NeoPixel object to control the LED string, 20% brigness
string = neopixel.NeoPixel(
    string_pixel_pin, npix_str, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# The NeoPixel object for the CPX already exists as "cp.pixels". These lines turn the brightness
# down to 20%, and makes it wait for the "show()" command to push changes to the pixels
cp.pixels.brightness = 0.2
cp.pixels.auto_write = False


# The wheel function takes a value between 0-255 and returns a color
# from the rainbow continuum
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
    
# Neopixel colors are represented as RGB "tuples" where the value of the Red, Green
# and blue components of the color ranges from 0 to 255
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
BLACK   = (0, 0, 0)

# Helper function to display a single color on both LED string & CPX
def set_leds(color):
    string.fill(color)
    cp.pixels.fill(color)
    string.show()
    cp.pixels.show()
    
# This function generates a color from the X, Y, Z values of acceleration
# Taken from Adafruit example by Kattini Rembor
# Scale turns the color intensity up, since typically, acceleration values
# range from 0-10 (in the absence of shaking)
scale = 25
def color_from_acc():
    x, y, z = cp.acceleration
    # uncomment this to see values
    #print((x, y, z))
    R = abs(scale*int(x))
    G = abs(scale*int(y))
    B = abs(scale*int(z))
    return (R & 255, G & 255, B & 255) # Return the color tuple (max out at 255)
    
# Start the program with LEDs all off
set_leds(BLACK)
    
# Variables to track the state of the push buttons
state_a = cp.button_a
state_b = cp.button_b

# Variables to track the state of cap touch pins
state_A2 = cp.touch_A2
state_A3 = cp.touch_A3
state_A4 = cp.touch_A4
state_A5 = cp.touch_A5


while True:
    # Check to see if the value of button A has changed
    if cp.button_a != state_a:
        state_a = cp.button_a  # Record the new state
        # TODO: make the LEDs react when button A is pressed
        if state_a:
            print("A pressed")
        else:
            print("A released")
            
    # Check to see if touch pins have been touched
    if cp.touch_A2 != state_A2:
        state_A2 = cp.touch_A2 # Record the new state
        if state_A2:
            print("Pin A2 touched")
        else:
            print("Pin A2 released")
            
    # Set the color of the LEDs based on the tilt angle of the CPX
    #col = color_from_acc()
    #set_leds(col)
    #time.sleep(0.05)
    
    # Set the color of the LEDs based on the value of the light sensor
    #print(cp.light)
    #time.sleep(0.01)
    #set_leds(wheel(cp.light))
    #time.sleep(0.05)
    
    # Detect shakes and taps. The "shake_threshold" keyword sets the 
    # detection sensitivity to a value between 10 and 30
    #if cp.shake(shake_threshold=12):
    #    cp.red_led = not cp.red_led  # Toggle red LED