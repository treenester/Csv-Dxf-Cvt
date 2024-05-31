#!/usr/bin/python

import csv
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
from ezdxf.gfxattribs import GfxAttribs

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

# Create a new DXF document.
doc = ezdxf.new(dxfversion="R2010")

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.add("PT", color=colors.RED)
doc.layers.add("PN", color=colors.CYAN)
doc.layers.add("EL", color=colors.GREEN)
doc.layers.add("DE", color=colors.MAGENTA)

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace, 
# paperspace layout or block definition).  
msp = doc.modelspace()

# Add entities to a layout by factory methods: layout.add_...() 

# open csv file and process contents
with open(args.input) as file_obj:
    reader = csv.reader(file_obj)
#df = pandas.read_csv(open(args.input))
    for pnum, north, east, elev, desc in reader:
        print ("Processing point: " + pnum)
        
        msp.add_point((float(east),float(north),float(elev)), dxfattribs=GfxAttribs(layer="PT"))

        msp.add_text(pnum, dxfattribs=GfxAttribs(layer="PN")
        ).set_placement((float(east), float(north)), align=TextEntityAlignment.BOTTOM_LEFT)

        msp.add_text(str(elev), dxfattribs=GfxAttribs(layer="EL")
        ).set_placement((float(east), float(north), float(elev)), align=TextEntityAlignment.BOTTOM_RIGHT)

        msp.add_text(desc, dxfattribs=GfxAttribs(layer="DE")
        ).set_placement((float(east), float(north)), align=TextEntityAlignment.TOP_LEFT)

doc.saveas(args.output)
print ("Done\n")
