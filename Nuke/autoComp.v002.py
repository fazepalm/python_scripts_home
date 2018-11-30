###################################
import nuke
import re
from PySide import QtGui

LS_CHANNEL_LIST = []
MM_CHANNEL_LIST = []
MM_MERGE_LIST = []
L_SHUFFLE_GRADE_LIST = []
UTIL_CHANNEL_LIST = []
IGNORE_CHANNEL_LIST = []
REF_CHANNEL_LIST = []
MM_STR = "MM_"
L_STR = "L_"
L_SHUFFLE_Y_DIST = 100
L_SHUFFLE_X_DIST = 100
P_L_SHUFFLE = ""
C_Dist = 400
MM_SHUFFLE_DIST = 200
MM_SHUFFLE_SPACE = 10
UTIL_SHUFFLE_X_DIST = 100
UTIL_SHUFFLE_Y_DIST = 100
CG_SHUFFLE_X_DIST = 100
CG_SHUFFLE_Y_DIST = 100
MM = 0
LS = 0
UTIL = 0
CG_PASSES = 1

UTIL_NAME_LIST = [ 'ao', 'frensel', 'fresnel', 'uv', 'wpp', 'xyz', 'depth', 'velocity', 'normals' ]
REF_LIST = [ 'specular', 'lighting' ]
IGNORE_LIST = [ 'rgba' ]

def shuffleLayer( node, channel, shuffleName, shuffleLabel ):
    shuffleNode = nuke.nodes.Shuffle( name = shuffleName, label = shuffleLabel, inputs=[node] )
    shuffleNode['in'].setValue( channel )
    shuffleNode['postage_stamp'].setValue( True )
    return shuffleNode

def setShuffleValue( node, channel, value ):
    if nuke.exists( node.name() ):
        node[ channel ].setValue( value )

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

        if not nuke.exists( C_DotName ):
            C_Dot = nuke.nodes.Dot( inputs=[ node ], name = C_DotName )
            C_DotXPos, C_DotYPos = getNodePos( C_Dot )
#        else:
#            C_Dot = nuke.toNode( C_DotName )

        if not nuke.exists( LF_DotName ):
            LF_Dot = nuke.nodes.Dot( inputs=[ C_Dot ], name = LF_DotName, ypos = C_DotYPos, xpos = C_DotXPos - C_Dist )
            LF_DotXPos, LF_DotYPos = getNodePos( LF_Dot )
#        else:
#            LF_Dot = nuke.toNode( LF_DotName )

        if not nuke.exists( R_DotName ):
            R_Dot = nuke.nodes.Dot( inputs=[ C_Dot ], name = R_DotName, ypos = C_DotYPos, xpos = C_DotXPos + C_Dist )
            R_DotXPos, R_DotYPos = getNodePos( R_Dot )
#        else:
#            R_Dot = nuke.toNode( R_DotName )

        if not nuke.exists( CG_DotName_01 ):
            CG_Dot_01 = nuke.nodes.Dot( inputs=[ C_Dot ],
                                        name = CG_DotName_01,
                                        ypos = C_DotYPos + 100,
                                        xpos = C_DotXPos )
            CG_DotXPos_01, CG_DotYPos_01 = getNodePos( CG_Dot_01 )
#        else:
#            CG_Dot_01 = nuke.toNode( CG_DotName_01 )

        if not nuke.exists( MM_DotName ):
            MM_Dot = nuke.nodes.Dot( inputs=[ LF_Dot ], name = MM_DotName, ypos = LF_DotYPos + 100, xpos = LF_DotXPos )
            MM_DotXPos, MM_DotYPos = getNodePos( MM_Dot )
#        else:
#            MM_Dot = nuke.toNode( MM_DotName )

        if not nuke.exists( L_DotName_01 ):
            L_Dot_01 = nuke.nodes.Dot( inputs=[ CG_Dot_01 ],
                                       name = L_DotName_01,
                                       ypos = CG_DotYPos_01,
                                       xpos = CG_DotXPos_01 - 300 )
            L_DotXPos_01, L_DotYPos_01 = getNodePos( L_Dot_01 )
#        else:
#            L_Dot_01 = nuke.toNode( L_DotName_01 )

        if not nuke.exists( L_DotName_02 ):
            if nuke.exists( L_DotName_01 ):
                L_Dot_02 = nuke.nodes.Dot( inputs=[ L_Dot_01 ],
                                            name = L_DotName_02,
                                            xpos = L_DotXPos_01,
                                            ypos = L_DotYPos_01 + L_SHUFFLE_Y_DIST )
                L_DotXPos_02, L_DotYPos_02 = getNodePos( L_Dot_02 )
#        else:
#            L_Dot_02 = nuke.toNode( L_DotName_02 )

        if not nuke.exists( CG_DotName_02 ):
            if nuke.exists( L_Dot_02.name() ):
                CG_Dot_02 = nuke.nodes.Dot( inputs=[ L_Dot_02 ], name = CG_DotName_02, ypos = L_DotYPos_02 + 300, xpos = L_DotXPos_02 )
                CG_DotXPos_02, CG_DotYPos_02 = getNodePos( CG_Dot_02 )
#        else:
#            CG_Dot_02 = nuke.toNode( CG_DotName_02 )

        if not nuke.exists( CG_DotName_03 ):
            if nuke.exists( CG_Dot_02.name() ):
                CG_Dot_03 = nuke.nodes.Dot( inputs=[ CG_Dot_02 ],
                                            name = CG_DotName_03,
                                            ypos = CG_DotYPos_02 + 300,
                                            xpos = CG_DotXPos_02 )
                CG_DotXPos_03, CG_DotYPos_03 = getNodePos( CG_Dot_03 )
#        else:
#            CG_Dot_03 = nuke.toNode( CG_DotName_03 )

        if not nuke.exists( UTIL_DotName_01 ):
            UTIL_Dot_01 = nuke.nodes.Dot( inputs=[ R_Dot ], name = UTIL_DotName_01, ypos = R_DotYPos + 300, xpos = R_DotXPos )
            UTIL_DotXPos_01, UTIL_DotYPos_01 = getNodePos( UTIL_Dot_01 )
        else:
            UTIL_Dot_01 = nuke.toNode( UTIL_DotName_01 )

        #breakout MM
        if MM == 1:
            if nuke.exists( MM_DotName ):
                shuffleChannels = [ 'red', 'green', 'blue', 'alpha' ]
                for count, MM_CHANNEL in enumerate( MM_CHANNEL_LIST ):
                    if count < 1:
                        MM_SHUFFLE_DOT_NAME = compPrefix + "_" + MM_CHANNEL
                        if not nuke.exists( MM_SHUFFLE_DOT_NAME ):
                            MM_SHUFFLE_DOT = nuke.nodes.Dot(
                                                            name = MM_SHUFFLE_DOT_NAME,
                                                            ypos = MM_DotYPos,
                                                            xpos = MM_DotXPos - ( ( count + 1 ) * MM_SHUFFLE_DIST  ) )

                            MM_SHUFFLE_DOT_XPos, MM_SHUFFLE_DOT_YPos = getNodePos( MM_SHUFFLE_DOT )
                        else:
                            MM_SHUFFLE_DOT = nuke.toNode( MM_SHUFFLE_DOT_NAME )

                        MM_SHUFFLE_NAME_R = compPrefix + "_" + MM_CHANNEL + "_R"
                        MM_SHUFFLE_NAME_G = compPrefix + "_" + MM_CHANNEL + "_G"
                        MM_SHUFFLE_NAME_B = compPrefix + "_" + MM_CHANNEL + "_B"

                        if count == 0:
                           MM_SHUFFLE_DOT.setInput( 0, MM_Dot )
                        else:
                            if nuke.exists( P_MM_SHUFFLE_DOT.name() ):
                                MM_SHUFFLE_DOT.setInput( 0, P_MM_SHUFFLE_DOT )

                        #store previous shuffle dot
                        P_MM_SHUFFLE_DOT = MM_SHUFFLE_DOT

                        if not nuke.exists( MM_SHUFFLE_NAME_R ):
                            MM_SHUFFLE_R = shuffleLayer( MM_SHUFFLE_DOT, MM_CHANNEL, MM_SHUFFLE_NAME_R, MM_CHANNEL + "_R" )
                            MM_SHUFFLE_R_H = MM_SHUFFLE_R.screenHeight() / 2
                            for sChannel in shuffleChannels:
                                setShuffleValue( MM_SHUFFLE_R, sChannel, "red" )
    #                    else:
    #                        MM_SHUFFLE_R = nuke.toNode( MM_SHUFFLE_NAME_R )

                        if not nuke.exists( MM_SHUFFLE_NAME_G ):
                            MM_SHUFFLE_G = shuffleLayer( MM_SHUFFLE_R, MM_CHANNEL, MM_SHUFFLE_NAME_G, MM_CHANNEL + "_G" )
                            MM_SHUFFLE_G_XPos, MM_SHUFFLE_G_YPos = getNodePos( MM_SHUFFLE_G )
                            MM_SHUFFLE_G.setXYpos( MM_SHUFFLE_G_XPos, ( MM_SHUFFLE_G_YPos + MM_SHUFFLE_R_H ) + MM_SHUFFLE_SPACE )
                            MM_SHUFFLE_G_H = MM_SHUFFLE_G.screenHeight() / 2
                            for sChannel in shuffleChannels:
                                setShuffleValue( MM_SHUFFLE_G, sChannel, "green" )
    #                    else:
    #                        MM_SHUFFLE_G = nuke.toNode( MM_SHUFFLE_NAME_G )

                        if not nuke.exists( MM_SHUFFLE_NAME_B ):
                            MM_SHUFFLE_B = shuffleLayer( MM_SHUFFLE_G, MM_CHANNEL, MM_SHUFFLE_NAME_B, MM_CHANNEL + "_B" )
                            MM_SHUFFLE_B_XPos, MM_SHUFFLE_B_YPos = getNodePos( MM_SHUFFLE_B )
                            MM_SHUFFLE_B.setXYpos( MM_SHUFFLE_B_XPos, ( MM_SHUFFLE_B_YPos + MM_SHUFFLE_G_H ) + MM_SHUFFLE_SPACE )
                            MM_SHUFFLE_B_H = MM_SHUFFLE_B.screenHeight() / 2
                            for sChannel in shuffleChannels:
                                setShuffleValue( MM_SHUFFLE_B, sChannel, "blue" )
    #                    else:
    #                        MM_SHUFFLE_B = nuke.toNode( MM_SHUFFLE_NAME_B )

                        if nuke.exists( MM_SHUFFLE_R.name() ) and nuke.exists( MM_SHUFFLE_G.name() ) and nuke.exists( MM_SHUFFLE_B.name() ):
                            MM_SHUFFLE_LIST = [ MM_SHUFFLE_R, MM_SHUFFLE_B, MM_SHUFFLE_G ]
                            MM_MERGE_NAME = compPrefix + "_" + MM_CHANNEL + "_MERGE"
                            if not nuke.exists( MM_MERGE_NAME ):
                                MM_MERGE = nuke.nodes.Merge2( name = MM_MERGE_NAME,
                                                            label = MM_CHANNEL + "_MERGE",
                                                            operation = "plus" )

                            else:
                                MM_MERGE = nuke.toNode( MM_MERGE_NAME )

                            #connect shuffles to first merge
                            setMergeInputs( MM_MERGE, MM_SHUFFLE_LIST )

                            MM_MERGE_XPos, MM_MERGE_YPos = getNodePos( MM_MERGE )
                            MM_MERGE_H = MM_MERGE.screenHeight() / 2
                            MM_MERGE_LIST.append( MM_MERGE )

                        if MM_MERGE_LIST != []:
                            if len( MM_MERGE_LIST ) > 0:
                                MM_MERGE_NAME_END = compPrefix + "_MM_MERGE_END"
                                if not nuke.exists( MM_MERGE_NAME_END ):
                                    MM_MERGE_END = nuke.nodes.Merge2( name = MM_MERGE_NAME_END,
                                                                label = "MM_MERGE_END",
                                                                operation = "plus" )

                                    MM_MERGE_END.setXYpos( MM_MERGE_XPos, ( MM_MERGE_YPos + MM_MERGE_H ) + 250 )
                            else:
                                MM_MERGE_END = nuke.toNode( MM_MERGE_NAME_END )

                            #connect shuffle merge's to final merge node
                            setMergeInputs( MM_MERGE_END, MM_MERGE_LIST )
        #breakout LS
        if LS == 1:
            if LS_CHANNEL_LIST != []:
                if nuke.exists( CG_Dot_01.name() ):
                    if nuke.exists( L_Dot_02.name() ):
                        for L_count, L_CHANNEL in enumerate( LS_CHANNEL_LIST ):
                            if L_count < 3:
                                L_SHUFFLE_NAME = compPrefix + "_" + L_CHANNEL
                                if not nuke.exists( L_SHUFFLE_NAME ):
                                    if L_count == 0:
                                        L_SHUFFLE = shuffleLayer( L_Dot_02, L_CHANNEL, L_SHUFFLE_NAME, L_CHANNEL )

                                    else:
                                        if nuke.exists( P_L_SHUFFLE.name() ):
                                            L_SHUFFLE = shuffleLayer( P_L_SHUFFLE, L_CHANNEL, L_SHUFFLE_NAME, L_CHANNEL )

                                    L_SHUFFLE_W = L_SHUFFLE.screenWidth()
                                    L_SHUFFLE_H = L_SHUFFLE.screenHeight() / 2
                                    L_SHUFFLE.setXYpos( ( L_DotXPos_02 + L_SHUFFLE_W ) + ( L_SHUFFLE_X_DIST * ( L_count + 1 ) ),
                                                          L_DotYPos_02 - L_SHUFFLE_H   )
                                    L_SHUFFLE_XPos, L_SHUFFLE_YPos = getNodePos( L_SHUFFLE )

                                else:
                                    L_SHUFFLE = nuke.toNode( L_SHUFFLE_NAME )

                                #store previous shuffle dot
                                P_L_SHUFFLE = L_SHUFFLE

                                L_SHUFFLE_GRADE_NAME = compPrefix + "_" + L_CHANNEL + "_GRADE"
                                if not nuke.exists( L_SHUFFLE_GRADE_NAME ):
                                    L_SHUFFLE_GRADE = nuke.nodes.Grade( name = L_SHUFFLE_GRADE_NAME,
                                                                        label = L_CHANNEL + "_GRADE",
                                                                        inputs = [ L_SHUFFLE ]  )
                                    L_SHUFFLE_GRADE.setXYpos( L_SHUFFLE_XPos,
                                                            ( L_SHUFFLE_YPos + L_SHUFFLE_H ) + L_SHUFFLE_Y_DIST / 2 )
#                                else:
#                                    L_SHUFFLE_GRADE = nuke.toNode( L_SHUFFLE_GRADE_NAME )

                                if nuke.exists( L_SHUFFLE_GRADE.name() ):
                                    L_SHUFFLE_GRADE_LIST.append( L_SHUFFLE_GRADE )

                        if L_SHUFFLE_GRADE_LIST != []:
                            if len( L_SHUFFLE_GRADE_LIST ) >= 2:
                                for L_GRADE_COUNT, L_SHUFFLE_GRADE_NODE in enumerate( L_SHUFFLE_GRADE_LIST ):
                                    L_SHUFFLE_GRADE_NAME = L_SHUFFLE_GRADE_NODE.name()
                                    L_SHUFFLE_MERGE_NAME = L_SHUFFLE_GRADE_NAME.replace( "_GRADE", "_MERGE" )
                                    L_SHUFFLE_GRADE_XPos, L_SHUFFLE_GRADE_YPos = getNodePos( L_SHUFFLE_GRADE_NODE )
                                    L_SHUFFLE_GRADE_W = L_SHUFFLE_GRADE_NODE.screenWidth()
                                    L_SHUFFLE_GRADE_H = L_SHUFFLE_GRADE_NODE.screenHeight() / 2


                                    if not nuke.exists( L_SHUFFLE_MERGE_NAME ):
                                        if L_GRADE_COUNT != 0:
                                            L_SHUFFLE_MERGE = nuke.nodes.Merge2( name = L_SHUFFLE_MERGE_NAME, operation = "plus" )
                                            L_SHUFFLE_MERGE.setXYpos( L_SHUFFLE_GRADE_XPos,
                                                                    ( L_SHUFFLE_GRADE_YPos - L_SHUFFLE_GRADE_H ) + L_SHUFFLE_Y_DIST / 2 )

                                            L_SHUFFLE_MERGE_XPos, L_SHUFFLE_MERGE_YPos = getNodePos( L_SHUFFLE_MERGE )

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

#                                else:
#                                    L_SHUFFLE_MERGE = nuke.toNode( L_SHUFFLE_MERGE_NAME )

        #breakout CG PASSES
        if CG_PASSES == 1:
            if CG_CHANNEL_LIST != []:
                print CG_Dot_02
                if nuke.exists( CG_Dot_02.name() ):
                    for CG_count, CG_CHANNEL in enumerate( CG_CHANNEL_LIST ):
                        CG_SHUFFLE_NAME = compPrefix + "_" + CG_CHANNEL
                        if not nuke.exists( CG_SHUFFLE_NAME ):
                            if re.search( 'diffuse', CG_CHANNEL, re.IGNORECASE  ):
                                CG_SHUFFLE = shuffleLayer( CG_Dot_02, CG_CHANNEL, CG_SHUFFLE_NAME, CG_CHANNEL )
                                CG_D_SHUFFLE = CG_SHUFFLE
                            if re.search( 'gi', CG_CHANNEL, re.IGNORECASE  ):
                                if nuke.exists( CG_D_SHUFFLE.name() ):
                                    CG_SHUFFLE = shuffleLayer( CG_D_SHUFFLE, CG_CHANNEL, CG_SHUFFLE_NAME, CG_CHANNEL )
                                else:
                                    CG_SHUFFLE = shuffleLayer( CG_Dot_02, CG_CHANNEL, CG_SHUFFLE_NAME, CG_CHANNEL )

#                            if nuke.exists( CG_SHUFFLE.name() ):
#                                CG_SHUFFLE_W = CG_SHUFFLE.screenWidth()
#                                CG_SHUFFLE_H = CG_SHUFFLE.screenHeight() / 2
#                                CG_SHUFFLE_X_VAL = ( CG_DotXPos_02 + CG_SHUFFLE_W ) + ( CG_SHUFFLE_X_DIST * ( CG_count + 1 ) )
#                                CG_SHUFFLE.setXYpos( CG_SHUFFLE_X_VAL, CG_DotYPos_02 - CG_SHUFFLE_H )
#                                CG_SHUFFLE_XPos, CG_SHUFFLE_YPos = getNodePos( CG_SHUFFLE )
#
#                        else:
#                            CG_SHUFFLE = nuke.toNode( CG_SHUFFLE_NAME )
#
#                        #store previous shuffle dot
#                        P_CG_SHUFFLE = CG_SHUFFLE

        #breakout UTIL
        if UTIL == 1:
            if UTIL_CHANNEL_LIST != []:
                if nuke.exists( R_Dot.name() ):
                    if nuke.exists( UTIL_Dot_01.name() ):
                        for UTIL_count, UTIL_CHANNEL in enumerate( UTIL_CHANNEL_LIST ):
                            UTIL_SHUFFLE_NAME = compPrefix + "_" + UTIL_CHANNEL
                            if not nuke.exists( UTIL_SHUFFLE_NAME ):
                                if UTIL_count == 0:
                                    UTIL_SHUFFLE = shuffleLayer( UTIL_Dot_01, UTIL_CHANNEL, UTIL_SHUFFLE_NAME, UTIL_CHANNEL )

                                else:
                                    if nuke.exists( P_UTIL_SHUFFLE.name() ):
                                        UTIL_SHUFFLE = shuffleLayer( P_UTIL_SHUFFLE, UTIL_CHANNEL, UTIL_SHUFFLE_NAME, UTIL_CHANNEL )

                                UTIL_SHUFFLE_W = UTIL_SHUFFLE.screenWidth()
                                UTIL_SHUFFLE_H = UTIL_SHUFFLE.screenHeight() / 2
                                UTIL_SHUFFLE.setXYpos( ( UTIL_DotXPos_01 + UTIL_SHUFFLE_W ) + ( UTIL_SHUFFLE_X_DIST *
                                                       ( UTIL_count + 1 ) ), UTIL_DotYPos_01 - UTIL_SHUFFLE_H )
                                UTIL_SHUFFLE_XPos, UTIL_SHUFFLE_YPos = getNodePos( UTIL_SHUFFLE )

                            else:
                                UTIL_SHUFFLE = nuke.toNode( UTIL_SHUFFLE_NAME )

                            #store previous shuffle dot
                            P_UTIL_SHUFFLE = UTIL_SHUFFLE

    else:
        nuke.error( "Selected Node Is Not a Read Node" )
        nuke.message( "Selected Node Is Not a Read Node" )

except ValueError as error:
    nuke.error( str( error ) )
    nuke.message( str( error ) )
