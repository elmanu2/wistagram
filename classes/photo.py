#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from conversion import *

class Photo(object):
    def __init__(self,resX,resY,dimension="mm"):
        self.resX = resX
        self.resY = resY
        self.ppi = 1
    #print "create photo"

    def ratio(self):
        return resX / resY

    def printInfo(self):
        print "[resX-resY-ppi] [%d-%d-%d]" %(self.resX,self.resY,self.ppi)

    def computePpmm(self,printFormat):
        (width,height) = printFormat.getPrintableArea()
        ppmmX = ppmm(self.resX,width)
        ppmmY = ppmm(self.resY,height)
        self.ppmm = max(ppmmX,ppmmY)
        self.ppi = ppmm2ppi(self.ppmm)
        self.width = self.resX / self.ppmm
        self.height = self.resY / self.ppmm
        return self.ppmm

    def computePpi(self,printFormat):
        self.computePpmm(printFormat)
        return self.ppi

    def getSize(self):
        return (self.width,self.height)


