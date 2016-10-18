#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math


def inch2mm(lengthInInches):
    return lengthInInches * 25.4

def mm2inch(lengthInMm):
    return lengthInMm / 25.4

#return pixel per millimeter
def ppmm(resolution,length,dimension="mm"):
    if(dimension == "in"):
        return resolution / float(inch2mm(length))
    else:
        return resolution / float(length)

def ppmm2ppi(ppmm):
    return int(math.floor(ppmm / mm2inch(1)))

#return length in mm
def length(resolution,ppmm):
    return resolution * ppmm

#return resolution
def resolution(length, ppmm,dimension="mm"):
    if(dimension == "in"):
        return inch2mm(length) / float(ppmm)
    else:
        return length / float(ppmm)





