#-------------------------------------------------------------------------------
# Name:        Travel Time
# Purpose:     To compute travel time to traverse a road
#
# Author:      cyndi.ignacio
#
# Created:     25/05/2016
# Copyright:   (c) cyndi.ignacio 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##---------------------------------------------------------------
#Import modules
import arcpy, numpy as np, scipy, arcpy.da
from arcpy.sa import *
from arcpy import env
from os import path
import re


##----------------------------------------------------------------
#Input road
road2= r'C:\Users\cyndi.ignacio\Documents\WB\35 - Travel Time\PortBarton.shp'

arcpy.CheckOutExtension("Spatial")

#Speed matrix
surface = [1,2,3,4]
good = [100, 80, 60, 0] #arbitrary values
fair = [95, 75, 55, 8]
poor = [90, 70, 50, 7]
bad = [85, 65, 45, 5]
sur_g = dict(zip(surface, good))
sur_f = dict(zip(surface, fair))
sur_p = dict(zip(surface, poor))
sur_b = dict(zip(surface, bad))


def travelTime(road):
    roadName = arcpy.Describe(road)
    length = 'km'
    TravelTime = 'TravelTime'
    cursor = arcpy.UpdateCursor(road) #, fields = 'Type', 'Quality')
    type1 = 'Type' #Asphalt, concrete, gravel, earth
    qual = 'Quality' #Good, fair, poor, bad
    for row in cursor:
        if row.getValue(type1) == 'Asphalt':
            if row.getValue(qual) == 'Good':
                ttime = row.getValue(length)/ sur_g[1]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Fair':
                ttime = row.getValue(length)/ sur_f[1]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Poor':
                ttime = row.getValue(length)/ sur_p[1]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Bad':
                ttime = row.getValue(length)/ sur_b[1]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
        if row.getValue(type1) == 'Concrete':
            if row.getValue(qual) == 'Good':
                ttime = row.getValue(length)/ sur_g[2]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Fair':
                ttime = row.getValue(length)/ sur_f[2]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Poor':
                ttime = row.getValue(length)/ sur_p[2]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Bad':
                ttime = row.getValue(length)/ sur_b[2]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
        if row.getValue(type1) == 'Gravel':
            if row.getValue(qual) == 'Good':
                ttime = row.getValue(length)/ sur_g[3]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Fair':
                ttime = row.getValue(length)/ sur_f[3]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Poor':
                ttime = row.getValue(length)/ sur_p[3]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Bad':
                ttime = row.getValue(length)/ sur_b[3]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
        if row.getValue(type1) == 'Earth':
            if row.getValue(qual) == 'Good':
                ttime = row.getValue(length)/ sur_g[4]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Fair':
                ttime = row.getValue(length)/ sur_f[4]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Poor':
                ttime = row.getValue(length)/ sur_p[4]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)
            if row.getValue(qual) == 'Bad':
                ttime = row.getValue(length)/ sur_b[4]
                row.setValue(TravelTime, ttime)
                cursor.updateRow(row)



travelTime(road2)

del road2

print 'finished'












