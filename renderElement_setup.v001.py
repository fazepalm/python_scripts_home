import maya.cmds as cmds
import maya.mel as mel


class create_VRay_Passes():

    def __INIT__( self ):
        
        print "Creating VRay Render Passes That Don't Exist!"
        
        self.elementTypeList = []
        self.RGB = [ 'R', 'G', 'B' ]   
        self.renderElementList = [ 'diffuseChannel', 'reflectChannel', 'refractChannel', 'specularChannel', 'giChannel', 'lightingChannel', 'matteShadowChannel', 'shadowChannel', 'normalsChannel', 'selfIllumChannel', 'zdepthChannel', 'velocityChannel' ]
        self.userRenderElementList = { 'AO':'ExtraTexElement', 'Fresnel':'ExtraTexElement', 'WPP':'ExtraTexElement', 'UV':'ExtraTexElement' }                
        self.vrayPrefix = 'vrayRE_'
        self.place2D_NAME_G = '2dPlace'
        self.FRESNEL_TXT_NAME_G = 'FRESNEL_TXT'
        self.samplerInfoNode = 'UTILITY_SAMPLE_NODE'
        self.defaultSceneRenderElement = cmds.ls( exactType = "VRayRenderElement" )
        for sceneRenderElement in self.defaultSceneRenderElement:
            self.elementTypeList.append( cmds.getAttr( sceneRenderElement + '.vrayClassType' ) )
            
        self._create_passes()
        
    def _getExtraTexConn( self, channelName ):
        conn = cmds.listConnections( channelName + '.vray_texture_extratex', plugs = True, connections = True )  
        return conn 
                 
    def _create_passes( self ):
        
        for channelName in self.renderElementList:
            if channelName not in self.elementTypeList:
                melString = "vrayAddRenderElement %s;" % ( channelName )
                elementName = mel.eval( melString )
                if 'velocity' in channelName:
                    cmds.setAttr( elementName + '.vray_ignorez_velocity', 0 )
        for userChannelName, userChannelType in self.userRenderElementList.iteritems():
            customRenamedElementName = self.vrayPrefix + userChannelName  
            if self.vrayPrefix + userChannelName not in self.defaultSceneRenderElement:
                melString = "vrayAddRenderElement %s;" % ( userChannelType )
                customElementName = mel.eval( melString )
                cmds.rename( customElementName, self.vrayPrefix + userChannelName )
                cmds.setAttr( customRenamedElementName + ".vray_name_extratex", userChannelName, type = "string" )                    
                cmds.setAttr( customRenamedElementName + ".vray_explicit_name_extratex", userChannelName, type = "string" )
            else:
                print customRenamedElementName + ' Exists, Attempting to Connect'

            if cmds.objExists( customRenamedElementName ):
                userElementConn = self._getExtraTexConn( customRenamedElementName )
                if userElementConn == None:
                    if 'AO' in userChannelName:
                        AO_TXT = cmds.shadingNode( 'VRayDirt', asTexture = True  )
                        AO_TXT_NAME = cmds.rename( AO_TXT, "AO_TXT" )                
                        if not cmds.objExists( self.place2D_NAME_G ) :
                            place2D = cmds.shadingNode( 'place2dTexture', asUtility = True  )
                            place2D_NAME = cmds.rename( place2D, "place2D" )                    
                        cmds.connectAttr( place2D_NAME + '.outUV', AO_TXT_NAME + '.uvCoord' ) 
                        cmds.connectAttr( place2D_NAME + '.outUvFilterSize', AO_TXT_NAME + '.uvFilterSize' )
                        cmds.setAttr( AO_TXT_NAME + '.doubleSided', 1 )
                        cmds.setAttr( AO_TXT_NAME + '.workWithTransparency', 1 )
                        cmds.setAttr( AO_TXT_NAME + '.resultAffectInclusive', 0 )
                        cmds.setAttr( AO_TXT_NAME + '.radius', 12 )
                        if self._getExtraTexConn( customRenamedElementName ) == None:                        
                            cmds.connectAttr( AO_TXT_NAME + '.outColor', customRenamedElementName + '.vray_texture_extratex', force = True )           
                    
                    if 'Fresnel' in userChannelName:
                        if not cmds.objExists( self.place2D_NAME_G ) :
                            place2D = cmds.shadingNode( 'place2dTexture', asUtility = True  )   
                            place2D_NAME = cmds.rename( place2D, "place2D" )
                            
                        if not cmds.objExists( self.FRESNEL_TXT_NAME_G ) :
                            FRESNEL_TXT = cmds.shadingNode( 'VRayFresnel', asTexture = True  )
                            FRESNEL_TXT_NAME = cmds.rename( FRESNEL_TXT, "FRESNEL_TXT" )                
                            cmds.connectAttr( place2D_NAME + '.outUV', FRESNEL_TXT_NAME + '.uvCoord' ) 
                            cmds.connectAttr( place2D_NAME + '.outUvFilterSize', FRESNEL_TXT_NAME + '.uvFilterSize' ) 

                            if self._getExtraTexConn( customRenamedElementName ) == None:                        
                                cmds.connectAttr( FRESNEL_TXT_NAME + '.outColor', customRenamedElementName + '.vray_texture_extratex', force = True )                                                                                  
                    
                    if 'WPP' in userChannelName:
                        if not cmds.objExists( self.samplerInfoNode ):
                            sNode = cmds.shadingNode('samplerInfo', asUtility=True)
                            sNode = cmds.rename(sNode, samplerInfoNode)
                        if 'vrayPointWorldReference' not in cmds.listAttr( self.samplerInfoNode ): 
                            cmds.vray( "addAttributesFromGroup", self.samplerInfoNode, "vray_samplerinfo_extra_tex", 1 )  
                        if self._getExtraTexConn( customRenamedElementName ) == None:                        
                            cmds.connectAttr( self.samplerInfoNode + '.vrayPointWorldReference', customRenamedElementName + '.vray_texture_extratex', force = True )           
                    
                    if 'UV' in userChannelName:
                        if not cmds.objExists( self.samplerInfoNode ):
                            sNode = cmds.shadingNode('samplerInfo', asUtility=True)
                            sNode = cmds.rename(sNode, self.samplerInfoNode) 
                        userUVElementConnR = cmds.listConnections( customRenamedElementName + '.vray_texture_extratexR', plugs = True, connections = True )
                        if userUVElementConnR == None:                              
                            cmds.connectAttr( self.samplerInfoNode + '.uCoord', customRenamedElementName + '.vray_texture_extratexR', force = True ) 
                        userUVElementConnG = cmds.listConnections( customRenamedElementName + '.vray_texture_extratexG', plugs = True, connections = True )
                        if userUVElementConnG == None:                                        
                            cmds.connectAttr( self.samplerInfoNode + '.vCoord', customRenamedElementName + '.vray_texture_extratexG', force = True )           
                          

        
create_VRay_Passes().__INIT__()