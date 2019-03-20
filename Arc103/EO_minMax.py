# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:11:31 2019

@author: mxhensch
"""

import arcpy 
from arcpy.sa import *
arcpy.env.overwriteOutput = True

inDEM = "M:/reg0/reg0data/layerfiles/DEM_10m.lyr"
inSHP = arcpy.GetParameterAsText(0)#"H:/GIS_data/EO_updates/Updates18_19/JonesPond_DSB.shp"
zone = "FID"
ndBehavior = "DATA"
outZS = "in_memory/outZS"
stats = "MIN_MAX"
ZonalStatisticsAsTable(inSHP, zone, inDEM, outZS, ndBehavior, stats)

#below from https://community.esri.com/thread/44338
myField = "MIN"  
minValue = arcpy.SearchCursor(outZS, "", "", "", myField + " A").next().getValue(myField) #Get 1st row in ascending cursor sort  
minFT = minValue*3.28084
myField = "MAX"  
maxValue = arcpy.SearchCursor(outZS, "", "", "", myField + " D").next().getValue(myField) #Get 1st row in descending cursor sort  
maxFT = maxValue*3.28084
arcpy.AddMessage("\n\nMinimum elevation:{0:.2f} meters ({1:.2f})\nMaximum elevation:{2:.2f} meters ({3:.2f} ft)\n\n".format(minValue,minFT,maxValue,maxFT))
