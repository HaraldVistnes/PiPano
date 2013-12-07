#!/usr/bin/env python

""" Script for annotating text and timestamps to images

    Copyright (C) 2013 Harald Vistnes <harald.vistnes@gmail.com>

"""

import os
import glob

dx = 20
dy = 20

pointsize_time = 24
dy_time = 28

pointsize_date = 16
dy_date = 18

pointsize_location = 32
dy_location = 34


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
    dir,basename = os.path.split(infilename)
    return os.path.join(dir,"p_" + str(index) + ".jpg")
    
def annotate(infilename, index, location):
    date,time = make_timestamp(infilename)
    outfilename = make_outfilename(infilename, index)
    x = dx
    y = dy    
    args = " -resize 1920x1080 -fill white -undercolor '#00000000' -gravity SouthWest"

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
    index = 1
    for f in files:
        annotate(f, index, location)
        index = index+1

if __name__ == "__main__":
    annotate_dir('/media/harald/DATAPART1/PiPano/20131207/images/1/img_*.jpg', "Kirkehamn")

