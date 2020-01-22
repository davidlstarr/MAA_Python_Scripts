# -*- coding: utf-8 -*-


import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)

for root, dirs, files in os.walk(arcpy.env.workspace):

    for f in files:
        if f.endswith(".mxd"):
            mxd = root + '\\' + f
            #arcpy.AddMessage(mxd)
            mxd1 = arcpy.mapping.MapDocument(mxd)

            for lyr in arcpy.mapping.ListLayers(mxd1):
                if lyr.isGroupLayer == False:
                    arcpy.AddMessage(lyr.datasetName)
                    if "BWI" in mxd:
                        if "Imagery" not in mxd:
                            if "GIS_MAP" not in mxd:
                                if "bwi_pub@maa-dodb-19c" in lyr.dataSource:
                                       bwi_Message = "Already Updated -- " + lyr.name
                                       arcpy.AddMessage(bwi_Message)
                                else:
                                    bwiPub_Message = "BWI--Replace Data Source for " + lyr.name
                                    arcpy.AddMessage(bwiPub_Message)
                                    lyr.replaceDataSource(
                                        "C:\\Users\\dstarr\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\bwi_pub@maa-dodb-19c.sde",
                                        "SDE_WORKSPACE", lyr.datasetName, False)
                    else:
                        if "Imagery" not in mxd:
                            if "GIS_MAP" not in mxd:
                                if "mtn_pub@maa-dodb-19c" in lyr.dataSource:
                                    mtn_Message = "Already Updated -- " + lyr.name
                                    arcpy.AddMessage(mtn_Message)
                                else:
                                    mtnPub_Message = "MTN--Replace Data Source for " + lyr.name
                                    arcpy.AddMessage(mtnPub_Message)
                                    lyr.replaceDataSource(
                                        "C:\\Users\\dstarr\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\mtn_pub@maa-dodb-19c.sde",
                                        "SDE_WORKSPACE", lyr.datasetName, False)

                # lyr.replaceDataSource("C:\\Users\\dstarr\\AppData\\Roaming\\ESRI\\Desktop10.6\\ArcCatalog\\RICS_Connection.sde", "SDE_WORKSPACE", "TEST")

            mxd1.save()
            # mxd = arcpy.mapping.MapDocument(path)
            # mxd.findAndReplaceWorkspacePaths(r"C:\Users\dstarr\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\bwi_pub@maa-dodb-11g.sde",r"C:\Users\dstarr\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\bwi_pub@maa-dodb-19c.sde", False)
