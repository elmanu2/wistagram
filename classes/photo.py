#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from helper.conversion import *


##Class to compute PPI(or DPI)
#
class Photo(object):

    ##@var resX
    #Horizontal resolution

    ##@var resY
    #Vertical resolution

    ##@var  ppmm
    #Pixel per millimeter

    ##@var  ppi
    #Pixel per inch

    ##@var ppiX
    #Horizontal pixel per inch

    ##@var ppiY
    #Vertical pixel per inch

    ##@var ppmmX
    #Horizontal pixel per millimeter

    ##@var ppmmY
    #Vertical pixel per millimeter

    ##@var width
    #Width

    ##@var height
    #Height

    ##Constructor
    def __init__(self,resX,resY,dimension="mm"):
        self.resX = resX
        self.resY = resY
        #default PPI
        self.ppmm = 2.8346
        self.ppi = 72
        self.ppiX = self.ppi
        self.ppiY = self.ppi
        self.ppmmX = self.ppmm
        self.ppmmY = self.ppmm
        self.width = self.resX / self.ppmmX
        self.height = self.resY / self.ppmmY
    #print "create photo"

    ##ratio of the picture
    #@return : Float
    def ratio(self):
        return self.resX / float(self.resY)

    ##Display ratio in output
    #@return : void
    def printInfo(self):
        print "[resX-resY-ppi] [%d-%d-%d]" %(self.resX,self.resY,self.ppi)

    ##Compute ppmm,ppi,ppmmX,ppmmY,ppiX,ppiY
    #@return : Float
    def computePpmm(self,printFormat):
        (width,height) = printFormat.getPrintableArea()

        self.ppmmX = ppmm(self.resX,width)
        self.ppmmY = ppmm(self.resY,height)
        self.ppmm = max(self.ppmmX,self.ppmmY)
        self.ppi = ppmm2ppi(self.ppmm)

        #If no ppi stretching, then ppiX == ppiY = ppi
        if(printFormat.dpiStretch == False):
            self.width = self.resX / self.ppmm
            self.height = self.resY / self.ppmm
            self.ppiX = ppmm2ppi(self.ppmm)
            self.ppiY = ppmm2ppi(self.ppmm)
        #else ppi stretching
        else:
            self.width = self.resX / self.ppmmX
            self.height = self.resY / self.ppmmY
            self.ppiX = ppmm2ppi(self.ppmmX)
            self.ppiY = ppmm2ppi(self.ppmmY)

#        print "\nCOMPUTE PPMM\n"
#        print "printable area %s,%s" %(width,height)
#        print "resX,resY %s,%s" %(self.resX,self.resY)
#        print "ppmmX,ppmmY %s,%s" %(self.ppmmX,self.ppmmY)
#        print "ppiX,ppiY %s,%s" %(self.ppiX,self.ppiY)
#        print "width,height %s,%s" %(self.width,self.height)

        return self.ppmm

    ##Compute ppi and ppmm
    #@return : Float
    def computePpi(self,printFormat):
        self.computePpmm(printFormat)
        return self.ppi

    ##compute value to resize photo or template\n
    #Thanks to this function, we keep a good ppi for printer\n
    #margin in pixel
    #@return : ((float,float),(float,float))
    def addTemplate(self,templateResX,templateResY,margin):
        #if photo is greater than template
        newResX =newResY = 0
        #if photo with margin is bigger than template
        if ( (self.resX + margin * 2) > templateResX):
            #Keep photo size, resize template
            newPhotoResX = self.resX
            newPhotoResY = self.resY
            newTemplateResX = self.resX + margin * 2
            newTemplateResY = newTemplateResX * templateResY / float(templateResX)
            newTemplateResX = int(math.floor(newTemplateResX))
            newTemplateResY = int(math.floor(newTemplateResY))
        #if photo with margin is smaller than template
        else :
            newPhotoResX = int(math.floor(templateResX - margin * 2))
            newPhotoResY = int(math.floor(newPhotoResX / self.ratio()))
            newTemplateResX = templateResX
            newTemplateResY = templateResY

        print "NEW PHOTO RES : %s %s" %(newPhotoResX,newPhotoResY)
        print "NEW TEMPLATE RES : %s %s" %(newTemplateResX,newTemplateResY)

        return ((newPhotoResX,newPhotoResY),(newTemplateResX,newTemplateResY))

    ##return size in mm
    #@return : (float,float)
    def getSize(self):
        return (self.width,self.height)

    ##Print functio
    def __repr__(self):
        return "Photo()"

    ##Print functio
    def __str__(self):
        return "[resX/resY/Width/Height/PPIX,PPIY] : [%s/%s/%smm/%smm/%s/%s]" %(self.resX,self.resY,self.width, self.height,self.ppiX,self.ppiY)


