# -*- coding: utf-8 -*-


import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters

folder = arcpy.GetParameterAsText(0)

# Variables
BWI_New_Datasource = "Database Connections/bwi_pub@maa-dodb-19c.sde"
MTN_New_Datasource = "Database Connections/mtn_pub@maa-dodb-19c.sde"
OutFolder = "C:\Workspace\\MAA\\"

#Output for Total Count
# outStr = "{0}{1}".format(OutFolder, "\\FcCount.csv")
# csv_out = open(outStr, "w")

#Output for All Null Value Records
outStrRecords = "{0}{1}".format(OutFolder, "\\FcCountRecords.csv")
csv_out_records = open(outStrRecords, "w")

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for root, dirs, files in os.walk(folder):

    for f in files:
        if f.endswith(".mxd"):
            mxd = root + '\\' + f

            mxd1 = arcpy.mapping.MapDocument(mxd)
            if "bak" not in mxd:
                if "External_Share" not in mxd:
                    if "Imagery" not in mxd:
                        if "GIS_MAP" not in mxd:
                            for lyr in arcpy.mapping.ListLayers(mxd1):
                                if lyr.isGroupLayer == False:
                                    try:
                                        if "%" not in lyr.dataSource:
                                            arcpy.AddMessage(lyr.dataSource)
                                            fields = arcpy.ListFields(lyr.dataSource)
                                            counter = 0
                                            for field in fields:
                                                arcpy.AddMessage(field.name)
                                                if "OBJECT" not in field.name:
                                                    try:
                                                        TotalfcCount = arcpy.GetCount_management(lyr.dataSource).getOutput(0)
                                                        total_message = "Total Values for " + lyr.dataSource + "=" + TotalfcCount
                                                        arcpy.AddMessage(total_message)
                                                        counter += 1
                                                        strCounter = str(counter)
                                                        temp_layer = lyr.dataSource + strCounter
                                                        arcpy.AddMessage(temp_layer)
                                                        if arcpy.Exists(temp_layer):
                                                            arcpy.AddMessage("Skip")
                                                        else:
                                                            query = field.name + " IS NULL"
                                                            arcpy.MakeFeatureLayer_management(lyr.dataSource, temp_layer,query)

                                                            TotalNullValues = arcpy.GetCount_management(temp_layer).getOutput(0)
                                                            null_message = "Total Null Values for " + lyr.dataSource + "=" + TotalNullValues
                                                            arcpy.AddMessage(null_message)

                                                            # #Output for Total Count
                                                            # # create string to add to csv
                                                            # outStr = "{0},{1},{2}\n".format(mxd, lyr.dataSource,TotalfcCount)
                                                            # arcpy.AddMessage(outStr)
                                                            # # write to file
                                                            # csv_out.write(outStr)

                                                            #Output for All Null Value Records
                                                            outStrRecords = "{0},{1},{2},{3},{4}\n".format(mxd, lyr.dataSource,field.name, TotalfcCount,TotalNullValues)
                                                            arcpy.AddMessage(outStrRecords)
                                                            # write to file
                                                            csv_out_records.write(outStrRecords)
                                                    except arcpy.ExecuteError:
                                                        arcpy.AddMessage(arcpy.GetMessages(2))
                                                        pass

                                    except arcpy.ExecuteError:
                                        arcpy.AddMessage(arcpy.GetMessages(2))
                                        pass
