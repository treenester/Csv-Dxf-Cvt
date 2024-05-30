#!/usr/bin/python

import csv
import dxfwrite

import argparse
#import pandas

__author__ = 'dlb'
__version__ = '2.0'
 
parser = argparse.ArgumentParser(description='Csv to Dxf Conversion')
parser.add_argument('-i','--input', help='infile',required=True)
parser.add_argument('-o','--output',help='outfile', required=True)
args = parser.parse_args()
 
## show values ##
print ("Input file: %s" % args.input )
print ("Output file: %s" % args.output )

## process files ##

# create/overwrite output file
# and start entities section
from dxfwrite import DXFEngine as dxf
drawing = dxf.drawing(args.output)
drawing.add_layer('PT')
drawing.add_layer('PN', color=2)
drawing.add_layer('EL', color=3)
drawing.add_layer('DE', color=4)
drawing.save()

# open csv file and process contents
with open(args.input) as file_obj:
    reader = csv.reader(file_obj)
#df = pandas.read_csv(open(args.input))
    for pnum, north, east, elev, desc in reader:
        print ("Processing point: " + pnum)
        
        pt = dxf.point((east, north, elev))
        pt['layer'] = 'PT'
        drawing.add(pt)

        pn = dxf.text(pnum, (east, north), valign=dxfwrite.BOTTOM, alignpoint=(east, north))
        pn['layer'] = 'PN'
        drawing.add(pn)

        el = dxf.text(str(elev), (east, north), halign=dxfwrite.RIGHT, valign=dxfwrite.BOTTOM, alignpoint=(east, north))
        el['layer'] = 'EL'
        drawing.add(el)

        de = dxf.text(desc, (east, north), valign=dxfwrite.TOP, alignpoint=(east, north))
        de['layer'] = 'DE'
        drawing.add(de)

drawing.save()
print ("Done\n")
