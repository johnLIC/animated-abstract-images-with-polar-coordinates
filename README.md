# animated-abstract-images-with-polar-coordinates
multithreaded python script to make animated mandala like art

I run this on a linux machine.  Run this from the command line like this:  

Usage:
>./polar_v26.py 1 90 0 1 1

The code that parses the output file names expects the above format.  If you do 

>python ./polar_v26.py 1 90 0 1 1 

the dirs and files that are made will have the wrong names, iirc.  The arguments are like this:

> ./polar_v26.py <start frame> <end frame> <display image(s) flag> <save image(s) flag> < generate gif flag>
  
This code is always evolving, so I have not cleaned it up at all.  There is a function called mandel() which will make a Mandelbrot set image, which is not being used now.

Have a look at lines 125 and 126.  The code is set up to multi-thread with 10 threads.  Change the 10's on lines 125 and 126 to whatever you want, depending on your CPU.

The conversion to a .gif at the bottom uses the convert command which is available in ffmpeg, so you will need to install that if you want automatic gif making.

For testing a single frame the command line loks like this:

>./polar_v26.py 12 12 1 0 0

That would render and display frame 12, without saving, or generating a gif.

Please let me know if you have improvements, or end up making anytihng cool!
