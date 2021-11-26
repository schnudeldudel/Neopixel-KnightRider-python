# NeoPixel-KnightRider
#
# Python implementation of https://github.com/technobly/NeoPixel-KnightRider 
#
# A highly configurable Knight Rider (larson display) routine for your NeoPixels
# (WS2812 RGB LED).
#
# Use it with a RaspberryPi and rpi-ws281x-python library 
# (see https://github.com/rpi-ws281x/rpi-ws281x-python)
#
# depends on:
# rpi-ws281x==4.3.1
#
# The MIT License (MIT)
#
# Copyright (c) 2013 Technobly - technobly@gmail.com - August 13th 2013
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from rpi_ws281x import PixelStrip, Color
import time

# LED strip configuration:
LED_COUNT   = 8       # Number of LED pixels in strip
LED_PIN     = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN    = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def clearStrip():
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()


def hex2color(color):
    red = (color & 0xFF0000) >> 16
    green = (color & 0x00FF00) >> 8
    blue = (color & 0x0000FF) >> 0

    return Color(red, green, blue)


def dimColor(color, width):
    red = (color & 0xFF0000) >> 16
    green = (color & 0x00FF00) >> 8
    blue = (color & 0x0000FF) >> 0

    dim_red = int(red/width)
    dim_green = int(green/width)
    dim_blue = int(blue/width)

    dim = Color(dim_red, dim_green, dim_blue)
    return dim

def knightRider(cycles=10, speed = 32, width = 4, col = 0xFF1000 ):

    """
    Credits for the idea & effect implementation to https://github.com/technobly/NeoPixel-KnightRider 

    Cycles - one cycle is scanning through all pixels left then right (or right then left)
    Speed - how fast one cycle is (32 with 16 pixels is default KnightRider speed)
    Width - how wide the trail effect is on the fading out LEDs.  The original display used
            light bulbs, so they have a persistance when turning off.  This creates a trail.
            Effective range is 2 - 8, 4 is default for 16 pixels.  Play with this.
    Color - 32-bit packed RGB color value.  All pixels will be this color."""

    # https://github.com/technobly/NeoPixel-KnightRider
    # uint32_t old_val[NUM_PIXELS]; // up to 256 lights!
    # // Larson time baby!
    # for(int i = 0; i < cycles; i++)

    # special conversion needed for rpi_ws281x lib
    color = hex2color(col)

    # setup the old_val list before using it
    old_val = []
    for i in range(strip.numPixels()):
        old_val.append(i)

    # for(int i = 0; i < cycles; i++)
    for i in range(0, cycles, 1):
    #   for (int count = 1; count<NUM_PIXELS; count++) {
        for count in range(1, strip.numPixels(), 1):
            # strip.setPixelColor(count, color);
            strip.setPixelColor(count, color)
    #       old_val[count] = color;
            old_val[count] = color
    #       for(int x = count; x>0; x--) {
            for x in range(count, 0, -1):
    #           old_val[x-1] = dimColor(old_val[x-1], width);
                old_val[x-1] = dimColor(old_val[x-1], width)
    #           strip.setPixelColor(x-1, old_val[x-1]);
                strip.setPixelColor(x-1, old_val[x-1])
            strip.show()
    #       delay(speed);
            time.sleep(speed/1000)
    #     }

    #   for (int count = NUM_PIXELS-1; count>=0; count--) {
        for count in range(strip.numPixels()-2, -1, -1):
    #       strip.setPixelColor(count, color);
            strip.setPixelColor(count, color)
    #       old_val[count] = color;
            old_val[count] = color
    #       for(int x = count; x<=NUM_PIXELS ;x++) {
            for x in range(count, strip.numPixels()-1, +1):
    #           old_val[x-1] = dimColor(old_val[x-1], width);
                old_val[x+1] = dimColor(old_val[x+1], width)
    #           strip.setPixelColor(x+1, old_val[x+1]);
                strip.setPixelColor(x+1, old_val[x+1])
    #     }
            strip.show()
    #       delay(speed);
            time.sleep(speed/1000)
    #     }
    # }



if __name__ == '__main__':
    
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                                LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    clearStrip()

    knightRider(3, 32, 4, 0x0000FF) # Cycles, Speed, Width, RGB Color (original orange-red)
    knightRider(3, 32, 3, 0xFF00FF) # Cycles, Speed, Width, RGB Color (purple)
    knightRider(3, 32, 2, 0x0000FF) # Cycles, Speed, Width, RGB Color (blue)
    knightRider(3, 32, 5, 0xFF0000) # Cycles, Speed, Width, RGB Color (red)
    knightRider(3, 32, 6, 0x00FF00) # Cycles, Speed, Width, RGB Color (green)
    knightRider(3, 32, 7, 0xFFFF00) # Cycles, Speed, Width, RGB Color (yellow)
    knightRider(3, 32, 8, 0x00FFFF) # Cycles, Speed, Width, RGB Color (cyan)
    knightRider(3, 32, 2, 0xFFFFFF) # Cycles, Speed, Width, RGB Color (white)
    clearStrip()

    # That's all folks.

