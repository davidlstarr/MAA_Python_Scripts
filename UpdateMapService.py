# -*- coding: utf-8 -*-


import arcpy
import os
import xml.dom.minidom as DOM

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
arcpy.env.workspace = arcpy.GetParameterAsText(0)

for root, dirs, files in os.walk(arcpy.env.workspace):

    for f in files:
        if f.endswith(".mxd"):
            try:
                mxd = root + '\\' + f
                con = 'GIS Servers/arcgis on gis.rics-jmt.net (admin).ags'
                mxdFolder = mxd.rsplit('\\', 2)
                mxdName = mxd.rsplit('\\', 1)
                mxdNameSplit = mxdName[1].rsplit('.', 1)
                mxdNameFolder = mxdFolder[1] + "/" + mxdNameSplit[0]
                arcpy.AddMessage(mxdNameFolder)
                sddraft = arcpy.env.workspace + "\\" + mxdNameSplit[0] + ".sddraft"
                sd = arcpy.env.workspace + "\\" + mxdNameSplit[0] + ".sd"
                arcpy.AddMessage(sddraft)
                arcpy.AddMessage(sd)
                mxd1 = arcpy.mapping.MapDocument(mxd)
                # create service definition draft
                analysis = arcpy.mapping.CreateMapSDDraft(mxd1, sddraft, mxdNameFolder, 'ARCGIS_SERVER',
                                                          con, False, None, mxdNameSplit[0], mxdNameSplit[0])

                # change service parameters
                doc = DOM.parse(sddraft)
                keys = doc.getElementsByTagName('Key')
                for key in keys:
                    if key.firstChild.data == 'UsageTimeout': key.nextSibling.firstChild.data = 600
                    if key.firstChild.data == 'WaitTimeout': key.nextSibling.firstChild.data = 60
                    if key.firstChild.data == 'IdleTimeout': key.nextSibling.firstChild.data = 1800
                    if key.firstChild.data == 'MinInstances': key.nextSibling.firstChild.data = 1
                    if key.firstChild.data == 'MaxInstances': key.nextSibling.firstChild.data = 2
                services___ = doc.getElementsByTagName('TypeName')
                for service__ in services___:
                    if service__.firstChild.data == 'KmlServer':
                        service__.parentNode.getElementsByTagName('Enabled')[0].firstChild.data = 'false'
                    if service__.firstChild.data == 'WMSServer':
                        service__.parentNode.getElementsByTagName('Enabled')[0].firstChild.data = 'false'

                # save changes
                if os.path.exists(sddraft): os.remove(sddraft)
                f = open(sddraft, "w")
                doc.writexml(f)
                f.close()

                #set service type to esriServiceDefinitionType_Replacement
                #Comment this out if it is not a replace
                newType = 'esriServiceDefinitionType_Replacement'
                xml = sddraft
                doc = DOM.parse(xml)
                descriptions = doc.getElementsByTagName('Type')
                for desc in descriptions:
                    if desc.parentNode.tagName == 'SVCManifest':
                        if desc.hasChildNodes():
                            desc.firstChild.data = newType
                outXml = xml
                f = open(outXml, 'w')
                doc.writexml(f)
                f.close()

                #stage and upload the service if the sddraft analysis did not contain errors
                if analysis['errors'] == {}:
                    # Execute StageService
                    arcpy.StageService_server(sddraft, sd)
                    # Execute UploadServiceDefinition
                    arcpy.UploadServiceDefinition_server(sd, con)
                else:
                    # if the sddraft analysis contained errors, display them
                    arcpy.mapping.AnalyzeForSD(sddraft)
                    arcpy.AddMessage(analysis['errors'])
            except arcpy.ExecuteError:
                arcpy.AddMessage(arcpy.GetMessages(2))
                pass


