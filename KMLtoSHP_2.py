#-------------------------------------------------------------------------------
# Name:        Batch convert KML to SHP
# Purpose:
#
# Author:      cyndi.ignacio
#
# Created:     04/12/2015
# Copyright:   (c) cyndi.ignacio 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import modules
import os, arcpy, arcpy.da
from os import path
from arcpy import env

#set parameters
inWorkspace = r"" # input workspace
env.workspace = inWorkspace
arcpy.env.overwriteOutput = True
arcpy.CreateFolder_management(inWorkspace, 'ORPS')
outLocation = path.join(inWorkspace, 'ORPS')
masterGDB = 'Test.gdb'
masterGDBLocation = path.join(inWorkspace, masterGDB)

arcpy.CreateFileGDB_management(inWorkspace, masterGDB)

for kmz in arcpy.ListFiles('*.kml'):
    try:
        kmz_new = 'Kal_' + path.splitext(path.basename(kmz))[0]
        print "CONVERTING: " + os.path.join(arcpy.env.workspace,kmz)
        arcpy.KMLToLayer_conversion(kmz, outLocation, kmz_new)
    except arcpy.ExecuteError:
        print "Something went wrong" + str(kmz) + ". Here's a traceback:"
        continue

env.workspace = outLocation
wks = arcpy.ListWorkspaces('*', 'FileGDB')
for fgdb in wks:
    fgdb_name = path.splitext(path.basename(fgdb))[0]
    env.workspace = fgdb
    featureClasses = arcpy.ListFeatureClasses('*', 'Polyline', 'Placemarks')
    for fc in featureClasses:
       arcpy.AddField_management(fc, 'NameID', 'TEXT')
       cursor = arcpy.UpdateCursor(fc)
       for row in cursor:
           row.setValue('NameID', fgdb_name)
           cursor.updateRow(row)
        print "COPYING: " + fc + " FROM: " + fgdb
        fcCopy = fgdb + os.sep + 'Placemarks' + os.sep + fc
        arcpy.FeatureClassToFeatureClass_conversion(fcCopy, masterGDBLocation, fgdb[fgdb.rfind(os.sep)+1:-4])


del kmz, wks, featureClasses, fgdb #row, cursor

print 'finished'


