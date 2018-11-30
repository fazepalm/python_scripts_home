import maya.cmds as cmds
import re
import traceback

disconnectShaders = 1

def getNodeType(nodeList, nodeTypeWanted):
    for node in nodeList:
        nodeType = cmds.nodeType(node)
        #print nodeType
        if nodeType == nodeTypeWanted:            
            return node
            
def connectShaders( selectedList, validVrayShaderList ):
    try:
        selected_proxy = selectedList[0]
        sel_proxy_shape = cmds.listRelatives(selected_proxy, shapes = True)[0]
        sel_proxy_shape_conn_list = cmds.listConnections(sel_proxy_shape)
        sel_proxy_shape_shaderSG = getNodeType(sel_proxy_shape_conn_list, "shadingEngine")
        sel_proxy_shape_shaderSG_conn = cmds.listConnections(sel_proxy_shape_shaderSG)
        sel_proxy_shape_shader = getNodeType(sel_proxy_shape_shaderSG_conn, "VRayMeshMaterial")
        shaderIndexSize = cmds.getAttr(sel_proxy_shape_shader + ".shaderNames", size = True)
        for shaderIndex in range(0, shaderIndexSize):
            proxyObj_shader = cmds.getAttr(sel_proxy_shape_shader + ".shaderNames" + "[" + str(shaderIndex) + "]")
            for vrayShader in validVrayShaders:
                if "_shd" in vrayShader:
                    vrayShader_str = vrayShader.split("_shd")[0]
                else:
                    vrayShader_str = vrayShader                    
                if re.findall(vrayShader_str, proxyObj_shader, re.IGNORECASE):
                    print "Shader Index: %s" % (shaderIndex)
                    print "Vray Shader: %s" % (vrayShader)            
                    print "Proxy Obj Shader: %s" % (proxyObj_shader)
                    print "\n"
                    sel_proxy_shape_shader_index = sel_proxy_shape_shader + ".shaders" + "[" + str(shaderIndex) + "]"            
                    sel_proxy_shape_shader_conn = cmds.listConnections(sel_proxy_shape_shader_index, connections = True, plugs = True)            
                    if disconnectShaders:
                        if sel_proxy_shape_shader_conn != None:
                            print ("disconnecting %s from %s" % (sel_proxy_shape_shader_conn[1], sel_proxy_shape_shader_conn[0]))
                            cmds.disconnectAttr(sel_proxy_shape_shader_conn[1], sel_proxy_shape_shader_conn[0])
                    sel_proxy_shape_shader_conn = cmds.listConnections(sel_proxy_shape_shader_index, connections = True, plugs = True)                                
                    if sel_proxy_shape_shader_conn == None:
                        print ("connecting %s from %s" % (vrayShader + ".outColor", sel_proxy_shape_shader_index))                
                        cmds.connectAttr(vrayShader + ".outColor", sel_proxy_shape_shader_index)
                        print "\n"
    except:
        traceback.print_exc()
                
validVrayShaders = cmds.ls(exactType = "VRayMtl")
selectedList = cmds.ls(sl=True)
connectShaders( selectedList, validVrayShaders )
