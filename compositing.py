#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PIL import Image
from classes.photo import Photo

#"toto.jpg" + "-suffix" -> "toto-suffix.jpg"
def generateFilepathWithSuffix(filepath,suffix):
    (filepathWithoutExtension,extension) = os.path.splitext(filepath)
    return filepathWithoutExtension + suffix + extension

#Add a margin and save the file (margin is for left,right,bottom and top)
def addMarginOnTemplate(templatePath,margin):
    template = Image.open(templatePath)
    photoSize = template.size
    print photoSize
    marginPhotoSize= (photoSize[0] + margin * 2, photoSize[1] + margin * 2)
    print marginPhotoSize
    marginPhoto = Image.new(mode="RGB", size=marginPhotoSize, color= (84,158,167))
    marginPhoto.paste(template,(margin,margin))
    fileOutput = generateFilepathWithSuffix(templatePath,"-margin")
    marginPhoto.save(fileOutput, 'jpeg')
    return fileOutput

#Add a photo on the template
#Resize the photo if necessary, or resize the template if necessary
def addPhotoOnTemplate(photoPath,templatePath,margin):
    template = Image.open(templatePath)
    image = Image.open(photoPath)

    photo = Photo(image.size[0],image.size[1])
    (resizePhoto,resizeTemplate) = photo.addTemplate(template.size[0],template.size[1],margin)
    image = image.resize(resizePhoto,Image.ANTIALIAS)
    template = template.resize(resizeTemplate,Image.ANTIALIAS)

    template.paste(image, (margin,margin))
    fileOutput = generateFilepathWithSuffix(photoPath,"-template")
    template.save(fileOutput, 'jpeg')
    return fileOutput


