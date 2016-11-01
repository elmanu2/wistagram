#!/usr/bin/python
# -*- coding: utf-8 -*-

from classes.printer import Printer

##
# @file printerlist.py
# Printer
#

## Display in the console, all the available printer\n
# on the current Operating System
def main():
    print "Available printer registered in the OS : "
    printernames = Printer.osPrinter()
    for idx, printername in enumerate(printernames):
        print "[%s -> %s]" %(idx,printername)


if __name__ == "__main__":
    main()

