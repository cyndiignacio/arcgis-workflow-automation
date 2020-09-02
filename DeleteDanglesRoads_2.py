#-------------------------------------------------------------------------------
# Name:        Delete road dangles
# Purpose:
#
# Author:      cyndi.ignacio
#
# Created:     16/06/2016
# Copyright:   (c) cyndi.ignacio 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#import modules
import arcpy
from os import path
from arcpy import env

#workspace
inWorkspace = r'C:\Users\cyndi.ignacio\Documents\WB\43 - Woodfields\Topology'
env.workspace = inWorkspace
arcpy.env.overwriteOutput = True

inFc = 'WF_Pilot_Roads.shp'

# Step 1: Delete Identical Roads
arcpy.DeleteIdentical_management(inFc, "Shape")

# Step 2: Feature vertices to points
outPt = 'Step2_pt.shp'
arcpy.FeatureVerticesToPoints_management(inFc, outPt, "DANGLE")

# Step 3: Select layer by location
lyr = 'WF_Roads2'
arcpy.MakeFeatureLayer_management(inFc, lyr)
arcpy.SelectLayerByLocation_management(lyr, "intersect", outPt)

# Step 4: Trim and Extend Line
arcpy.TrimLine_edit(lyr, "10 Meters", "KEEP_SHORT")
arcpy.ExtendLine_edit(lyr, "10 Meters", "EXTENSION")

# Step 5: Repeat step 2 on updated dataset
outPt2 = 'Step5_pt.shp'
arcpy.FeatureVerticesToPoints_management(lyr, outPt2, "DANGLE")

del inFc, lyr, outPt, outPt2

print 'finished'

