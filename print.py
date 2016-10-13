#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import popen2
import os
import math

from classes.photo import Photo
from classes.printFormat import PrintFormat
from conversion import *

#Selphy CP 910 : 10x15cm
#                3,93701 x 5,90551 inches
#Format Instagram : 612 x 612 / 1080 x 1080
#PPI pour remplir 10cm -> 612 / 3,93701 -> 155
#                      -> 1080 / 3,93701 -> 274


def getImmediateSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def userSelectionInArray(subDirArray):
    selection = -1
    while ( (selection < 0) or (selection >= len(subDirArray))):
        for idx, val in enumerate(subDirArray):
            print"[%d -> %s]" %(idx,val)

        userSelection = raw_input()
        selection =  int(float(userSelection))
    return selection

def listScreenShotFiles(inputDir):
    filelist=os.listdir(inputDir)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        #Remove files which are not jpeg files
        if not(fichier.endswith(".jpg")):
            filelist.remove(fichier)
        #Remove files which have been generated by this script
        if "-python.jpg" in fichier:
            filelist.remove(fichier)
    #print(filelist)
    return filelist


def testEqualWithAccuracy(float1,float2,precision):
    if ( math.fabs(float1 - float2) < precision):
        return True
    else:
        print "%s is not equal to %s" %(float1,float2)
        return False

def unitTesting():

    #Dimension conversion
    test = inch2mm(4)
    assert(testEqualWithAccuracy(test,101.6,0.01))
    test = inch2mm(6)
    assert(testEqualWithAccuracy(test,152.4,0.01))

    test = mm2inch(101.6)
    assert(testEqualWithAccuracy(test,4.0,0.01))
    test = mm2inch(152.4)
    assert(testEqualWithAccuracy(test,6.0,0.01))

    assert(testEqualWithAccuracy(ppmm(612,91.6),6.68122270742,0.01))
    assert(testEqualWithAccuracy(ppmm2ppi(ppmm(612,91.6)),169.0,0.01))

    print "TESTS ON DIMENSION CONVERSION PASSED SUCCESSFULLY"

    #Print format
    printFormat = PrintFormat(4,6)
    assert(not testEqualWithAccuracy(printFormat.width,101.6,0.01))
    assert(not testEqualWithAccuracy(printFormat.height,152.4,0.01))
    printFormat = PrintFormat(4,6,"in")
    assert(testEqualWithAccuracy(printFormat.width,101.6,0.01))
    assert(testEqualWithAccuracy(printFormat.height,152.4,0.01))
    printFormat.setMargin(10,10,"mm")
    (printAreaWidth,printAreaHeight) = printFormat.getPrintableArea()
    assert(testEqualWithAccuracy(printAreaWidth,91.6,0.01))
    assert(testEqualWithAccuracy(printAreaHeight,142.4,0.01))
    assert(testEqualWithAccuracy(printFormat.ratio(),4.0/6.0,0.01))
    assert(testEqualWithAccuracy(printFormat.printableRatio(),91.6/142.4,0.01))
    print "TESTS ON PRINTER FORMAT PASSED SUCCESSFULLY"

    #Compute PPI
    photo = Photo(612,612)
    photo.computePpmm(printFormat)
    assert(testEqualWithAccuracy(photo.ppmm,6.68122270742,0.01))
    assert(testEqualWithAccuracy(photo.ppi,169.0,0.01))
    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,91.6,0.01))
    assert(testEqualWithAccuracy(height,91.6,0.01))

    photo = Photo(1080,1007)
    photo.computePpmm(printFormat)
    assert(testEqualWithAccuracy(photo.ppmm,11.7903930131,0.01))
    assert(testEqualWithAccuracy(photo.ppi,299.0,0.01))
    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,91.6,0.01))
    assert(testEqualWithAccuracy(height,85.41,0.01))
    print "TESTS ON PPI COMPUTATION PASSED SUCCESSFULLY"

#print command : lpr -P Canon_CP900 -o media="Postcard(4x6in)" [filepath]
#print center
def printCommand(filename):
    cmd = "lpr -P Canon_CP900 -o media=\"Postcard(4x6in)\" " + filename
    print "Command : %s" %cmd
    res = popen2.popen4(cmd)

def main():

    #Make the tests
    unitTesting()

    #The root directory
    inputDir = "/Users/manu/Desktop/wistiti/"
    subDirArray = getImmediateSubdirectories(inputDir)

    #User choose the subdirectory
    userIndexSelection = userSelectionInArray(subDirArray)
    inputDir = os.path.join(inputDir,subDirArray[userIndexSelection])
    #Get the images list (jpg)
    files = listScreenShotFiles(inputDir)

    #Display information for user
    print "********************************"
    print files
    print "%s files found" %(len(files))
    #Create a post card print format (Selphy 900: 4x6 inches)
    printFormat = PrintFormat(4,6,"in")
    #Add a margin (top=bottom=left=right=5mm)
    printFormat.setMargin(10,10,"mm")
    print "********************************"

    userInput = ""
    index = 0
    while(userInput != "q"):
        #Open the picture image
        filepath = os.path.join(inputDir,files[index])
        (filepathWithoutExtension,extension) = os.path.splitext(filepath)
        fileOutput = filepathWithoutExtension + "-python" + extension
        #print filepathWithoutExtension
        #print extension
        #print fileOutput


        im = Image.open(filepath)
        photo = Photo(im.size[0],im.size[1])
        photo.computePpmm(printFormat)
        print "********************************"
        print "File %s on %s : %s" %(index+1,len(files),files[index])
        print "[resX/resY/Width/Height/PPI] : [%s/%s/%smm/%smm/%s]" %(photo.resX,photo.resY,photo.width, photo.height,photo.ppi)

        #User choose the action
        userInput = raw_input("Print? print/next/display/quit [p/n/d/q]")
        #print "Resultat %s" % userInput
        if userInput == "p":
            im.save(fileOutput, dpi = (photo.ppi,photo.ppi))
            printCommand(fileOutput)
            print "WARNING : YOU CAN PRINT THE SAME IMAGE"
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

