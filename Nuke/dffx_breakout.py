###################################
import nuke
import re
from PySide import QtGui

compPrefix = None
LS_CHANNEL_LIST = []
MM_CHANNEL_LIST = []
MM_MERGE_LIST = []
L_SHUFFLE_GRADE_LIST = []
UTIL_CHANNEL_LIST = []
CG_COPY_01_LIST = []
IGNORE_CHANNEL_LIST = []
REF_CHANNEL_LIST = []
CG_PASS_LIST_01 = []
CG_PASS_LIST_02 = []
MM_STR = "MM_"
L_STR = "L_"
L_SHUFFLE_Y_DIST = 100
L_SHUFFLE_X_DIST = 100
P_L_SHUFFLE = ""
C_Dist = 650
MM_SHUFFLE_DIST = 200
MM_SHUFFLE_SPACE = 10
UTIL_SHUFFLE_X_DIST = 100
UTIL_SHUFFLE_Y_DIST = 100
CG_SHUFFLE_X_DIST = 100
CG_SHUFFLE_Y_DIST = 100

#################################
#################################
#DEBUG
#################################
#################################
MM = 1
LS = 1
UTIL = 1
CG_PASSES = 1
#################################
#################################

UTIL_NAME_LIST = [ 'ao', 'frensel', 'fresnel', 'uv', 'wpp', 'xyz', 'depth', 'velocity', 'normals' ]
REF_LIST = [ 'specular', 'lighting' ]
IGNORE_LIST = [ 'rgba' ]

#Utility functions
def check_nodeExists( existsList ):
    for nodeName in existsList:
        return nuke.exists( nodeName )

#SHUFFLE
def shuffleLayer( node, channel, shuffleName, shuffleLabel ):
    shuffleNode = nuke.nodes.Shuffle( name = shuffleName, label = shuffleLabel, inputs=[node] )
    shuffleNode['in'].setValue( channel )
    shuffleNode['postage_stamp'].setValue( True )
    return shuffleNode

def getSetVars( inputNode, inputCount, rootNode, rootXpos, rootYpos, align ):
    inputNode_X_DIST = 100
    inputNode_Y_DIST = 100
    inputNode_X_VAL = None
    inputNode_Y_VAL = None
    rootNodeClass = None

    if rootNode != None:
        rootNodeClass = rootNode.Class()
    inputNode_W = inputNode.screenWidth() / 2
    inputNode_H = inputNode.screenHeight() / 2
    if align == 'horizontal':
        if rootXpos != None and rootYpos != None:
            inputNode_X_VAL = ( rootXpos + inputNode_W ) + ( inputNode_X_DIST * inputCount )
            if rootNodeClass == 'Dot':
                inputNode_Y_VAL = rootYpos - inputNode_H
            else:
                inputNode_Y_VAL = rootYpos
    if align == 'vertical':
        if rootXpos != None and rootYpos != None:
            inputNode_Y_VAL = ( rootYpos + inputNode_H ) + ( inputNode_Y_DIST * inputCount )
            if rootNodeClass == 'Dot':
                inputNode_X_VAL = rootXpos - inputNode_W
            else:
                inputNode_X_VAL = rootXpos

    if inputNode_X_VAL != None and inputNode_Y_VAL != None:
        inputNode.setXYpos( inputNode_X_VAL, inputNode_Y_VAL  )
    inputNode_XPos, inputNode_YPos = getNodePos( inputNode )

    return inputNode_W, inputNode_H, inputNode_XPos, inputNode_YPos

def shuffleFromList( compPrefix, CG_PASS_LIST, rootNode_01, rootXpos_01, rootYpos_01, useCount ):
    shuffleDict = {}
    shuffleVarList = []
    for CG_count, CG_CHANNEL in enumerate( CG_PASS_LIST ):
        if useCount:
            nodeCount = CG_count
        else:
            nodeCount = 1
        CG_SHUFFLE_NAME = compPrefix + "_" + CG_CHANNEL
        if not nuke.exists( CG_SHUFFLE_NAME ):
            if CG_count == 0:
                rootNode = rootNode_01
                rootXpos = rootXpos_01
                rootYpos = rootYpos_01
            else:
                rootNode = P_CG_SHUFFLE
                rootXpos = CG_SHUFFLE_XPos
                rootYpos = CG_SHUFFLE_YPos

            CG_SHUFFLE = shuffleLayer( rootNode, CG_CHANNEL, CG_SHUFFLE_NAME, CG_CHANNEL )

            CG_SHUFFLE_W, CG_SHUFFLE_H, CG_SHUFFLE_XPos, CG_SHUFFLE_YPos = getSetVars( CG_SHUFFLE,
                                                                                       nodeCount,
                                                                                       rootNode,
                                                                                       rootXpos,
                                                                                       rootYpos,
                                                                                       align = "horizontal" )
            #store previous shuffle dot
            P_CG_SHUFFLE = CG_SHUFFLE

            shuffleVarList = [ CG_SHUFFLE_W, CG_SHUFFLE_H, CG_SHUFFLE_XPos, CG_SHUFFLE_YPos ]
            shuffleDict[ CG_SHUFFLE ] = shuffleVarList

    return shuffleDict

def setShuffleValue( node, channel, value ):
    if nuke.exists( node.name() ):
        node[ channel ].setValue( value )

#Create Merge
def createMerge( mergeName, mergeLabel, operation ):
    MERGE_NODE = nuke.nodes.Merge2( name = mergeName,
                                label = mergeLabel,
                                operation = operation )
    return MERGE_NODE

#Create Dot
def createDot( dotName, nodeList ):
    dotNode = nuke.nodes.Dot( name = dotName, inputs=nodeList )
    return dotNode
###########

#Create Grade
def createGrade( gradeName, gradeLabel, nodeList ):
    gradeNode = nuke.nodes.Grade( name = gradeName, label = gradeLabel, inputs=nodeList )
    return gradeNode
###########

def setMergeInputs( node, nodeList ):
    for N_count, node_I in enumerate( nodeList ):
        index = N_count
        if N_count >= 2:
            index += 1
        node.setInput( index, node_I )

def getNodePos ( node ):
    nodeXpos = node.xpos()
    nodeYpos = node.ypos()
    return [ nodeXpos, nodeYpos ]

def breakout():
    try:
        node = nuke.selectedNode()
        nodeType = node.Class()

        if nodeType == 'Read':
            reqFields = ['exr/vrayInfo/%s' % i for i in ( ['renderlayer'] )]
            mData = node.metadata()
            if not set( reqFields ).issubset( mData ):
                nuke.warning( "renderLayer name not found, using node name instead" )
                compPrefix = node.name()
            else:
                compPrefix = node.name() + "_" + node.metadata( 'exr/vrayInfo/%s' % 'renderlayer' )

            C_DotName = compPrefix + "_C_Dot"
            LF_DotName = compPrefix + "_LF_Dot"
            R_DotName = compPrefix + "_R_Dot"
            CG_DotName_01 = compPrefix + "_CG_Dot_01"
            L_DotName_01 = compPrefix + "_L_Dot_01"
            L_DotName_02 = compPrefix + "_L_Dot_02"
            MM_DotName = compPrefix + "_MM_Dot"
            UTIL_DotName_01 = compPrefix + "_UTIL_Dot_01"
            CG_DotName_02 = compPrefix + "_CG_Dot_02"
            CG_DotName_03 = compPrefix + "_CG_Dot_03"

            channels = node.channels()
            channelNames = list( set( [ c.split( '.' ) [0] for c in channels ] ) )
            channelNames.sort()

            #channel list creation
            #################################
            for channel in channelNames:
                L_RE_MATCH = re.search( L_STR, channel, re.IGNORECASE  )
                MM_RE_MATCH = re.search( MM_STR, channel, re.IGNORECASE  )
                if L_RE_MATCH:
                    LS_CHANNEL_LIST.append( channel )
                if MM_RE_MATCH:
                    MM_CHANNEL_LIST.append( channel )
                for UTIL_NAME in UTIL_NAME_LIST:
                    UTIL_RE_MATCH = re.search( UTIL_NAME, channel, re.IGNORECASE  )
                    if UTIL_RE_MATCH:
                        if channel not in UTIL_CHANNEL_LIST:
                            UTIL_CHANNEL_LIST.append( channel )
                for REF_NAME in REF_LIST:
                    REF_RE_MATCH = re.search( REF_NAME, channel, re.IGNORECASE  )
                    if REF_RE_MATCH:
                        if channel not in REF_CHANNEL_LIST:
                            REF_CHANNEL_LIST.append( channel )
                for IGNORE_NAME in IGNORE_LIST:
                    IGNORE_RE_MATCH = re.search( IGNORE_NAME, channel, re.IGNORECASE  )
                    if IGNORE_RE_MATCH:
                        if channel not in IGNORE_CHANNEL_LIST:
                            IGNORE_CHANNEL_LIST.append( channel )

            CURR_TOTAL_PASSES = LS_CHANNEL_LIST + MM_CHANNEL_LIST + UTIL_CHANNEL_LIST

            REMAINING_PASSES = list( set( channelNames ) - set( CURR_TOTAL_PASSES ) )

            CG_CHANNEL_LIST = list( set( REMAINING_PASSES ) - ( set( IGNORE_CHANNEL_LIST ) | set( REF_CHANNEL_LIST ) ) )
            #################################
            #################################
            #NODE CREATION COUNT
            #################################
            #################################
            LS_NODE_COUNT = "max"
            if LS_NODE_COUNT == "max":
                LS_NODE_COUNT = LS_CHANNEL_LIST

            MM_NODE_COUNT = "max"
            if MM_NODE_COUNT == "max":
                MM_NODE_COUNT = MM_CHANNEL_LIST

            CG_NODE_COUNT = "max"
            if CG_NODE_COUNT == "max":
                CG_NODE_COUNT = CG_CHANNEL_LIST

            UTIL_NODE_COUNT = "max"
            if UTIL_NODE_COUNT == "max":
                UTIL_NODE_COUNT = UTIL_CHANNEL_LIST
            #################################
            #################################
            #Initial Dot Creation
            #################################
            #################################
            if not nuke.exists( C_DotName ):
                C_Dot_inputList = [node]
                C_Dot = createDot( C_DotName, C_Dot_inputList )
                C_DotXPos, C_DotYPos = getNodePos( C_Dot )
            else:
                C_Dot = nuke.toNode( C_DotName )

            if not nuke.exists( LF_DotName ):
                LF_Dot_inputList = [C_Dot]
                LF_Dot = createDot( LF_DotName, LF_Dot_inputList )
                LF_Dot.setXYpos( C_DotXPos - C_Dist, C_DotYPos )
                LF_DotXPos, LF_DotYPos = getNodePos( LF_Dot )
            else:
                LF_Dot = nuke.toNode( LF_DotName )

            if not nuke.exists( R_DotName ):
                R_Dot_inputList = [C_Dot]
                R_Dot = createDot( R_DotName, R_Dot_inputList )
                R_Dot.setXYpos( C_DotXPos + C_Dist, C_DotYPos )
                R_DotXPos, R_DotYPos = getNodePos( R_Dot )
            else:
                R_Dot = nuke.toNode( R_DotName )

            if not nuke.exists( CG_DotName_01 ):
                CG_Dot_inputList = [C_Dot]
                CG_Dot_01 = createDot( CG_DotName_01, CG_Dot_inputList )
                CG_Dot_01.setXYpos( C_DotXPos, C_DotYPos + 100 )
                CG_DotXPos_01, CG_DotYPos_01 = getNodePos( CG_Dot_01 )
            else:
                CG_Dot_01 = nuke.toNode( CG_DotName_01 )

            if not nuke.exists( MM_DotName ):
                MM_Dot_inputList = [LF_Dot]
                MM_Dot = createDot( MM_DotName, MM_Dot_inputList )
                MM_Dot.setXYpos( LF_DotXPos, LF_DotYPos + 100 )
                MM_DotXPos, MM_DotYPos = getNodePos( MM_Dot )
            else:
                MM_Dot = nuke.toNode( MM_DotName )

            if not nuke.exists( L_DotName_01 ):
                L_Dot_01_inputList = [CG_Dot_01]
                L_Dot_01 = createDot( L_DotName_01, L_Dot_01_inputList )
                L_Dot_01.setXYpos( CG_DotXPos_01 - 300, CG_DotYPos_01 )
                L_DotXPos_01, L_DotYPos_01 = getNodePos( L_Dot_01 )
            else:
                L_Dot_01 = nuke.toNode( L_DotName_01 )

            if not nuke.exists( L_DotName_02 ):
                if nuke.exists( L_DotName_01 ):
                    L_Dot_02_inputList = [L_Dot_01]
                    L_Dot_02 = createDot( L_DotName_02, L_Dot_02_inputList )
                    L_Dot_02.setXYpos( L_DotXPos_01, L_DotYPos_01 + L_SHUFFLE_Y_DIST )
                    L_DotXPos_02, L_DotYPos_02 = getNodePos( L_Dot_02 )
            else:
                L_Dot_02 = nuke.toNode( L_DotName_02 )

            if not nuke.exists( CG_DotName_02 ):
                if nuke.exists( L_Dot_02.name() ):
                    CG_Dot_02_inputList = [L_Dot_02]
                    CG_Dot_02 = createDot( CG_DotName_02, CG_Dot_02_inputList )
                    CG_Dot_02.setXYpos( L_DotXPos_02, L_DotYPos_02 + 300 )
                    CG_DotXPos_02, CG_DotYPos_02 = getNodePos( CG_Dot_02 )
            else:
                CG_Dot_02 = nuke.toNode( CG_DotName_02 )

            if not nuke.exists( CG_DotName_03 ):
                if nuke.exists( CG_Dot_02.name() ):
                    CG_Dot_03_inputList = [CG_Dot_02]
                    CG_Dot_03 = createDot( CG_DotName_03, CG_Dot_03_inputList )
                    CG_Dot_03.setXYpos( CG_DotXPos_02, CG_DotYPos_02 + 600 )
                    CG_DotXPos_03, CG_DotYPos_03 = getNodePos( CG_Dot_03 )
            else:
                CG_Dot_03 = nuke.toNode( CG_DotName_03 )

            if not nuke.exists( UTIL_DotName_01 ):
                UTIL_Dot_01_inputList = [R_Dot]
                UTIL_Dot_01 = createDot( UTIL_DotName_01, UTIL_Dot_01_inputList )
                UTIL_Dot_01.setXYpos( R_DotXPos, R_DotYPos + 300 )
                UTIL_DotXPos_01, UTIL_DotYPos_01 = getNodePos( UTIL_Dot_01 )

            else:
                UTIL_Dot_01 = nuke.toNode( UTIL_DotName_01 )

            #################################
            #################################
            #breakout MM
            #################################
            #################################

            if MM == 1:
                if nuke.exists( MM_DotName ):
                    shuffleChannels = [ 'red', 'green', 'blue', 'alpha' ]
                    for count, MM_CHANNEL in enumerate( MM_CHANNEL_LIST ):
                        if count <= MM_NODE_COUNT:
                            MM_SHUFFLE_DOT_NAME = compPrefix + "_" + MM_CHANNEL
                            if not nuke.exists( MM_SHUFFLE_DOT_NAME ):
                                MM_SHUFFLE_DOT_inputList = [MM_Dot]
                                MM_SHUFFLE_DOT = createDot( MM_SHUFFLE_DOT_NAME, MM_SHUFFLE_DOT_inputList )
                                MM_SHUFFLE_DOT.setXYpos( MM_DotXPos - ( ( count + 1 ) * MM_SHUFFLE_DIST ), MM_DotYPos )

                                MM_SHUFFLE_DOT_XPos, MM_SHUFFLE_DOT_YPos = getNodePos( MM_SHUFFLE_DOT )
                            else:
                                MM_SHUFFLE_DOT = nuke.toNode( MM_SHUFFLE_DOT_NAME )

                            MM_SHUFFLE_NAME_R = compPrefix + "_" + MM_CHANNEL + "_R"
                            MM_SHUFFLE_NAME_G = compPrefix + "_" + MM_CHANNEL + "_G"
                            MM_SHUFFLE_NAME_B = compPrefix + "_" + MM_CHANNEL + "_B"

                            if count != 0:
                                if nuke.exists( P_MM_SHUFFLE_DOT.name() ):
                                    MM_SHUFFLE_DOT.setInput( 0, P_MM_SHUFFLE_DOT )

                            #store previous shuffle dot
                            P_MM_SHUFFLE_DOT = MM_SHUFFLE_DOT

                            if not nuke.exists( MM_SHUFFLE_NAME_R ):
                                MM_SHUFFLE_R = shuffleLayer( MM_SHUFFLE_DOT, MM_CHANNEL, MM_SHUFFLE_NAME_R, MM_CHANNEL + "_R" )
                                MM_SHUFFLE_R_W, MM_SHUFFLE_R_H, MM_SHUFFLE_R_XPos, MM_SHUFFLE_R_YPos = getSetVars( MM_SHUFFLE_R,
                                                                                                                        1,
                                                                                                                        None,
                                                                                                                        None,
                                                                                                                        None,
                                                                                                                        align = 'vertical' )
                                for sChannel in shuffleChannels:
                                    setShuffleValue( MM_SHUFFLE_R, sChannel, "red" )
                            else:
                                MM_SHUFFLE_R = nuke.toNode( MM_SHUFFLE_NAME_R )

                            if not nuke.exists( MM_SHUFFLE_NAME_G ):
                                MM_SHUFFLE_G = shuffleLayer( MM_SHUFFLE_R, MM_CHANNEL, MM_SHUFFLE_NAME_G, MM_CHANNEL + "_G" )
                                MM_SHUFFLE_G_W, MM_SHUFFLE_G_H, MM_SHUFFLE_G_XPos, MM_SHUFFLE_G_YPos = getSetVars( MM_SHUFFLE_G,
                                                                                                                        1,
                                                                                                                        None,
                                                                                                                        MM_SHUFFLE_R_XPos,
                                                                                                                        MM_SHUFFLE_R_YPos,
                                                                                                                        align = 'vertical' )
                                for sChannel in shuffleChannels:
                                    setShuffleValue( MM_SHUFFLE_G, sChannel, "green" )

                            else:
                                MM_SHUFFLE_G = nuke.toNode( MM_SHUFFLE_NAME_G )

                            if not nuke.exists( MM_SHUFFLE_NAME_B ):
                                MM_SHUFFLE_B = shuffleLayer( MM_SHUFFLE_G, MM_CHANNEL, MM_SHUFFLE_NAME_B, MM_CHANNEL + "_B" )
                                MM_SHUFFLE_B_W, MM_SHUFFLE_B_H, MM_SHUFFLE_B_XPos, MM_SHUFFLE_B_YPos = getSetVars( MM_SHUFFLE_B,
                                                                                                                        1,
                                                                                                                        None,
                                                                                                                        MM_SHUFFLE_G_XPos,
                                                                                                                        MM_SHUFFLE_G_YPos,
                                                                                                                        align = 'vertical' )
                                for sChannel in shuffleChannels:
                                    setShuffleValue( MM_SHUFFLE_B, sChannel, "blue" )
                            else:
                                MM_SHUFFLE_B = nuke.toNode( MM_SHUFFLE_NAME_B )

                            if check_nodeExists( [ MM_SHUFFLE_R.name(), MM_SHUFFLE_G.name(), MM_SHUFFLE_B.name() ] ):
                                MM_SHUFFLE_LIST = [ MM_SHUFFLE_R, MM_SHUFFLE_B, MM_SHUFFLE_G ]
                                MM_MERGE_NAME = compPrefix + "_" + MM_CHANNEL + "_MERGE"
                                if not nuke.exists( MM_MERGE_NAME ):
                                    MM_MERGE = createMerge( MM_MERGE_NAME, MM_CHANNEL + "_MERGE", "plus" )
                                else:
                                    MM_MERGE = nuke.toNode( MM_MERGE_NAME )

                                #connect shuffles to first merge
                                setMergeInputs( MM_MERGE, MM_SHUFFLE_LIST )

                                MM_MERGE_W, MM_MERGE_H, MM_MERGE_XPos, MM_MERGE_YPos = getSetVars( MM_MERGE,
                                                                                                    1,
                                                                                                    None,
                                                                                                    None,
                                                                                                    None,
                                                                                                    align = 'horizontal' )

                                MM_MERGE_LIST.append( MM_MERGE )

                            if MM_MERGE_LIST != []:
                                if len( MM_MERGE_LIST ) >= 2:
                                    MM_MERGE_NAME_END = compPrefix + "_MM_MERGE_END"
                                    if not nuke.exists( MM_MERGE_NAME_END ):
                                        MM_MERGE_END = createMerge( MM_MERGE_NAME_END, "MM_MERGE_END", "plus" )

                                    else:
                                        MM_MERGE_END = nuke.toNode( MM_MERGE_NAME_END )

                                    #connect shuffle merge's to final merge node
                                    setMergeInputs( MM_MERGE_END, MM_MERGE_LIST )

            #################################
            #################################
            #breakout LS
            #################################
            #################################

            if LS == 1:
                if LS_CHANNEL_LIST != []:
                    if nuke.exists( CG_Dot_01.name() ):
                        if nuke.exists( L_Dot_02.name() ):
                            for L_count, L_CHANNEL in enumerate( LS_CHANNEL_LIST ):
                                if L_count <= LS_NODE_COUNT:
                                    L_SHUFFLE_NAME = compPrefix + "_" + L_CHANNEL
                                    if not nuke.exists( L_SHUFFLE_NAME ):
                                        if L_count == 0:
                                            L_SHUFFLE = shuffleLayer( L_Dot_02, L_CHANNEL, L_SHUFFLE_NAME, L_CHANNEL )

                                        else:
                                            if nuke.exists( P_L_SHUFFLE.name() ):
                                                L_SHUFFLE = shuffleLayer( P_L_SHUFFLE, L_CHANNEL, L_SHUFFLE_NAME, L_CHANNEL )

                                        L_SHUFFLE_W, L_SHUFFLE_H, L_SHUFFLE_XPos, L_SHUFFLE_YPos = getSetVars( L_SHUFFLE,
                                                                                                                L_count + 1,
                                                                                                                L_Dot_02,
                                                                                                                L_DotXPos_02,
                                                                                                                L_DotYPos_02,
                                                                                                                align = 'horizontal' )

                                    else:
                                        L_SHUFFLE = nuke.toNode( L_SHUFFLE_NAME )

                                    #store previous shuffle dot
                                    P_L_SHUFFLE = L_SHUFFLE

                                    L_SHUFFLE_GRADE_NAME = compPrefix + "_" + L_CHANNEL + "_GRADE"
                                    if not nuke.exists( L_SHUFFLE_GRADE_NAME ):
                                        L_SHUFFLE_GRADE = createGrade( L_SHUFFLE_GRADE_NAME, L_CHANNEL + "_GRADE", [ L_SHUFFLE ] )

                                        L_SHUFFLE_GRADE.setXYpos( L_SHUFFLE_XPos,
                                                                ( L_SHUFFLE_YPos + L_SHUFFLE_H ) + L_SHUFFLE_Y_DIST / 2 )
                                    else:
                                        L_SHUFFLE_GRADE = nuke.toNode( L_SHUFFLE_GRADE_NAME )

                                    if nuke.exists( L_SHUFFLE_GRADE.name() ):
                                        L_SHUFFLE_GRADE_LIST.append( L_SHUFFLE_GRADE )

                            if L_SHUFFLE_GRADE_LIST != []:
                                if len( L_SHUFFLE_GRADE_LIST ) >= 2:
                                    for L_GRADE_COUNT, L_SHUFFLE_GRADE_NODE in enumerate( L_SHUFFLE_GRADE_LIST ):
                                        L_SHUFFLE_GRADE_NAME = L_SHUFFLE_GRADE_NODE.name()
                                        L_SHUFFLE_MERGE_NAME = L_SHUFFLE_GRADE_NAME.replace( "_GRADE", "_MERGE" )

                                        L_SHUFFLE_GRADE_W, L_SHUFFLE_GRADE_H, L_SHUFFLE_GRADE_XPos, L_SHUFFLE_GRADE_YPos = getSetVars( L_SHUFFLE_GRADE_NODE,
                                                                                                                                        1,
                                                                                                                                        None,
                                                                                                                                        None,
                                                                                                                                        None,
                                                                                                                                        align = 'vertical' )

                                        if not nuke.exists( L_SHUFFLE_MERGE_NAME ):
                                            if L_GRADE_COUNT != 0:
                                                L_SHUFFLE_MERGE = createMerge( L_SHUFFLE_MERGE_NAME, "GRADE_MERGE_%03d" % ( L_GRADE_COUNT ), "plus" )

                                                L_SHUFFLE_MERGE_W, L_SHUFFLE_MERGE_H, L_SHUFFLE_MERGE_XPos, L_SHUFFLE_MERGE_YPos = getSetVars( L_SHUFFLE_MERGE,
                                                                                    1,
                                                                                    None,
                                                                                    L_SHUFFLE_GRADE_XPos,
                                                                                    L_SHUFFLE_GRADE_YPos,
                                                                                    align = 'vertical' )

                                                if L_GRADE_COUNT == 1:
                                                    #connect L_SHUFFLE_MERGE to grades
                                                    setMergeInputs( L_SHUFFLE_MERGE,
                                                                  [ L_SHUFFLE_GRADE_NODE, P_L_SHUFFLE_GRADE_NODE ] )
                                                else:
                                                    #connect L_SHUFFLE_MERGE to grades
                                                    setMergeInputs( L_SHUFFLE_MERGE, [ P_L_SHUFFLE_MERGE, L_SHUFFLE_GRADE_NODE ] )
                                                #store previous L_SHUFFLE_MERGE
                                                P_L_SHUFFLE_MERGE = L_SHUFFLE_MERGE

                                        #store previous L_SHUFFLE_GRADE_NODE
                                        P_L_SHUFFLE_GRADE_NODE = L_SHUFFLE_GRADE_NODE

                                    else:
                                        L_SHUFFLE_MERGE = nuke.toNode( L_SHUFFLE_MERGE_NAME )

            #################################
            #################################
            #breakout CG
            #################################
            #################################

            if CG_PASSES == 1:
                if CG_CHANNEL_LIST != []:
                    GI_CHANNEL = None
                    DIFFUSE_CHANNEL = None
                    P_CG_SHUFFLE_DOT_01 = None
                    CURRENT_PASS_LIST = REF_CHANNEL_LIST + IGNORE_CHANNEL_LIST
                    if nuke.exists( CG_Dot_02.name() ):
                        for CG_count, CG_CHANNEL in enumerate( CG_CHANNEL_LIST ):
                            CG_DIFFUSE_MATCH = re.search( 'diffuse', CG_CHANNEL, re.IGNORECASE )
                            if CG_DIFFUSE_MATCH != None:
                                DIFFUSE_CHANNEL = CG_DIFFUSE_MATCH.group(0)
                            CG_GI_MATCH = re.search( 'gi', CG_CHANNEL, re.IGNORECASE )
                            if CG_GI_MATCH != None:
                                GI_CHANNEL = CG_GI_MATCH.group(0)

                            if CG_CHANNEL not in CURRENT_PASS_LIST:
                                if CG_CHANNEL != GI_CHANNEL:
                                    if CG_CHANNEL != DIFFUSE_CHANNEL:
                                        CG_PASS_LIST_02.append( CG_CHANNEL )

                        CG_PASS_LIST_01 = [ DIFFUSE_CHANNEL, GI_CHANNEL ]

                        CG_PASS_DICT_01 = shuffleFromList( compPrefix, CG_PASS_LIST_01, CG_Dot_02, CG_DotXPos_02, CG_DotYPos_02, useCount = True  )

                        if CG_PASS_DICT_01 != {}:
                            for CG_SHUFFLE_01_COUNT, ( CG_SHUFFLE_01, CG_SHUFFLE_VAL_LIST_01 ) in enumerate( CG_PASS_DICT_01.iteritems() ):
                                CG_SHUFFLE_DOT_NAME_01 = CG_SHUFFLE_01.name() + "_DOT_01"
                                CG_SHUFFLE_W, CG_SHUFFLE_H, CG_SHUFFLE_XPos, CG_SHUFFLE_YPos = CG_SHUFFLE_VAL_LIST_01
                                if not nuke.exists( CG_SHUFFLE_DOT_NAME_01 ):
                                    CG_SHUFFLE_DOT_01_inputList = [CG_Dot_02]
                                    CG_SHUFFLE_DOT_01 = createDot( CG_SHUFFLE_DOT_NAME_01, CG_SHUFFLE_DOT_01_inputList )
                                    CG_SHUFFLE_DOT_01.setXYpos( CG_SHUFFLE_XPos, CG_SHUFFLE_YPos + CG_SHUFFLE_H + UTIL_SHUFFLE_Y_DIST )
                                    CG_SHUFFLE_DOT_01_XPos, CG_SHUFFLE_DOT_01_YPos = getNodePos( CG_SHUFFLE_DOT_01 )

                                    if CG_SHUFFLE_01_COUNT != 0:
                                        # print CG_SHUFFLE_01_COUNT
                                        # print P_CG_SHUFFLE_DOT_01.name()
                                        CG_SHUFFLE_DOT_01.setInput( 0, P_CG_SHUFFLE_DOT_01 )

                                    #store previous shuffle dot
                                    P_CG_SHUFFLE_DOT_01 = CG_SHUFFLE_DOT_01

                                CG_COPY_NAME_01 = CG_SHUFFLE_01.name() + "_COPY_01"

                                if ( check_nodeExists( [ CG_SHUFFLE_DOT_01.name(), CG_SHUFFLE_01.name() ] ) ):
                                    if not nuke.exists( CG_COPY_NAME_01 ):
                                        CG_COPY_01 = nuke.nodes.Copy(
                                                                        name = CG_COPY_NAME_01,
                                                                        ypos = CG_SHUFFLE_YPos + CG_SHUFFLE_H + UTIL_SHUFFLE_Y_DIST * 2 ,
                                                                        xpos = CG_SHUFFLE_XPos,
                                                                        to0 = "rgba.alpha",
                                                                        from0 = "rgba.alpha" )
                                        CG_COPY_01_XPos, CG_COPY_01_YPos = getNodePos( CG_COPY_01 )

                                        CG_COPY_01.setInput( 1, CG_SHUFFLE_DOT_01 )
                                        CG_COPY_01.setInput( 0, CG_SHUFFLE_01 )

                                        #store previous shuffle dot
                                        P_CG_COPY_01 = CG_COPY_01

                                        CG_COPY_01_LIST.append( CG_COPY_01 )

                            CG_MERGE_DIV_NAME_01 = compPrefix + "_COPY_MERGE_01"
                            P_CG_MERGE_DIV_01 = None
                            if CG_COPY_01_LIST != []:
                                if CG_COPY_01_LIST >= 2:
                                    for CG_COPY_01_COUNT, CG_COPY_01_NODE in enumerate( CG_COPY_01_LIST ):
                                        if not nuke.exists( CG_MERGE_DIV_NAME_01 ):
                                            CG_COPY_01_XPos, CG_COPY_01_YPos = getNodePos( CG_COPY_01_NODE )
                                            CG_MERGE_DIV_01 = nuke.nodes.Merge2(
                                                                            name = CG_MERGE_DIV_NAME_01,
                                                                            ypos = CG_COPY_01_YPos + CG_SHUFFLE_H + UTIL_SHUFFLE_Y_DIST,
                                                                            xpos = CG_COPY_01_XPos,
                                                                            operation = "divide"
                                                                            )
                                            CG_MERGE_DIV_01_XPos, CG_MERGE_DIV_01_YPos = getNodePos( CG_MERGE_DIV_01 )

                                            #store previous shuffle dot
                                            P_CG_COPY_01_NODE = CG_COPY_01_NODE

                                        if CG_COPY_01_COUNT != 0:
                                            setMergeInputs( CG_MERGE_DIV_01,
                                                          [ P_CG_COPY_01_NODE, CG_COPY_01_NODE ] )



                        CG_PASS_DICT_02 = shuffleFromList( compPrefix, CG_PASS_LIST_02, CG_Dot_03, CG_DotXPos_03, CG_DotYPos_03, useCount = True  )

            #################################
            #################################
            #breakout UTIL
            #################################
            #################################

            if UTIL == 1:
                if UTIL_CHANNEL_LIST != []:
                    UTIL_PASS_DICT_01 = shuffleFromList( compPrefix, UTIL_CHANNEL_LIST, UTIL_Dot_01, UTIL_DotXPos_01, UTIL_DotYPos_01, useCount = False  )

        else:
            nuke.error( "Selected Node Is Not a Read Node" )
            nuke.message( "Selected Node Is Not a Read Node" )

    except ValueError as error:
        nuke.error( str( error ) )
        nuke.message( str( error ) )
