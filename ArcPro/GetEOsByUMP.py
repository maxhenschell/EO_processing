# Name: Get EOs within a selected UMP
# See tool for help
# Output gdb is name of UMP

# Import system modules
import arcpy 
import os
#from arcpy import env
import sys

#clean up
arcpy.Delete_management("EOlyr") 
arcpy.Delete_management("UMPlyr") 
arcpy.env.overwriteOutput = True

# Set global variables
decUMP = r"M:/reg0/reg0data/layerfiles/decumpareas.lyr" 
stwdEO = r"W:/GIS_Data/EO_Mapping/_statewide_EOs/statewide_eos.shp"
decLand = r"M:\reg0\reg0data\layerfiles\pubpoly.lyr"
xy_tolerance = ""
UMPfield = "NEW_UMP_CO"
EOfield = "ELEM_TYPE"
EOTypes = ['A','C','P']

# Set environment settings
UMPs = arcpy.GetParameterAsText(0)
outDir = arcpy.GetParameterAsText(1) #"C:/Users/mxhensch/GIS_data"
arcpy.env.workspace = outDir

arcpy.AddMessage("UMPs to process: {}".format(UMPs))

for i in UMPs.split(';'):
    arcpy.AddMessage("...{}...".format(i))
    UMP = i#; print(UMP)
    UMP = UMP.replace("'", "")
    UMP = UMP.upper()
    UMP_sim = UMP.replace(" ", "_")
    gdb = UMP_sim+".gdb"
    arcpy.AddMessage("Processing {}...".format(UMP))

    
    #Check if gdb exists, create if not
    if not arcpy.Exists(gdb):
        arcpy.CreateFileGDB_management(outDir, gdb)
        #print("   FileGDB created")
    #else: print("   FileGDB exists")
    outLocation = os.path.join(outDir, gdb)

    UMP_out = outLocation+"/"+UMP_sim+"_land"

    # Get a layer DEC_UMP
    arcpy.MakeFeatureLayer_management(decUMP, "UMPlyr") 
    
    # sql statement to select the UMP from the DEC_UMP shapefile
    sql_exp = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters("UMPlyr", UMPfield),UMP)
    arcpy.AddMessage(sql_exp)
	
    # Select UMP of interest
    arcpy.SelectLayerByAttribute_management("UMPlyr", "NEW_SELECTION",sql_exp)
    
    #Clip DEC lands layer to UMP
    arcpy.Clip_analysis(decLand, "UMPlyr", UMP_out)
    
    # Make the statewide a layer
    arcpy.MakeFeatureLayer_management(stwdEO, "EOlyr") 

    #get EOs by type
    for eo in EOTypes:
    	EO_out = outLocation+"/"+UMP_sim+"_EOs_"+eo
    	#print("   %s"%EO_out)
    	query2 = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters("EOlyr",EOfield),eo)
    	
    	# Select eo types
    	arcpy.SelectLayerByAttribute_management("EOlyr", "NEW_SELECTION", query2) 
    	
    	# intersect the UMP and eo layers, then write it out
    	arcpy.SelectLayerByLocation_management("EOlyr", "intersect", "UMPlyr", 0, "SUBSET_SELECTION")
    	arcpy.CopyFeatures_management("EOlyr", EO_out)
    
    #clean up
    arcpy.Delete_management("EOlyr") 
    arcpy.Delete_management("UMPlyr") 
	arcpy.AddMessage("{} completed!".format(UMP))