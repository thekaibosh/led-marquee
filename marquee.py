#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import argparse

# LED strip configuration:
LED_COUNT = 144       # Number of LED pixels.
ROW_COUNT = 9         # Number of pixel rows
COL_COUNT = 16        # Number of pixel columns
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def getStripOrdinal(x,y):
    if x % 2 == 0:
        return x * COL_COUNT + y
    else:
        return (x+1) * COL_COUNT - (y+1)

def extractColumns(matrix,n,m):
    if n<0 or m>=len(matrix[0]):
        raise ValueError("Column indices out of range")

    extractedMatrix = [row[n:(m+1)] for row in matrix]]
    return extractedMatrix

def convertPixelsToMatrix(pixels,numRows,numCols):
    matrix = []
    for y in range(numRows):
        row=[]
        for x in range(numCols):
            row.append(pixels[x,y])
        matrix.append(row)
    return matrix
    
#this pulls a number of columns out of a matrix
#returning from the the nth to the mth. If m is
#greater than the size of the matrix, remaining
# columns will be pulled starting at the 0th
#this will be used for animating the viewframe
#since the matrix will likely be smaller than the 
#message
def extractColumns(matrix,start,colsToExtract):
    rowSize = len(matrix[0])

    if start < 0 or start >= row_size:
        raise ValueError("starting column index out of range")
    #calculate ending column index
    end = (n+colsToExtract -1) % rowSize
    
    extractedMatrix = [matrix[i][(start+j) % rowSize] for i in range(len(matrix)) for j in range(colsToExtract)]
    return extractedMatrix

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def createPixels(text,size):
    #monospaced fonts are the same height and width
    image_width=len(display_text)*font_size
    image_height=font_size+2
    # Create new black image
    img=Image.new('RGB',(image_width,image_height),color="black")

    #write text on image
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("c64_pro_mono.ttf",font_size)
    draw.text((0,1),display_text,(175,0,0), font=font)

    # create pixel map, which is matrix of RGB tuples
    pixel_map = img.load()
    return pixel_map
    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    display_text = "ABC"
    font_size = 7

    pixel_map = create_Pixels(display_text,font_size)
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            for i in range(ROW_COUNT):
                for j in range(COL_COUNT):
                    ord=getStripOrdinal(i,j)
                    colorBmp = pixel_map[j,i]
                    strip.setPixelColor(ord,Color(colorBmp[2] if colorBmp[2]==175 else 0,colorBmp[0] if colorBmp[0]==175 else 0,colorBmp[1] if colorBmp[1]==175 else 0))
            strip.show()
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
