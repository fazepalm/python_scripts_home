import maya.cmds as cmds

vraySettings = { 'imageFormatStr': 'exr (multichannel)',
                'animType': 1,
                'samplerType' : 1,
                'aaFilterOn' : 0,
                'animBatchOnly': 1,
                'clearRVOn': 1,
                'sRGBOn': 1,
                'dmcMaxSubdivs': 20,
                'dmcThreshold': .015,
                'dmcs_adaptiveThreshold': .015,
                'dmcs_adaptiveMinSamples': 8,
                'cmap_adaptationOnly': 1,
                'cmap_type': 0,
                'cmap_gamma': 2.2,
                'cmap_affectSwatches': 1,
                'ddisplac_edgeLength': 1,
                'ddisplac_maxSubdivs': 4,
                'sys_rayc_dynMemLimit': 24000,
                'sys_regsgen_seqtype': 3,
                'globopt_geom_doHidden': 0,
                'stamp_on': 1,
                'stamp_text': "V-Ray for Maya %vrayversion | render time %rendertime | frame %frame | camera %camera | date %date | username %computername"
                }

for attr, value in vraySettings.iteritems():
    if 'text' not in attr and 'Str' not in attr:
        cmds.setAttr( 'vraySettings.' + attr, value )
    else:
        cmds.setAttr( 'vraySettings.' + attr, value, type = 'string' )
        