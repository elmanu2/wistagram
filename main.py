#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from classes.photo import Photo
from classes.printFormat import PrintFormat
from classes.configuration import Configuration
from classes.printer import Printer
from helper.conversion import *
from helper.compositing import *

##
# @file main.py
# Main
#

## return immediate subdirectories
#@return [String]
def getImmediateSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

## User prompt for an index in an array
#@return int
def userSelectionInArray(subDirArray):
    selection = -1
    while ( (selection < 0) or (selection >= len(subDirArray))):
        for idx, val in enumerate(subDirArray):
            print"[%d -> %s]" %(idx,val)

        userSelection = raw_input()
        selection =  int(float(userSelection))
    return selection

## return a list of *.jpg files\n
# exclude files with "print"\n
# exclude files with "template"\n
# exclude files with "python"
#@return [String]
def listScreenShotFiles(inputDir):
    filelist=os.listdir(inputDir)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        #Remove files which are not jpeg files
        if not(fichier.endswith(".jpg")):
            filelist.remove(fichier)
        #Remove files which have been generated by this script
        elif "print" in fichier:
            filelist.remove(fichier)
        #Remove files which have been generated by this script
        elif "template" in fichier:
            filelist.remove(fichier)
        elif "python" in fichier:
            filelist.remove(fichier)


    #print(filelist)
    return filelist


##MAIN
def main():


    #The root directory
    inputDir = "/Users/manu/Desktop/wistiti/"
    #The configuration file directory
    configDir = os.path.join(inputDir, "configurations")

    #USE CONFIGURATION FILE
    #Ask user for configuration
    files = Configuration.listConfigurationFiles(configDir)
    selection = Configuration.userSelection(files)
    selectionFilepath = os.path.join(configDir,files[selection])
    cfg = Configuration(selectionFilepath)

    print cfg

    #templateFile = "./resources/test/template/COR-MARS16_elements-template-gimp.jpg"
    useTemplate = cfg.getUseTemplate()
    if(useTemplate == True):
        templateFile = cfg.getTemplateName()
    else:
        templateFile = "NoTemplate"

    #marginColor = (84,158,167)
    marginColor = cfg.getTemplateColor()
    #TODO = Manage difference between width and height margins
    templateMargin = cfg.getPrinterMarginTemplate()[0]
    photoMargin = cfg.getPrinterMarginPhoto()[0]
    #The printer
    if(cfg.getPrinterOsName() == "Canon_CP900"):
        printFormat = PrintFormat.SelphyCP900(dpiStretch=cfg.getPrinterDpiStretch())
    elif(cfg.getPrinterOsName() == "Dai_Nippon_Printing_DP_DS620"):
        printFormat = PrintFormat.DNPDS620(dpiStretch=cfg.getPrinterDpiStretch())
    elif(cfg.getPrinterOsName() == "DNPDS620"):
        print "No osname and osformat for this printer %s\n"\
              "Change the configuration file. Quit" %(cfg.getPrinterOsName())
        return
    else :
        print "No printer with this name %s, quit" %(cfg.getPrinterOsName())
        return
    printFormat.setPrinterMargin(cfg.getPrinterMargin()[0],
                                 cfg.getPrinterMargin()[1],
                                 cfg.getPrinterMarginDim)
    print printFormat
    #END OF USE CONFIGURATION FILE


    #Add a margin on the template (add new pixel for printer margin)
    templateFile = addMarginOnTemplate(templateFile,templateMargin,marginColor=marginColor)

    #Get the subdirectories that include instagram pictures
    subDirArray = getImmediateSubdirectories(inputDir)

    #User chooses the subdirectory
    userIndexSelection = userSelectionInArray(subDirArray)
    inputDir = os.path.join(inputDir,subDirArray[userIndexSelection])
    #Get the images list (jpg)
    files = listScreenShotFiles(inputDir)

    #Display information for user
    print "********************************"
    print "%s files found" %(len(files))
    print files
    print "********************************"

    userInput = ""
    index = 0
    if(len(files) == 0):
        print "No compatible file in this directory, quit..."
        return

    while(userInput != "q"):
        #Open the picture image
        filepath = os.path.join(inputDir,files[index])
        (filepathWithoutExtension,extension) = os.path.splitext(filepath)

        #fileOutput = filepathWithoutExtension + "-python" + extension
        #print filepathWithoutExtension
        #print extension
        #print fileOutput

        #Add a photo on the template
        photoPath = addPhotoOnTemplate(filepath,templateFile,margin=photoMargin)
        im = Image.open(photoPath)

        #exif_data = im._getexif()
        #print im.info
        #print exif_data
        photo = Photo(im.size[0],im.size[1])
        photo.computePpmm(printFormat)
        print "********************************"
        print "File %s on %s : %s" %(index+1,len(files),files[index])
        print photo
        fileOutput = generateFilepathWithSuffix(photoPath,"-CP900-print")
        im.save(fileOutput, 'jpeg', dpi = (photo.ppiX,photo.ppiY))
        im2 = Image.open(fileOutput)

        #User choose the action
        userInput = raw_input("Print? print/next/display/quit [p/n/d/q]")
        #print "Resultat %s" % userInput
        if userInput == "p":
            print im2.info
            printCommand = Printer.computePrinterCommand(fileOutput,
                                                  cfg.getPrinterOsName(),
                                                  cfg.getPrinterOsFormat())
            Printer.sendPrinterJob(printCommand)
            print "INFO : YOU CAN PRINT THE SAME IMAGE"
        elif userInput == "n":
            print "Next picture"
            index += 1
        elif userInput == "d":
            print "Display"
            im.show()
        elif userInput == "q":
            print "Quit"
        else :
            print "Unknown command"

        if(index >= len(files)):
            userInput = "q"
            print "No more picture, quit..."

if __name__ == "__main__":
    main()

