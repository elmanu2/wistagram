#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import io
import os


#Configuration
class Configuration(object):
    def __init__(self,filename):
        self.filename = filename
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        self.rawConfiguration = config

    #Template filepath
    #return : String
    def getTemplateName(self):
        return self.rawConfiguration.get('template', 'templateFilepath')

    #Template margin color
    #return : (Int,Int,Int)
    def getTemplateColor(self):
        rawColor = self.rawConfiguration.get('template', 'color')
        rgb = rawColor.split(',')
        return (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    #Printer OS name
    #return : String
    def getPrinterName(self):
        return self.rawConfiguration.get('printer','name')

    #Use Dpi stretch
    #return : BOOL
    def getPrinterDpiStretch(self):
        rawDpiStretch = self.rawConfiguration.get('printer','dpiStretch')
        return Configuration.str2Bool(rawDpiStretch)

    #Printer margin
    #return : (Int,Int)
    def getPrinterMargin(self):
        rawFormat = self.rawConfiguration.get('printer','margin')
        return Configuration.splitFormat(rawFormat)

    #Printer margin dimension : "mm" or "inch"
    #return : String
    def getPrinterMarginDim(self):
        return self.rawConfiguration.get('printer','marginDim')

    #Printer margin photo in pixels
    #return : (Int,Int)
    def getPrinterMarginPhoto(self):
        rawFormat = self.rawConfiguration.get('printer','marginphoto')
        return Configuration.splitFormat(rawFormat)

    #Printer margin template in pixels
    #return : (Int,Int)
    def getPrinterMarginTemplate(self):
        rawFormat = self.rawConfiguration.get('printer','margintemplate')
        return Configuration.splitFormat(rawFormat)

    #Convert a string into a boolean value
    #return : BOOL
    @staticmethod
    def str2Bool(text):
        if text == "True":
            return True
        elif text == "true":
            return True
        elif text == "1":
            return True
        elif text == "Yes":
            return true
        elif text == "yes":
            return True
        else:
            return False

    #Convert a string into a 3-uplet for colors
    #return : (Int,Int,Int)
    @staticmethod
    def splitColor(text):
        rgb = text.split(',')
        return (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    #Convert a string into a 2-uplet for (width,height)
    #return : (Int,Int)
    @staticmethod
    def splitFormat(text):
        widthHeight = text.split('x')
        return (int(widthHeight[0]),int(widthHeight[1]))

    #List the *.cfg file in a directory
    #return : [String]
    @staticmethod
    def listConfigurationFiles(inputDir):
        filelist=os.listdir(inputDir)
        for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
            #Remove files which are not jpeg files
            if not(fichier.endswith(".cfg")):
                filelist.remove(fichier)
        #print(filelist)
        return filelist

    #User index selection in an array
    #return : Int
    @staticmethod
    def userSelection(fileArray):
        selection = -1
        print "Select the configuration file ? (enter a number) :"
        while ( (selection < 0) or (selection >= len(fileArray))):
            for idx, val in enumerate(fileArray):
                print"[%d -> %s]" %(idx,val)

            userSelection = raw_input()
            selection =  int(float(userSelection))
        return selection

    def __repr__(self):
        return "Configuration()"

    def __str__(self):
        printValue = "[filename -> %s]\n" %(self.filename)
        printValue += "[template name -> %s]\n" %(self.getTemplateName())
        printValue += "[template color -> (%s,%s,%s)]\n" %(self.getTemplateColor())
        printValue += "[printer name -> %s]\n" %(self.getPrinterName())
        printValue += "[printer Dpi Stretch -> %s]\n" %(self.getPrinterDpiStretch())
        printValue += "[printer margin -> (%sx%s)]\n" %(self.getPrinterMargin())
        printValue += "[printer margin dimension -> %s]\n" %(self.getPrinterMarginDim())
        printValue += "[printer margin template -> (%sx%s)pixels]\n" %(self.getPrinterMarginTemplate())
        printValue += "[printer margin photo -> (%s,%s)pixels]\n" %(self.getPrinterMarginPhoto())
        return printValue


def unitTest():
    rootDirectory = "/Users/manu/Desktop/wistiti/configurations"
    files = Configuration.listConfigurationFiles(rootDirectory)
    selection = Configuration.userSelection(files)
    selectionFilepath = os.path.join(rootDirectory,files[selection])

    configuration = Configuration(selectionFilepath)
    #Template configuration
    templateName = configuration.getTemplateName()
    templateColor = configuration.getTemplateColor()
    #Printer configuration
    printerName = configuration.getPrinterName()
    printerDpiStretch = configuration.getPrinterDpiStretch()
    printerMargin = configuration.getPrinterMargin()
    printerMarginDimension = configuration.getPrinterMarginDim()
    printerMarginTemplate = configuration.getPrinterMarginTemplate()
    printerMarginPhoto = configuration.getPrinterMarginPhoto()

    assert(len(files) > 0)

    #Test Printer configuration
    assert(printerName == "SelphyCP900")

    #Test Format configuration
    assert(templateName == "./resources/test/template/COR-NOV16_elements-template-instagram_FLASH-gimp.jpg")
    assert(templateColor == (216,123,98))

    
    assert(printerDpiStretch)
    assert(printerMargin == (-1,-1))
    assert(printerMarginDimension == "mm")
    assert(printerMarginTemplate == (30,30))
    assert(printerMarginPhoto == (60,60))


def main():
    unitTest()

if __name__ == "__main__":
    main()
