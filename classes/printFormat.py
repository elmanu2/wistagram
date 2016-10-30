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
        self.fullPrint = False
        self.marginWidth = 0
        self.marginHeight = 0
        self.name = "NoPrinterName"
        print "create print format %smm %smm" %(self.width,self.height)

    #The Selphy CP900 printer
    @staticmethod
    def SelphyCP900(dpiStretch=False):
        printer = PrintFormat(100,148,"mm")
        printer.dpiStretch = dpiStretch
        printer.name = "SelphyCP900"
        return printer

    #The DNP printer
    @staticmethod
    def DNPDS620(dpiStretch=False):
        printer = PrintFormat(100,152,"mm")
        printer.dpiStretch = dpiStretch
        printer.name = "DNPDS620"
        return printer

    def setDpiStretch(self,state):
        self.dpiStretch = state

    def ratio(self):
        return self.width / self.height

    def printableRatio(self):
        (printableAreaWidth,printableAreaHeight) = self.getPrintableArea()
        return printableAreaWidth / printableAreaHeight

    #Global margin, each is divided by 2 on left,right,top and bottom
    def setPrinterMargin(self,marginWidth,marginHeight,dimension="mm"):
        if (dimension=="in"):
            self.marginWidth = inch2mm(marginWidth)
            self.marginHeight = inch2mm(marginHeight)
        else:
            self.marginWidth = marginWidth
            self.marginHeight = marginHeight

    #Result : Area (width,height) in millimeters
    def getPrintableArea(self):
        return (self.width - self.marginWidth,self.height - self.marginHeight)

    def __repr__(self):
        return "PrintFormat()"

    def __str__(self):
        return "[name/width/height/marginWidth/marginHeight/DpiStretch] : [%s/%smm/%smm/%s/%s/%s]" %(self.name,self.width,self.height, self.marginWidth,self.marginHeight,self.dpiStretch)
