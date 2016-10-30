#!/usr/bin/python
# -*- coding: utf-8 -*-



from classes.printer import Printer


def main():
    print "Available printer registered in the OS : "
    printernames = Printer.osPrinter()
    for idx, printername in enumerate(printernames):
        print "[%s -> %s]" %(idx,printername)


if __name__ == "__main__":
    main()

