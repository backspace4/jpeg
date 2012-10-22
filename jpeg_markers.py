#!/usr/bin/env python
# -*- python -*-

__description__ = 'dump markers in jpeg image file'
__author__ = 'backspace____'
__version__ = '0.0.1'
__date__ = '2012/10/23'

"""
a script to dump markers in jpeg image file

no Copyright
Use at your own risk

History:
  2012/11/23: start

Todo:

"""

import sys
import io


markers = {0xffd8:'SOI',
           0xffdb:'DQT',
           0xffc4:'DHT',
           0xffc0:'SOF0',
           0xffc1:'SOF1',
           0xffdd:'DRI',
           0xffda:'SOS',
           0xffd9:'EOI',
           0xffe0:'APP0',
           0xffe1:'APP1',
           0xffe2:'APP2',
           0xffe3:'APP3',
           0xffe4:'APP4',
           0xffe5:'APP5',
           0xffe6:'APP6',
           0xffe7:'APP7',
           0xffe8:'APP8',
           0xffe9:'APP9',
           0xffea:'APPA',
           0xffeb:'APPB',
           0xffec:'APPC',
           0xffed:'APPD'}

class Tokenizer:

    def __init__(self, file):
        #print "file %(file)s" % locals()
        self.file = file
        self.mk = []
        self.io = io.open(self.file, 'rb')
        self.mk.append(ord(self.io.read(1)))
        self.mk.append(ord(self.io.read(1)))

    def next(self):
        if self.io.closed:
            return False

        self.mk[0] = self.mk[-1]
        byte  = self.io.read(1)
        if not byte:
            self.io.close()
            return False
        else:
            self.mk[1] = ord(byte)

        return True

    def marker(self):
        key = self.mk[0] * (16 ** 2) + self.mk[1]
        if markers.has_key(key):
            return markers[key]
        return False

    def is_marker(self):
        key = self.mk[0] * (16 ** 2) + self.mk[1]
        if markers.has_key(key):
            return True
        return False

    def length(self):
        if self.io.closed:
            return False
        self.len = self.io.peek(2)
        return ord(self.len[0]) * (16 ** 2) + ord(self.len[1])

    def pos(self):
        if self.io.closed:
            return False
        return self.io.tell() -1

def Main():

    tk = Tokenizer(sys.argv[1])

    print "%4s:   %08s %8s" %("MARK", "pos", "size")
    print "-------------------------"

    eof = False
    while not eof:

        if tk.is_marker():
            marker = tk.marker()
        else:
            eof = not tk.next()
            continue

        if (marker == "SOI" or
            marker == "EOI" or
            marker == "SOS"):
            length = 0
        else:
            length = tk.length()

        pos = tk.pos()

        print "%(marker)4s: 0x%(pos)08x %(length)8d" % locals()
        eof = not tk.next()


if __name__ == '__main__':
    Main()

