#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2019, David Yaffe
# GPLv3 Licensed

import re
import csv
import sys
import argparse

class Services2CSV:
    """ Docstring """

    pattern = (
        r"^(?P<service>[A-Za-z0-9-_.+*\/\\\(\)]+)(\s+?)(?P<port>\d{1,5})\/(?P<protocol>\w{3,4})"
        r"((\s+)(?P<alias>[A-Za-z0-9-_.+*\/\\\(\)]+))?((\s+)#\s(?P<description>.*))?$"
    )
    regex = re.compile(pattern)

    def __init__(self):
        """ Docstring """
        self.servicelist = []

    def readServices(self):
        """ Docstring """

        with open("/etc/services") as infile:
            for line in infile:
                if not line in ['\n', '\r\n'] or line[0] == "#":
                    result = re.match(self.pattern, line)
                if result:
                    serviceRow = result.groupdict()
                    if serviceRow['alias']:
                        serviceRow['alias'] = serviceRow['alias'].strip()
                    if serviceRow['description']:
                        serviceRow['description'] = serviceRow['description'].strip()
                    self.servicelist.append(serviceRow)

    def writeServices(self):
        """ Docstring """

        fieldnames = ['service', 'port', 'protocol', 'alias', 'description']
        with open('services.csv', 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for line in self.servicelist:
                writer.writerow(line)

def main():
    """ DocString """

    desc = 'python script to convert /etc/services to either CSV or JSON'
    parser = argparse.ArgumentParser(description=desc)
#    args = parser.parse_args()
    ser = Services2CSV()
    ser.readServices()
    ser.writeServices()

if __name__ == '__main__':
    sys.exit(main())
