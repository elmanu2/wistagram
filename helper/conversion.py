#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

##
# @file conversion.py
# Conversion operation
#


##Inch to millimeter
#@return float
def inch2mm(lengthInInches):
    return lengthInInches * 25.4

##Millimeter to inch
#@return float
def mm2inch(lengthInMm):
    return lengthInMm / 25.4

##ppmm from resolution and size
#@return float -> pixel per millimeter
def ppmm(resolution,length,dimension="mm"):
    if(dimension == "in"):
        return resolution / float(inch2mm(length))
    else:
        return resolution / float(length)

##ppmm2ppi
#@return float -> pixel per icnh
def ppmm2ppi(ppmm):
    return int(math.floor(ppmm / mm2inch(1)))
    #We can't set a ppi as int when saving file with PIL
    #return ppmm / mm2inch(1)

##ppi2ppmm
#@return float
def ppi2ppmm(ppi):
    return float(ppi / inch2mm(1))

#return length in mm
#@return float
def length(resolution,ppmm):
    return resolution * ppmm

#resolution from lentgh and ppmm
#@return float resolution
def resolution(length, ppmm,dimension="mm"):
    if(dimension == "in"):
        return inch2mm(length) / float(ppmm)
    else:
        return length / float(ppmm)





