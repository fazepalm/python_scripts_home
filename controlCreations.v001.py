import maya.cmds as cmds
ctrlName = "test_01"
ctrlScale = 2
ctrlName_scale = 5
# ctrlBox = cmds.nurbsSquare( c = (0, 0, 0), nr = (0, 1, 0), sl1 = 1, sl2 = 1, sps = 1, d = 3, ch = 1)
# cmds.scale(8, 1, 1, ctrlBox, r = True )
# if ctrlBox:
#     ctrlBox = ctrlBox[0]
# curve_01, curve_02, curve_03, curve_04 = cmds.listRelatives(ctrlBox, children = True)
# cmds.attachCurve(curve_01, curve_02, curve_03, curve_04, ch = 1, rpo = 0, kmk = 1,
#                  m = 0, bb = 0.5, bki = 0, p = 0.1)
# cmds.delete(ctrlBox, constructionHistory = 1)
# cmds.delete(ctrlBox)

# midCtrl = cmds.curve( degree = 1,\
#             knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],\
#             point = [(-2, 0, -2),\
#                      (-2, 0, -3),\
#                      (2, 0, -3),\
#                      (2, 0, -2),\
#                      (3, 0, -2),\
#                      (3, 0, 2),\
#                      (2, 0, 2),\
#                      (2, 0, 3),\
#                      (-2, 0, 3),\
#                      (-2, 0, 2),\
#                      (-3, 0, 2),\
#                      (-3, 0, -2),\
#                      (-2, 0, -2)]\
#           )
# cmds.scale(.25, .25, .25, midCtrl, r = True )
# cmds.move(-3.1, 0, 0, midCtrl, r = True, os = True, wd = True )
ctrl_curves = cmds.textCurves( f='Times-Roman', t=ctrlName )
ctrl_curves_str = cmds.listRelatives(ctrl_curves, children = True)
cmds.parent(ctrl_curves_str, r = True, s = True)

cmds.scale(ctrlName_scale, ctrlName_scale, ctrlName_scale, ctrl_curves, r = True)