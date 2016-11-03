#!/usr/bin/python
# -*- coding: utf-8 -*-
import cups
import subprocess

##
# @file printer.py
# Printer
# https://www.cups.org/doc/options.html?VERSION=1.7&Q=




##OS printers operations
#
#
class Printer(object):

    ##@var printers
    #The printers data dictionary from cups

    ##Constructor
    def __init__(self):
        con = cups.Connection()
        self.printers = con.getPrinters()
        print self.printers

    ##Get the raw input dictionnary
    #@return : Dictionary
    @staticmethod
    def getPrinterDict():
        con = cups.Connection()
        return con.getPrinters()

    ##Is the printer registered in the OS?
    #@return : BOOL
    @staticmethod
    def exists(printername):
        printers = Printer.getPrinterDict()
        exists = False
        for key,value in printers.iteritems():
            if(key == printername):
                exists = True
        return exists

    ##Get an information about a specific OS printer
    #@return : String
    @staticmethod
    def information(printername,inputKey):
        printers = Printer.getPrinterDict()
        exists = False
        for key,value in printers.iteritems():
            if(key == printername):
                for keyInfo,valueInfo in value.iteritems():
                    if(keyInfo == inputKey):
                        return valueInfo
        return None

    ##List of the printers available in the Operating System
    #@return : [String]
    @staticmethod
    def osPrinter():
        printers = Printer.getPrinterDict()
        printernames = []
        for key,value in printers.iteritems():
            printernames += [key]
        return printernames

    ##Detect if the printer is online/offline
    #@return : BOOL
    @staticmethod
    def printerOnline(printername):
        info = Printer.information(printername,"printer-state-reasons")
        #[u'none'] or [u'offline-report']
        if(info[0] == 'none'):
            print printername + " online"
            return True
        elif(info[0] == 'offline-report'):
            print printername + " offline"
            return False
        else :
            print printername + " unknown state"

    ##Compute printer command
    #lpr -P Canon_CP900 -o media="Postcard(4x6in)" [filepath]
    #@return : [String]
    @staticmethod
    def computePrinterCommand(filepath,
                              printername="Canon_CP900",
                              printerFormat="media=\"Postcard(4x6in)\""):

        return ["lpr","-P",printername,"-o","media="+printerFormat,filepath]
    #return ["lpr","-P",printername,"-o","orientation-requested=3","-o","media="+printerFormat,filepath]


    ##Send printer job
    #printer command :[lpr,-P,Canon_CP900,-o,media="Postcard(4x6in)",[filepath]]
    #@return : Void
    @staticmethod
    def sendPrinterJob(printerCommand):
        try :
            print ("Send job %s" %printerCommand)
            process = subprocess.check_output(printerCommand)
            print "Command OK"
        except subprocess.CalledProcessError, e :
            print "Command FAILED"
            #print e


