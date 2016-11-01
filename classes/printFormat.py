#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from helper.conversion import *

##
# @file printFormat.py
# PrintFormat
#


##Class Print format
#
class PrintFormat(object):

    ##@var width
    #Width

    ##@var height
    #Height

    ##@var fullPrint
    #Fullprint or not

    ##@var marginWidth
    #Margin width

    ##@var marginHeight
    #Margin height

    ##@var osname
    #OS name

    ##@var dpiStretch
    #dpi stretch or not

    ##Constructor
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
        self.osname = "NoPrinterName"
        print "create print format %smm %smm" %(self.width,self.height)

    ##The Selphy CP900 printer
    #@return : PrintFormat
    @staticmethod
    def SelphyCP900(dpiStretch=False):
        printer = PrintFormat(100,148,"mm")
        printer.dpiStretch = dpiStretch
        printer.osname = "Canon_CP900"
        return printer

    ##The DNP printer
    #@return : PrintFormat
    @staticmethod
    def DNPDS620(dpiStretch=False):
        printer = PrintFormat(100,152,"mm")
        printer.dpiStretch = dpiStretch
        printer.osname = "DNPDS620"
        return printer

    ##set stretch horizontal or vertical based on ppi/ppmmm
    #@return : void
    def setDpiStretch(self,state):
        self.dpiStretch = state

    ##print format ratio
    #@return : float
    def ratio(self):
        return self.width / self.height

    ##printable format ratio
    #@return : float
    def printableRatio(self):
        (printableAreaWidth,printableAreaHeight) = self.getPrintableArea()
        return printableAreaWidth / printableAreaHeight

    ##Global margin, each is divided by 2 on left,right,top and bottom
    #@return : void
    def setPrinterMargin(self,marginWidth,marginHeight,dimension="mm"):
        if (dimension=="in"):
            self.marginWidth = inch2mm(marginWidth)
            self.marginHeight = inch2mm(marginHeight)
        else:
            self.marginWidth = marginWidth
            self.marginHeight = marginHeight

    ##Area in millimeters
    #@return :  (width,height)
    def getPrintableArea(self):
        return (self.width - self.marginWidth,self.height - self.marginHeight)

    ##Print function
    def __repr__(self):
        return "PrintFormat()"

    ##Print function
    def __str__(self):
        return "[osname/width/height/marginWidth/marginHeight/DpiStretch] : [%s/%smm/%smm/%s/%s/%s]" %(self.osname,self.width,self.height, self.marginWidth,self.marginHeight,self.dpiStretch)
