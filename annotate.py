#!/usr/bin/env python

""" Script for annotating text and timestamps to images

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

"""

import os
import glob
from optparse import OptionParser

dx = 20
dy = 20

pointsize_time = 24
dy_time = 28

pointsize_date = 16
dy_date = 18

pointsize_location = 32
dy_location = 34

fps = 15

def monthstring(month):
    months = [ "", "januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember" ]
    return months[month]

def make_timestamp(filename):
    basename = os.path.basename(filename)
    year = basename[4:8]
    month = monthstring(int(basename[8:10]))
    day = str(int(basename[10:12]))
    hour = basename[13:15]
    minute = basename[15:17]
    return day + ". " + month + " " + year, hour + ":" + minute

def make_outfilename(infilename, index):
    folder,basename = os.path.split(infilename)
    return os.path.join(folder,"p_" + str(index) + ".jpg")
    
def annotate(infilename, index, location):
    date,time = make_timestamp(infilename)
    outfilename = make_outfilename(infilename, index)
    x = dx
    y = dy    
    args = " -resize 1600x1200 -fill white -undercolor '#00000000' -gravity SouthWest"

    args += " -pointsize " + str(pointsize_time) + " -annotate +" + str(x) + "+" + str(y) + " '" + time + "'"
    y += dy_time

    args += " -pointsize " + str(pointsize_date) + " -annotate +" + str(x) + "+" + str(y) + " '" + date + "'"
    y += dy_date

    if location:
        args += " -pointsize " + str(pointsize_location) + " -annotate +" + str(x) + "+" + str(y) + " '" + location + "'"
        y += dy_location
        
    os.system("convert " + infilename + args + " " + outfilename)

def annotate_dir(d, location):
    files = glob.glob(d)
    files.sort()
    index = 1
    for f in files:
        print 'Annotating ' + f
        annotate(f, index, location)
        index = index+1

def make_video(folder, videofile):
    os.system("ls -1tr " + folder + "p*.jpg > " + folder + "files.txt")
    print 'Creating uncompresed video...'
    os.system("mencoder -nosound -noskip -oac copy -ovc copy -o " + folder + "tmp_output.avi -mf fps=" + str(fps) + " 'mf://@" + folder + "files.txt'")
    print 'Compressing video...'
    os.system("mencoder -ovc x264 " + folder + "tmp_output.avi -o " + folder + videofile)
    print 'Cleaning up...'
    os.remove(folder + "tmp_output.avi")

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="indir", help="Folder containing input images")
    parser.add_option("-l", "--location", dest="location", help="Location string to be annotated")
    parser.add_option("-v", "--video", dest="avifile", help="Generate timelapse video")
    parser.add_option("-f", "--fps", dest="fps", help="Video fps")

    (options, args) = parser.parse_args()

    if options.fps:
        fps = options.fps

    if options.indir:
        if options.indir[-1] != '/':
            options.indir += '/'

        annotate_dir(options.indir + "img_*.jpg", options.location)

        if options.avifile:
            make_video(options.indir, options.avifile)

if __name__ == "__main__":
    main()

