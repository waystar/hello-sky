# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# Anyone may use and distribute this script, I'm not responsible for any
#   misuse of this file. Nor am I responsible for space alien attacks,
#   giant meteor collisions, or anyone forgetting to save their files 
#   before using scripts or plug-ins.


"""
VERY experimental !!!!!

Run from within script editor

Not yet setup for use as addon

Also... written out of need before I actually learned Python

"""

#script BEGIN
"""
bl_info = {
    "name": "Marker List Export",
    "author": "Waylena McCully",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "VideoSequenceEditor > Marker",
    "description": "Exports markers, labels, times and frames to CSV text file.",
    "warning": "Very experimental, used personally, not tested elsewhere",
    "wiki_url": "",
    "category": "",
    }
"""

import bpy
from operator import itemgetter
import csv
import os

#want to create a listy thing sorted by frame and calculate time and write it all to file

marker_list = []
scene = bpy.context.scene


# calculate seconds from frames  -stolen from someone online I don't remember
fps = scene.render.fps
fps_base = scene.render.fps_base

def frame_to_time(frame_number):
    raw_time = (frame_number - 1) / fps
    return round(raw_time, 3)


# converter - from user Lee on stackoverflow https://stackoverflow.com/users/2527629/lee

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)



###---  Make "list"

for marker in scene.timeline_markers:

    frame_time_sec = frame_to_time(marker.frame)
    frame_time_minsec = sec2time(frame_time_sec, 2)

    marker_list.append((marker.frame, frame_time_minsec, frame_time_sec, marker.name))


###--- Sort
marker_list_sort = sorted(marker_list, key=itemgetter(0))


# get basename from blend file, strip off extension
foo = bpy.path.basename(bpy.context.blend_data.filepath)
fooNew = foo.replace(" ", "").rstrip(foo[-6:]).upper()


###--- txt instead of csv to force Excel to import properly
filepath = bpy.data.filepath
folder = os.path.dirname(filepath)

# this needs updated to use str.format() syntax to be more robust
with open ("%s/%s.txt" %(folder, fooNew), "w") as out:
    writer = csv.writer(out, delimiter=';', lineterminator='\n')
    writer.writerows(marker_list_sort)
