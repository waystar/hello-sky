#!/usr/bin/env python

# panoramaOffset.py: Gimp plugin-in to offset image layer along x axis only. 
#                   Useful when creating or modifying panorama strips to 
#                       check seamline and modify in necessary. 
#                   Same as Layer->Transform->Offset, selecting "x/2, y/2"
#                       and then returning the y value to zero. 

# Place the python script in the folder where Gimp expects to find plug-ins.
#   This could be under <user folder>/.gimp-2.x/plug-ins, or it could be under 
#   whatever folder structure your operating system put Gimp into.

# Tested and used with Gimp 2.8 on Windows 7, Linux Mint 18.1, and Windows 10

# Anyone may use and distribute this plug-in, I'm not responsible for any
#   misuse of this file. Nor am I responsible for space alien attacks,
#   giant meteor collisions, or anyone forgetting to save their files 
#   before using scripts or plug-ins.


from gimpfu import *

def panoramaOffset(img, layer):

	width = layer.width 	

	offset_x = int(width/2)

	pdb.gimp_drawable_offset(layer, True, 1, offset_x, 0)

	return


register(
	"python_fu_panoramaOffset",
	"Panorama Offset",
	"Offsets layer along x-axis with wraparound for purpose of cleaning seamless edges.",
	"Waylena McCully",
	"Waylena McCully",
	"2017",
	"<Image>/Layer/Panorama Offset",
	"*",
	[

	],
	[],
	panoramaOffset)

main()	
