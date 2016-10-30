#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from classes.printer import Printer
from classes.photo import Photo
from classes.printFormat import PrintFormat
from classes.configuration import Configuration
from conversion import *
from printer import *
from compositing import *

def testEqualWithAccuracy(float1,float2,precision):
    if ( math.fabs(float1 - float2) < precision):
        return True
    else:
        print "%s is not equal to %s" %(float1,float2)
        return False

def testFileWithSelphyCP900(filepath,dpiX,dpiY):
    printFormat = PrintFormat.SelphyCP900()
    printFormat.setPrinterMargin(10,10,"mm")

    im = Image.open(filepath)
    photo = Photo(im.size[0],im.size[1])
    photo.computePpmm(printFormat)

    fileOutput = generateFilepathWithSuffix(filepath,"-CP900-print")
    im.save(fileOutput, 'jpeg', dpi = (photo.ppiX,photo.ppiY))
    print fileOutput
    imTest = Image.open(fileOutput)
    (imageDpiX,imageDpiY) = imTest.info['dpi']
    assert(imageDpiX == dpiX)
    assert(imageDpiY == dpiY)

def testFileWithSelphyCP900Template(filepath,dpiX,dpiY):
    printFormat = PrintFormat.SelphyCP900(dpiStretch=True)
    printFormat.setPrinterMargin(-1,-1,"mm")

    im = Image.open(filepath)
    photo = Photo(im.size[0],im.size[1])
    photo.computePpmm(printFormat)

    fileOutput = generateFilepathWithSuffix(filepath,"-CP900-print")
    im.save(fileOutput, 'jpeg', dpi = (photo.ppiX,photo.ppiY))
    print fileOutput
    imTest = Image.open(fileOutput)
    (imageDpiX,imageDpiY) = imTest.info['dpi']
    assert(imageDpiX == dpiX)
    assert(imageDpiY == dpiY)


def testSelphyCP900():
    print "\n****TEST SELPHY CP900 Instagram file****"
    testFileWithSelphyCP900("./resources/test/finhalmn/1313840674994551403.jpg",172,172)
    testFileWithSelphyCP900("./resources/test/bentalou/1139147525899845285.jpg",304,304)
    testFileWithSelphyCP900("./resources/test/bentalou/1194941102189608484.jpg",304,304)
    testFileWithSelphyCP900("./resources/test/bentalou/1326184207731289979.jpg",211,211)
    testFileWithSelphyCP900("./resources/test/bentalou/712495213394164801.jpg",180,180)
    print "TESTS ON SELPHY CP900 INSTAGRAM FILES PASSED SUCCESSFULLY"

def testSelphyCP900Template():
    print "\n****TEST SELPHY CP900 Template****"
    testFileWithSelphyCP900Template("./resources/test/template/COR-MARS16_elements-template-gimp.jpg",297,301)
    print "TESTS ON SELPHY CP900 TEMPLATE PASSED SUCCESSFULLY"

def testAddTemplate():
    print "\n****TEST ADDING TEMPLATE****"
    photopath = "./resources/test/bentalou/712495213394164801.jpg"
    templatePathOrigin = "./resources/test/template/COR-MARS16_elements-template-gimp.jpg"
    templatePath = templatePathOrigin
    printMargin = 30
    templateMargin = 60
    marginColor = (84,158,167)

    #Add a margin on the template (add new pixel for printer margin)
    templatePath = addMarginOnTemplate(templatePath,printMargin,marginColor=marginColor)

    #Add a photo on the template
    photoPath = addPhotoOnTemplate(photopath,templatePath,margin=templateMargin)

    #Create photo settings
    photoWithTemplate = Image.open(photoPath)
    print photoWithTemplate.size[0]
    photoSettings = Photo(photoWithTemplate.size[0],photoWithTemplate.size[1])
    print photoSettings

    #Create printer
    printer = PrintFormat.SelphyCP900(dpiStretch=True)

    #Adapt dpi
    photoSettings.computePpmm(printer)

    #Save file
    fileOutput = generateFilepathWithSuffix(photoPath,"-CP900-print")
    photoWithTemplate.save(fileOutput, 'jpeg', dpi=(photoSettings.ppiX,photoSettings.ppiY))
    print photoSettings
    
    #TEST
    testTemplateOrigin = Image.open(templatePathOrigin)
    testTemplateMargin = Image.open(templatePath)
    sizeOrigin = testTemplateOrigin.size
    sizeTemplateMargin = testTemplateMargin.size
    sizePhotoWithTemplate = photoWithTemplate.size
    print sizeOrigin
    assert( sizeOrigin[0] == 1181)
    assert( sizeOrigin[1] == 1771)
    assert( sizeTemplateMargin[0] == 1241)
    assert( sizeTemplateMargin[1] == 1831)
    assert( sizePhotoWithTemplate[0] == 1241)
    assert( sizePhotoWithTemplate[1] == 1831)

    imTest = Image.open(fileOutput)
    (imageDpiX,imageDpiY) = imTest.info['dpi']
    assert(imageDpiX == 315)
    assert(imageDpiY == 314)

    print"TESTS ON MARGIN + TEMPLATE + PHOTO  PASSED SUCCESSFULLY"

def unitTesting():

    print "\n****UNIT TESTS****"
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
    #assert(testEqualWithAccuracy(ppi2ppmm(169.0,ppmm(612,91.6)),0.01))


    print "TESTS ON DIMENSION CONVERSION PASSED SUCCESSFULLY"

    #Print format
    printFormat = PrintFormat(4,6)
    assert(not testEqualWithAccuracy(printFormat.width,101.6,0.01))
    assert(not testEqualWithAccuracy(printFormat.height,152.4,0.01))
    printFormat = PrintFormat(4,6,"in")
    assert(testEqualWithAccuracy(printFormat.width,101.6,0.01))
    assert(testEqualWithAccuracy(printFormat.height,152.4,0.01))
    printFormat.setPrinterMargin(10,10,"mm")
    (printAreaWidth,printAreaHeight) = printFormat.getPrintableArea()
    assert(testEqualWithAccuracy(printAreaWidth,91.6,0.01))
    assert(testEqualWithAccuracy(printAreaHeight,142.4,0.01))
    assert(testEqualWithAccuracy(printFormat.ratio(),4.0/6.0,0.01))
    assert(testEqualWithAccuracy(printFormat.printableRatio(),91.6/142.4,0.01))

    printFormatSelphy = PrintFormat.SelphyCP900()
    printFormatSelphy.setPrinterMargin(0,0,"mm")
    (printAreaWidth,printAreaHeight) = printFormatSelphy.getPrintableArea()
    assert(testEqualWithAccuracy(printAreaWidth,100,0.01))
    assert(testEqualWithAccuracy(printAreaHeight,148,0.01))

    print "TESTS ON PRINTER FORMAT PASSED SUCCESSFULLY"

    #Compute PPI
    printFormat = PrintFormat(4,6,"in")
    printFormat.setDpiStretch(False)
    printFormat.setPrinterMargin(10,10,"mm")

    photo = Photo(612,612)
    photo.computePpmm(printFormat)
    assert(testEqualWithAccuracy(photo.ppmm,6.68122270742,0.01))
    assert(testEqualWithAccuracy(photo.ppi,169.0,0.01))
    assert(testEqualWithAccuracy(photo.ppiX,169.0,0.01))
    assert(testEqualWithAccuracy(photo.ppiY,169.0,0.01))

    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,91.6,0.01))
    assert(testEqualWithAccuracy(height,91.6,0.01))

    photo = Photo(1080,1080)
    photo.computePpmm(printFormat)
    assert(testEqualWithAccuracy(photo.ppmm,11.79,0.01))
    assert(testEqualWithAccuracy(photo.ppi,299.0,0.01))
    assert(testEqualWithAccuracy(photo.ppiX,299.0,0.01))
    assert(testEqualWithAccuracy(photo.ppiY,299.0,0.01))

    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,91.6,0.01))
    assert(testEqualWithAccuracy(height,91.6,0.01))

    #Test Clutcho file as full print
    photo = Photo(1181,1771)
    printFormatSelphy.setDpiStretch(True)
    print printFormatSelphy.dpiStretch
    photo.computePpmm(printFormatSelphy)
    assert(testEqualWithAccuracy(photo.ppmmX,11.81,0.01))
    assert(testEqualWithAccuracy(photo.ppmmY,11.966,0.01))
    assert(testEqualWithAccuracy(photo.ppiX,299,0.01))
    assert(testEqualWithAccuracy(photo.ppiY,303,0.01))

    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,100.0,0.01))
    assert(testEqualWithAccuracy(height,148,0.01))

    print "TESTS ON PPI COMPUTATION PASSED SUCCESSFULLY"

def testPrinter():
    Printer()
    assert(Printer.exists("Canon_CP900"))
    print Printer.osPrinter()
    #assert(Printer.printerOnline("Canon_CP900"))

def testConfiguration():
    print "\n****TEST CONFIGURATION****"
    rootDirectory = "./resources/test/configurations"
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
    print configuration
    print "TESTS ON CONFIGURATION PASSED SUCCESSFULLY"


def main():
    print "\n"
    unitTesting()
    testSelphyCP900()
    testSelphyCP900Template()
    testAddTemplate()
    testPrinter()
    testConfiguration()
    print "\n\n***TESTS PASSED SUCCESSFULLY***\n"
    return
if __name__ == "__main__":
    main()
