#!/usr/bin/python
# -*- coding: utf-8 -*-
import cups

class Printer(object):
    def __init__(self):
        con = cups.Connection()
        self.printers = con.getPrinters()
        print self.printers

    @staticmethod
    def getPrinterDict():
        con = cups.Connection()
        return con.getPrinters()

    @staticmethod
    def exists(printername):
        printers = Printer.getPrinterDict()
        exists = False
        for key,value in printers.iteritems():
            if(key == printername):
                exists = True
        return exists

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
