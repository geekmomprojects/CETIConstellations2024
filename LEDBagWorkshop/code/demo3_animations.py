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

from adafruit_circuitplayground import cp
from math import floor


# The circuit plaground express uses the NEOPIXEL pin to control the 10
# LEDs on its front. We will attach a pixel pixel string of 20 addtional
# addressable LEDs to pin A1
cp_pixel_pin        = board.NEOPIXEL
string_pixel_pin    = board.A1

# The number of NeoPixels on the attached LED string
npix_str   = 20
npix_cp    = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

# Create a NeoPixel object to control the LED string, 20% brigness
pixel_string = neopixel.NeoPixel(
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


# This function takes a pixel string as an input and fills all the pixels
# with a rainbow gradient, starting with the wheel color of "color_index"
def fill_rainbow(pixels, color_index, do_show=True):
    for i in range(pixels.n):       # pixels.n is the number of leds
        index = color_index + i*255//pixels.n
        pixels[i] = wheel(index & 255)
    if do_show:
        pixels.show()

# This function fills both the CPX and string LEDs with a rainbow
# incrementing the starting color slightly each time it is called
rainbow_index = 0
rainbow_increment = 3
def rainbow_animation():
    global rainbow_index
    fill_rainbow(cp.pixels, rainbow_index)
    fill_rainbow(pixel_string, rainbow_index)
    rainbow_index = (rainbow_index + rainbow_increment) & 255

# Fade an RGB color tuple by a fraction represented by a number from 0 (no fade) to
# 255 (fade completely to black). A brightness value of less than "threshold" is
# set to 0 (off)
def fade_color(col, fract, threshold=20):
    return (0 if col[0] < threshold else int(col[0]*fract),
            0 if col[1] < threshold else int(col[1]*fract),
            0 if col[2] < threshold else int(col[2]*fract))

# Fades all pixels in the string by the same fraction.
# Returns true if any pixels are illuminated
def fade_string(pixels, fract=0.8):
    for i in range(pixels.n):
        if pixels[i] != (0,0,0):
            pixels[i] = fade_color(pixels[i], fract)

# Animation to move a comet around both the CPX and attached pixel
# string with the same speed
comet_speed = 2  # number of seconds to traverse all the pixels
def comet_animation():
    global rainbow_index

    # Fade any illuminated pixels to create comet "tail
    fade_string(cp.pixels)
    fade_string(pixel_string)

    # Set and increment the hue of the next illuminated pixel
    color = wheel(rainbow_index)
    rainbow_index = (rainbow_index + rainbow_increment) & 255

    # Calculate the position of the current illuminated pixel in each
    # string based on how much time has passed and the speed
    comet_pos = (time.monotonic() % comet_speed)/comet_speed

    # Round the position to the nearest integer value in the string
    cp_pos = int(floor(comet_pos*npix_cp)) % npix_cp
    str_pos = int(floor(comet_pos*npix_str)) % npix_str

    # Set the pixel color
    cp.pixels[cp_pos] = color
    pixel_string[str_pos] = color

    # Push changes to the leds
    cp.pixels.show()
    pixel_string.show()


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


# Function to randomly turn on any of the pixels in the array
# Chance is the odds (fraction out of 255) to turn each pixel off
def blink_on(pixels, chance, color=None):
    for i in range(pixels.n):
        if pixels[i] == (0,0,0):
            if random.random() < chance:
                if color is None:
                    color = wheel(random.randint(0,255))
                pixels[i] = color
    pixels.show()

# Animation function that generates random colored twinkles
twinkle_chance = 0.03
random_color = False
def twinkle_animation():
    fade_string(cp.pixels)
    fade_string(pixel_string)
    color = wheel(random.randint(0,255)) if random_color else color_from_acc()
    blink_on(cp.pixels, twinkle_chance, color)
    blink_on(pixel_string, twinkle_chance, color)


# Record whether button A is pressed or not so we can detect when it changes
stateA = cp.button_a

# These variables help keep track of when it's time to draw the next "frame"
# in our LED animation without using the "time.sleep()" function. This lets
# our animations be "non blocking" so we can detect sensor input while still
# maintaining a consistent framerate for the LED animation
last_animate_time = 0
animate_delay = 0.04

anims = [twinkle_animation, rainbow_animation, comet_animation]
anim_index = 0
cur_anim = anims[anim_index]

# number of seconds it takes to cycle the rainbow through
# the color spectrum
rainbow_index = 1
while True:
    # Check for sensor inputs
    
    # Check to see if button A was pushed
    # Pressing button A advances to the next animation
    if cp.button_a != stateA: # State of A has changed
        if cp.button_a:
            print("A pressed")
            # Change to the next animation
            anim_index = (anim_index + 1) % len(anims)
            cur_anim = anims[anim_index]
        stateA = cp.button_a
        
    # TODO: Check for capacitive input touches and select a
    # specific animation based on which pin was touched

    # Determine if we should draw the next animation frame
    now = time.monotonic()
    if now - last_animate_time > animate_delay:
        last_animate_time = now     # update the time of the most recent frame
        cur_anim()                  # call the current animation

