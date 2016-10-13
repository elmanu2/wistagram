#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from conversion import *

class PrintFormat(object):
    def __init__(self,width,height,dimension="mm"):
        if (dimension=="in"):
            self.width = inch2mm(width)
            self.height = inch2mm(height)
        else:
            self.width = width
            self.height = height
        print "create print format %smm %smm" %(self.width,self.height)

    def ratio(self):
        return self.width / self.height

    def printableRatio(self):
        (printableAreaWidth,printableAreaHeight) = self.getPrintableArea()
        return printableAreaWidth / printableAreaHeight

    #Global margin, each is divided by 2 on left,right,top and bottom
    def setMargin(self,marginWidth,marginHeight,dimension="mm"):
        if (dimension=="in"):
            self.marginWidth = inch2mm(marginWidth)
            self.marginHeight = inch2mm(marginHeight)
        else:
            self.marginWidth = marginWidth
            self.marginHeight = marginHeight

    #Result : Area (width,height) in millimeters
    def getPrintableArea(self):
        return (self.width - self.marginWidth,self.height - self.marginHeight)
