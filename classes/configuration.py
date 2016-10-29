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

    def getTemplateName(self):
        return self.rawConfiguration.get('template', 'templateFilepath')

    def getTemplateColor(self):
        rawColor = self.rawConfiguration.get('template', 'color')
        rgb = rawColor.split(',')
        return (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def getPrinterName(self):
        return self.rawConfiguration.get('printer','name')

    def getPrinterDpiStretch(self):
        rawDpiStretch = self.rawConfiguration.get('printer','dpiStretch')
        return Configuration.str2Bool(rawDpiStretch)

    def getPrinterMargin(self):
        rawFormat = self.rawConfiguration.get('printer','margin')
        return Configuration.splitFormat(rawFormat)

    def getPrinterMarginDim(self):
        return self.rawConfiguration.get('printer','marginDim')

    def getPrinterMarginPhoto(self):
        rawFormat = self.rawConfiguration.get('printer','marginphoto')
        return Configuration.splitFormat(rawFormat)

    def getPrinterMarginTemplate(self):
        rawFormat = self.rawConfiguration.get('printer','margintemplate')
        return Configuration.splitFormat(rawFormat)



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


    @staticmethod
    def splitColor(text):
        rgb = text.split(',')
        return (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    @staticmethod
    def splitFormat(text):
        widthHeight = text.split('x')
        return (int(widthHeight[0]),int(widthHeight[1]))


    @staticmethod
    def listConfigurationFiles(inputDir):
        filelist=os.listdir(inputDir)
        for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
            #Remove files which are not jpeg files
            if not(fichier.endswith(".cfg")):
                filelist.remove(fichier)
        #print(filelist)
        return filelist

    @staticmethod
    def userSelection(fileArray):
        selection = -1
        while ( (selection < 0) or (selection >= len(fileArray))):
            for idx, val in enumerate(fileArray):
                print"[%d -> %s]" %(idx,val)

            userSelection = raw_input()
            selection =  int(float(userSelection))
        return selection

    def __repr__(self):
        return "Configuration()"

    def __str__(self):
        return "[resX/resY/Width/Height/PPIX,PPIY] : [%s/%s/%smm/%smm/%s/%s]" %(self.resX,self.resY,self.width, self.height,self.ppiX,self.ppiY)

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

    

    print files
    print selection
    print selectionFilepath
    print templateName
    print templateColor
    print printerName
    print printerDpiStretch
    print printerMargin
    print printerMarginDimension
    print printerMarginPhoto


def main():
    unitTest()

if __name__ == "__main__":
    main()
