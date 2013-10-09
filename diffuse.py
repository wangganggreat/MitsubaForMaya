#-
# ==========================================================================
# Copyright (C) 1995 - 2006 Autodesk, Inc. and/or its licensors.  All 
# rights reserved.
#
# The coded instructions, statements, computer programs, and/or related 
# material (collectively the "Data") in these files contain unpublished 
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its 
# licensors, which is protected by U.S. and Canadian federal copyright 
# law and by international treaties.
#
# The Data is provided for use exclusively by You. You have the right 
# to use, modify, and incorporate this Data into other products for 
# purposes authorized by the Autodesk software license agreement, 
# without fee.
#
# The copyright notices in the Software and this entire statement, 
# including the above license grant, this restriction and the 
# following disclaimer, must be included in all copies of the 
# Software, in whole or in part, and all derivative works of 
# the Software, unless such copies or derivative works are solely 
# in the form of machine-executable object code generated by a 
# source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. 
# AUTODESK DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED 
# WARRANTIES INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF 
# NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR 
# PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE, OR 
# TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS LICENSORS 
# BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL, 
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK 
# AND/OR ITS LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY 
# OR PROBABILITY OF SUCH DAMAGES.
#
# ==========================================================================
#+
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaDiffuseShader"
kPluginNodeClassify = "shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x8700E)

class diffuse(OpenMayaMPx.MPxNode):
        def __init__(self):
                OpenMayaMPx.MPxNode.__init__(self)
                mOutColor = OpenMaya.MObject()
                mReflectance = OpenMaya.MObject()

        def compute(self, plug, block):
                if plug == diffuse.mOutColor or plug.parent() == diffuse.mOutColor:
                        resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
                        
                        color = block.inputValue( diffuse.mReflectance ).asFloatVector()

                        resultColor.x = color.x
                        resultColor.y = color.y
                        resultColor.z = color.z

                        outColorHandle = block.outputValue( diffuse.mOutColor )
                        outColorHandle.setMFloatVector(resultColor)
                        outColorHandle.setClean()
                else:
                        return OpenMaya.kUnknownParameter


def nodeCreator():
        return diffuse()

def nodeInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()

        try:
                diffuse.mReflectance = nAttr.createColor("reflectance", "r")
                nAttr.setKeyable(1) 
                nAttr.setStorable(1)
                nAttr.setReadable(1)
                nAttr.setWritable(1)

                diffuse.mOutColor = nAttr.createColor("outColor", "oc")
                nAttr.setStorable(0)
                nAttr.setHidden(0)
                nAttr.setReadable(1)
                nAttr.setWritable(0)

        except:
                sys.stderr.write("Failed to create attributes\n")
                raise

        try:
                diffuse.addAttribute(diffuse.mReflectance)
                diffuse.addAttribute(diffuse.mOutColor)
        except:
                sys.stderr.write("Failed to add attributes\n")
                raise

        try:
                diffuse.attributeAffects (diffuse.mReflectance, diffuse.mOutColor)
        except:
                sys.stderr.write("Failed in setting attributeAffects\n")
                raise


# initialize the script plug-in
def initializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, 
                                        nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
        except:
                sys.stderr.write( "Failed to register node: %s" % kPluginNodeName )
                raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterNode( kPluginNodeId )
        except:
                sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeName )
                raise