#-------------------------------------------------------------------------------
# Name:        RIA Analysis: Kilometer band approach
# Purpose:
#
# Author:      cyndi.ignacio
#
# Created:     15/12/2015
# Copyright:   (c) cyndi.ignacio 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import modules
import os, arcpy, arcpy.da
from os import path
from arcpy import env

#set parameters
inWorkspace = r'C:\Users\cyndi.ignacio\Documents\WB\RIA\RIA Analysis\FMR\GAA_2014_Batch3.gdb'
env.workspace = inWorkspace
arcpy.env.overwriteOutput = True

#-----------------------------------------------------------------------------------------------------
#Get the ID of each TRIP road project and append it as name of output feature class
fc = 'GAA_2014_Mindanao_B2' #TRIP road projects
philBndy = 'Phil_country_boundary'
fc_fieldName = 'NameID'
distances = [1, 2.5, 5] #buffer distances
bufferUnit = 'kilometers'

#Create feature layer
arcpy.MakeFeatureLayer_management(fc, "Polyline_lyr")     # no need to make the layer each time through the cursor
with arcpy.da.SearchCursor(fc, fc_fieldName) as cursor:
    for row in cursor:
        var_PolylineName = row[0]
        print "Buffering road project " + var_PolylineName
        arcpy.SelectLayerByAttribute_management("Polyline_lyr", "NEW_SELECTION", '"{}" = \'{}\''.format(fc_fieldName, var_PolylineName))

        #STEP1: Execute multiple ring buffer analysis
        outBufName = 'GAA_Buffer\\' + 'Buf_'+ var_PolylineName
        finOutBufName = path.join(inWorkspace, outBufName)
        arcpy.MultipleRingBuffer_analysis("Polyline_lyr", finOutBufName, distances, bufferUnit,'', 'NONE')

        #STEP2: Intersect buffer layer with philippine boundary layer
        outIntName = 'GAA_Buf_Int\\' + 'BufInt_'+ var_PolylineName
        finOutIntName = path.join(inWorkspace, outIntName)
        arcpy.Intersect_analysis([finOutBufName, philBndy], finOutIntName, 'ALL', '', 'INPUT')

        #STEP3: Dissolve buffer layers to merge features into three features (1, 2.5 and 5km)
        outDisName = 'GAA_Buf_Dis\\' + 'BufDis_'+ var_PolylineName
        finOutDis = path.join(inWorkspace, outDisName)
        dissolveField = ['distance', 'NameID', 'Filename_1', 'ID_1'] #for GAA 2014 and 2015
        #dissolveField = ['distance', 'SubprojID', 'NameID'] #for PRDP 2015
        arcpy.Dissolve_management(finOutIntName, finOutDis, dissolveField, '', 'SINGLE_PART', '')

        #STEP4: Delete islands by performing near analysis (only features with 0 distance to rd (connected) will be retained)
        arcpy.Near_analysis(finOutDis, "Polyline_lyr")
        outDelLyr = 'Dis' + var_PolylineName
        arcpy.MakeFeatureLayer_management(finOutDis, outDelLyr)

        expression = '"NEAR_DIST" <> 0' #features that do not have 0 NEAR_DIST will be deleted
        arcpy.SelectLayerByAttribute_management(outDelLyr, 'NEW_SELECTION', expression)
        if int(arcpy.GetCount_management(outDelLyr).getOutput(0))>0:
            arcpy.DeleteFeatures_management(outDelLyr)



del fc, cursor, row, fc_fieldName, outBufName, outIntName, philBndy, outDisName, finOutDis, outDelLyr
print 'finished RIA Analysis (up to Step4)'
