#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from classes.photo import Photo
from classes.printFormat import PrintFormat
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

    (filepathWithoutExtension,extension) = os.path.splitext(filepath)
    fileOutput = filepathWithoutExtension + "-CP900-print" + extension
    im.save(fileOutput, 'jpeg', dpi = (photo.ppiX,photo.ppiY))
    print fileOutput
    imTest = Image.open(fileOutput)
    (imageDpiX,imageDpiY) = imTest.info['dpi']
    assert(imageDpiX == dpiX)
    assert(imageDpiY == dpiY)

def testFileWithSelphyCP900Template(filepath,dpiX,dpiY):
    printFormat = PrintFormat.SelphyCP900(fullprint=True)
    printFormat.setPrinterMargin(-1,-1,"mm")

    im = Image.open(filepath)
    photo = Photo(im.size[0],im.size[1])
    photo.computePpmm(printFormat)

    (filepathWithoutExtension,extension) = os.path.splitext(filepath)
    fileOutput = filepathWithoutExtension + "-CP900-print" + extension
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

    #Add a margin on the template (add new pixel for printer margin)
    templatePath = addMarginOnTemplate(templatePath,printMargin)

    #Add a photo on the template
    photoPath = addPhotoOnTemplate(photopath,templatePath,margin=templateMargin)

    #Create photo settings
    photoWithTemplate = Image.open(photoPath)
    print photoWithTemplate.size[0]
    photoSettings = Photo(photoWithTemplate.size[0],photoWithTemplate.size[1])
    print photoSettings

    #Create printer
    printer = PrintFormat.SelphyCP900(fullprint=True)

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
    assert( sizeOrigin[0], 1121)
    assert( sizeOrigin[1], 1771)
    assert( sizeTemplateMargin[0], 1241)
    assert( sizeTemplateMargin[1], 1831)
    assert( sizePhotoWithTemplate[0], 1241)
    assert( sizePhotoWithTemplate[1], 1831)

    imTest = Image.open(fileOutput)
    (imageDpiX,imageDpiY) = imTest.info['dpi']
    assert(imageDpiX == 315)
    assert(imageDpiY == 314)








#    filepath = "./resources/test/bentalou/712495213394164801.jpg"
#    template = Image.open("./resources/test/template/COR-MARS16_elements-template-gimp.jpg")
#    image = Image.open(filepath)
#
#    #Computation
#    margin = 30
#    photo = Photo(image.size[0],image.size[1])
#    (resizePhoto,resizeTemplate) = photo.addTemplate(template.size[0],template.size[1],margin)
#    image = image.resize(resizePhoto,Image.ANTIALIAS)
#    template = template.resize(resizeTemplate,Image.ANTIALIAS)
#
#    template.paste(image, (margin,margin))
#
#
#    #TO PRINTER
#    printFormat = PrintFormat.SelphyCP900()
#    printFormat.setPrinterMargin(-1,-1,"mm")
#
#
#    finalPhoto = Photo(template.size[0],template.size[1])
#    finalPhoto.setFullPrint(True)
#    finalPhoto.computePpmm(printFormat)
#    print "[resX/resY/Width/Height/PPIX,PPIY] : [%s/%s/%smm/%smm/%s/%s]" %(finalPhoto.resX,finalPhoto.resY,finalPhoto.width, finalPhoto.height,finalPhoto.ppiX,finalPhoto.ppiY)
#
#
#
#    (filepathWithoutExtension,extension) = os.path.splitext(filepath)
#    fileOutput = filepathWithoutExtension + "-CP900-template-print" + extension
#    print (finalPhoto.ppiX,finalPhoto.ppiY)
#    template.save(fileOutput, 'jpeg', dpi = (finalPhoto.ppiX,finalPhoto.ppiY))
#    print fileOutput
#    imTest = Image.open(fileOutput)
#    (imageDpiX,imageDpiY) = imTest.info['dpi']
#    printCommand(fileOutput)



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
    printFormat.setFullPrint(False)
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
    printFormatSelphy.setFullPrint(True)
    print printFormatSelphy.fullPrint
    photo.computePpmm(printFormatSelphy)
    assert(testEqualWithAccuracy(photo.ppmmX,11.81,0.01))
    assert(testEqualWithAccuracy(photo.ppmmY,11.966,0.01))
    assert(testEqualWithAccuracy(photo.ppiX,299,0.01))
    assert(testEqualWithAccuracy(photo.ppiY,303,0.01))

    (width,height) = photo.getSize()
    assert(testEqualWithAccuracy(width,100.0,0.01))
    assert(testEqualWithAccuracy(height,148,0.01))

    print "TESTS ON PPI COMPUTATION PASSED SUCCESSFULLY"

def main():
    print "\n"
    unitTesting()
    testSelphyCP900()
    testSelphyCP900Template()
    testAddTemplate()
    print "\n"
    return
if __name__ == "__main__":
    main()
