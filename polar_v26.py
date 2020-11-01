#!/usr/bin/python3

# multi-threaded animated mandala (or random image) maker.
# ./multi_v03.py 90 0 1

#  args:
#  1) start frame, sys.argv[0]
#  2) end frame, sys.argv[1]
#  3) flag to display sys.argv[2]
#  4) flag to render sys.argv[3]
#  5) sys.argv[3] make animated gif 0/1

# to make images
from PIL import Image
import math
from math import sin,cos,radians,e,sqrt
import random
import sys
import os

# for multiprocessing
from functools import partial
import time
import multiprocessing
 

#####################################################

def mandel(c):
        z=complex( .6*math.cos(radians(frame*2)), .6*math.sin(radians(frame*2)) )
        for h in range(0,80):
            z = z**2 + c #+ complex(math.sin(frame*4), math.cos(frame*4))
            if abs(z) > 2:
                break
        if abs(z) >= 2:
            return abs(z)
        else:
            return 1.0/(1.0+10*abs(z))


# the multiprocessing version of this seems very picky about data types.
def pixelCalc(t):
    mag = [0,0]
    x = t%W
    y = t/W # t is actually an index into a 1D array
    r = math.sqrt((x-(W/2))**2 + (y-(W/2))**2)
    theta = math.atan2(x-W/2,y-W/2)
    if x<0:
        theta += math.pi
    if y<0:
        theta += math.pi*2

    mag[0] = r #int((r+100*math.sin(.01*r))%80*(255/80)) 
    mag[1] = theta #100*math.log(1+abs(theta+math.sin(4*theta))) % 255.0
    return [ int(x), int(y) ], mag  # return one pixel's color data tuple


# This gets called by the pool - each process does one row.
def imageMaker(t_range):
    t = 0
    while t < W*H:
        pixel = (pixelCalc(t))
        #print pixel
        t = t + 1
        
        x = pixel[0][0]
        y = pixel[0][1]
        mag = pixel[1]
        theta = mag[1]
        r = mag[0]+100*sin(radians(frame*4+60*sin(theta*6 + sin(radians(frame*4)))))        
        #wave = sin(theta) 

        R = int(150 * pow((1.0 + sin(theta + 0.000*math.pi + 12*sin(.030*r) + radians(frame*4))), .5))
        G = int(150 * pow((1.0 + sin(theta + 0.666*math.pi + 12*cos(.030*r) + radians(frame*4))), .5))
        B = int(150 * pow((1.0 + sin(theta + 1.333*math.pi + 12*sin(.030*r) + radians(frame*4))), .5))
        if R < 150:
            R = 0
        if G < 150:
            G = 0
        if B < 150:
            B = 0
        
        RGB[t-1] = (R,G,B)
                
    return RGB

        


# After the pool happens, put the data into an image format, and save and/or gificate the images
def image_array_munger(show, save, gif):
    #print "array munger"
    #print "len(RGB)=", len(RGB)
    RGB_flat = []
    for chunk in RGB:
        #print len(chunk)
        for elem in chunk:
            RGB_flat.append(elem)
    #print "len RGB_flat= ", len(RGB_flat)
    im = Image.new("RGB", (W,H))
    RGB_tuple = (RGB[0])
    im.putdata(RGB_tuple)
    if show==1:
        print ("showing frame " + str(frame))
        im.show()
    if save==1:
        print ("saving " + str(frame))
        if not os.path.exists('render/'+sys.argv[0].split(".")[1] ):
            os.makedirs('render/'+sys.argv[0].split(".")[1] )
        im.save('render/'+sys.argv[0].split(".")[1] + "/" + sys.argv[0].split(".")[1] + "." + str(frame).zfill(4) + '.png')


#####################################################

frame_start = int(sys.argv[1])
frame_end = int(sys.argv[2])
W=1000
H=1000
if __name__=='__main__':
    start = time.clock()
    print ("hello")
    for frame in range(frame_start, frame_end + 1):
        RGB = [(0,0,0)]*W*H  # I don't remember why we want RGB in array_munger
        print (len(RGB))
        pool = multiprocessing.Pool(processes=10)  # run this many processes, so we don't double-write into RGB
        RGB = pool.map(imageMaker, range(0,10))  # run one process for each row in the image
        pool.close()  # "we are not adding any more threads" 
        pool.join()  # wait for all the threads, or maybe that's what the next line does.
        #print "size RGB = " + str(len(RGB))
        #print RGB[0]
        image_array_munger(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))  # assemble image data array, argv[2] = show?, argv[3] = save?

    # make an animated gif
    if sys.argv[5] == "1":    
        input_path = "render/" + sys.argv[0].split(".")[1]+"/"+sys.argv[0].split(".")[1] + ".*.png"
        if not os.path.exists('gif'):
            os.makedirs('gif')
        output_path = "gif/" + sys.argv[0].split(".")[1] + ".gif"
        #  convert -delay 10 -loop 0 render/v08.*.png gif/v002_02.gif
        os.system("convert -delay 10 -loop 0 " + input_path + " " + output_path)

    #print "elapsed time: " + str(time.clock()-start)
