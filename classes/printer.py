#!/usr/bin/python
# -*- coding: utf-8 -*-
import cups

#OS printers operations
class Printer(object):
    def __init__(self):
        con = cups.Connection()
        self.printers = con.getPrinters()
        print self.printers

    #Get the raw input dictionnary
    #return : Dictionary
    @staticmethod
    def getPrinterDict():
        con = cups.Connection()
        return con.getPrinters()

    #Is the printer registered in the OS?
    #return : BOOL
    @staticmethod
    def exists(printername):
        printers = Printer.getPrinterDict()
        exists = False
        for key,value in printers.iteritems():
            if(key == printername):
                exists = True
        return exists

    #Get an information about a specific OS printer
    #return : String
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

    #List of the printers available in the Operating System
    #return : [String]
    @staticmethod
    def osPrinter():
        printers = Printer.getPrinterDict()
        printernames = []
        for key,value in printers.iteritems():
            printernames += [key]
        return printernames

    #Detect if the printer is online/offline
    #return : BOOL
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
