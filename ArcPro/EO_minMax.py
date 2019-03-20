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
stats = "MIN_MAX_MEAN"
ZonalStatisticsAsTable(inSHP, zone, inDEM, outZS, ndBehavior, stats)

#below from https://community.esri.com/thread/44338
myField = "MIN"  
minValue = arcpy.SearchCursor(outZS, "", "", "", myField + " A").next().getValue(myField) #Get 1st row in ascending cursor sort  
minFT = minValue*3.28084
myField = "MAX"  
maxValue = arcpy.SearchCursor(outZS, "", "", "", myField + " D").next().getValue(myField) #Get 1st row in descending cursor sort  
maxFT = maxValue*3.28084
#f.write("{0}, {1}, {2}, {3}".format(row.VEHICLEID,row.NEAR_X,row.NEAR_Y,row.TIME))
print("Minimum elevation:%.2f meters (%.2f ft)\nMaximum elevation:%.2f meters (%.2f ft)"%(minValue,minFT,maxValue,maxFT))
arcpy.AddMessage("\n\nMinimum elevation:%.2f meters (%.2f ft)\nMaximum elevation:%.2f meters (%.2f ft)\n\n"%(minValue,minFT,maxValue,maxFT))
