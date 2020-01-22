# -*- coding: utf-8 -*-

import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.


# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)
arcpy.AddMessage(output)

arcpy.env.overwriteOutput = True
arcpy.env.outputZFlag = "Enabled"
arcpy.env.preserveGlobalIds = True

arcpy.AddMessage(arcpy.env.outputZFlag)

# Local variables:
datasets = arcpy.ListDatasets(feature_type='feature')
arcpy.AddMessage(datasets)

# copy datasets
for ds in datasets:
    try:
        InputPath = os.path.join(arcpy.env.workspace, ds)
        arcpy.AddMessage(InputPath)

        OutPath = output + "\\" + ds
        arcpy.AddMessage(OutPath)
        arcpy.Copy_management(InputPath, OutPath, "FeatureDataset")
    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages(2))
        pass

featureclasses = arcpy.ListFeatureClasses()
arcpy.AddMessage(featureclasses)

for fc in featureclasses:
    InputPath = os.path.join(arcpy.env.workspace, fc)
    arcpy.AddMessage(InputPath)

    OutPath = output + "\\" + fc
    arcpy.AddMessage(OutPath)

    arcpy.CopyFeatures_management(InputPath, OutPath, "", "0", "0", "0")
