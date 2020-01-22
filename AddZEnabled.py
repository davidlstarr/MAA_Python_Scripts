# -*- coding: utf-8 -*-
"""
Script will copy over all datasets from original SDE database, z-enable and keep Global ID in tact for all feature classes, and copy over all datasets and feature classes over to new SDE database
Please ensure to create temporary GDB before running script. This will go in your Output GDB parameter!!!!!
"""

import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True
arcpy.env.outputZFlag = "Enabled"
arcpy.env.preserveGlobalIds = True

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)
outputGdb = arcpy.GetParameterAsText(1)

arcpy.AddWarning("Please ensure to create temporary GDB before running script. This will go in your Output GDB parameter")
# create datasets

datasets = arcpy.ListDatasets(feature_type='feature')
# arcpy.AddMessage(datasets)

# Copy dataset schema over from original SDE
arcpy.AddWarning("Setup Datasets")
for ds in datasets:
    try:
        InputPath = os.path.join(arcpy.env.workspace, ds)
        arcpy.AddMessage(InputPath)

        OutPath = outputGdb + "\\"
        # arcpy.AddMessage(OutPath)
        if arcpy.Exists(outputGdb + "\\" +ds):
            message = ds+" Exists!"
            arcpy.AddMessage(message)
        else:
            arcpy.CreateFeatureDataset_management(out_dataset_path=OutPath,
                                                  out_name=ds,
                                                  spatial_reference="PROJCS['NAD_1983_StatePlane_Maryland_FIPS_1900_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1312333.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-77.0],PARAMETER['Standard_Parallel_1',38.3],PARAMETER['Standard_Parallel_2',39.45],PARAMETER['Latitude_Of_Origin',37.66666666666666],UNIT['Foot_US',0.3048006096012192]];-120561100 -95444400 3048.00609601219;-100000 3048.00609601219;-100000 10000;3.28083333333333E-03;3.28083333333333E-03;0.001;IsHighPrecision")
    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages(2))
        pass

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

# Create Feature classes with z-enabled and copy over feature classes from original sde
arcpy.AddWarning("Copy Feature Classes")
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        try:
            # arcpy.AddMessage(desc)
            InputPath = os.path.join(arcpy.env.workspace, ds, fc)
            desc = arcpy.Describe(InputPath)

            arcpy.AddMessage(InputPath)

            OutPath = outputGdb + "\\" + ds
            desc_output = arcpy.Describe(OutPath)
            arcpy.AddMessage(OutPath)

            OutPathFC = outputGdb + "\\" + ds + "\\" + fc

            # arcpy.AddMessage(desc_output.hasZ)
            arcpy.AddMessage(desc.shapeType)
            if arcpy.Exists(OutPathFC):
                arcpy.AddWarning("Feature Class already exists!")
            else:
                arcpy.CreateFeatureclass_management(out_path=OutPath, out_name=fc, geometry_type=desc.shapeType,
                                                    template=fc, has_m="DISABLED", has_z="ENABLED",
                                                    spatial_reference="PROJCS['NAD_1983_StatePlane_Maryland_FIPS_1900_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1312333.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-77.0],PARAMETER['Standard_Parallel_1',38.3],PARAMETER['Standard_Parallel_2',39.45],PARAMETER['Latitude_Of_Origin',37.66666666666666],UNIT['Foot_US',0.3048006096012192]];-120561100 -95444400 3048.00609601219;-100000 3048.00609601219;-100000 10000;3.28083333333333E-03;3.28083333333333E-03;0.001;IsHighPrecision",
                                                    config_keyword="", spatial_grid_1="0", spatial_grid_2="0",
                                                    spatial_grid_3="0")
                arcpy.CopyFeatures_management(InputPath, OutPathFC)


        except arcpy.ExecuteError:
            arcpy.AddMessage(arcpy.GetMessages(2))
            pass



