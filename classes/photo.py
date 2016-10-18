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
        self.fullPrint = False
    #print "create photo"

    def ratio(self):
        return resX / resY

    #Will stretch the Image when printing if true
    def setFullPrint(self,state):
        self.fullPrint = state

    def printInfo(self):
        print "[resX-resY-ppi] [%d-%d-%d]" %(self.resX,self.resY,self.ppi)

    def computePpmm(self,printFormat):
        (width,height) = printFormat.getPrintableArea()

        self.ppmmX = ppmm(self.resX,width)
        self.ppmmY = ppmm(self.resY,height)
        self.ppmm = max(self.ppmmX,self.ppmmY)
        self.ppi = ppmm2ppi(self.ppmm)

        if(self.fullPrint == False):
            self.width = self.resX / self.ppmm
            self.height = self.resY / self.ppmm
            self.ppiX = ppmm2ppi(self.ppmm)
            self.ppiY = ppmm2ppi(self.ppmm)
        else:
            self.width = self.resX / self.ppmmX
            self.height = self.resY / self.ppmmY
            self.ppiX = ppmm2ppi(self.ppmmX)
            self.ppiY = ppmm2ppi(self.ppmmY)

        print "\nCOMPUTE PPMM\n"
        print "printable area %s,%s" %(width,height)
        print "resX,resY %s,%s" %(self.resX,self.resY)
        print "ppmmX,ppmmY %s,%s" %(self.ppmmX,self.ppmmY)
        print "ppiX,ppiY %s,%s" %(self.ppiX,self.ppiY)
        print "width,height %s,%s" %(self.width,self.height)

        return self.ppmm

    def computePpi(self,printFormat):
        self.computePpmm(printFormat)
        return self.ppi

    def getSize(self):
        return (self.width,self.height)


