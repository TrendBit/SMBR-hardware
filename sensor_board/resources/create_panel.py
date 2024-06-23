from kikit import panelize_ui_impl as ki
from kikit.units import mm, deg
from kikit.panelize import Panel, BasicGridPosition, Origin
from pcbnewTransition.pcbnew import LoadBoard, VECTOR2I
from pcbnewTransition import pcbnew
from itertools import chain


############### Custom config
board1_path = "../boards/SM1.kicad_pcb"
board2_path = "../boards/SM2.kicad_pcb"
board3_path = "../boards/SM3.kicad_pcb"
output_path = "../boards/panel.kicad_pcb"

board_spacing = 3*mm

################ KiKit Panel Config (Only deviations from default)

framing={
		"type": "frame", #only rail on top and bottom
		"vspace" : "3mm", # space between board and rail
		"hspace" : "3mm", # space between board and rail
		"width": "5mm", # Width of the rail
		"mintotalheight": "70mm",
		"mintotalwidth": "70mm",
		"fillet": "2.5mm",
	}

cuts =  {
		"type": "vcuts"
	}
tabs = { #Add tabs between board and board as well as board and rail
		"type":"annotation"
	}
tooling = {
        "type": "3hole",
        "hoffset": "2.5mm",
        "voffset": "2.5mm",
        "size": "1.152mm",
		"paste": False,
		"soldermaskmargin": "1.3mm"
    }

fiducials = {
		"type": "4fid",
		"hoffset" : "4mm",
		"voffset" : "4mm",
		"coppersize" : "1mm",
		"opening"	: "2mm",
		"paste": False
}

post = {
        "millradius": "1mm",
}

# Obtain full config by combining above with default
preset = ki.obtainPreset([], tabs=tabs, cuts=cuts, framing=framing, tooling=tooling, fiducials=fiducials ,post=post)



################ Adjusted `panelize_ui#doPanelization`

# Prepare
board1 = LoadBoard(board1_path)
board2 = LoadBoard(board2_path)
board3 = LoadBoard(board3_path)
panel = Panel(output_path)


panel.inheritDesignSettings(board1)
panel.inheritProperties(board1)
panel.inheritTitleBlock(board1)


###### Manually build layout. Inspired by `panelize_ui_impl#buildLayout`
sourceArea1 = ki.readSourceArea(preset["source"], board1)
sourceArea2 = ki.readSourceArea(preset["source"], board2)
sourceArea3 = ki.readSourceArea(preset["source"], board3)

substrateCount = len(panel.substrates) # Store number of previous boards (probably 0)
# Prepare renaming nets and references
netRenamer = lambda x, y: "Board_{n}-{orig}".format(n=x, orig=y)
refRenamer = lambda x, y: "Board_{n}-{orig}".format(n=x, orig=y)

# Actually place the individual boards
# Use existing grid positioner
# Place two boards above each other
panelOrigin = VECTOR2I(0,0)

board1_voffset = 0*mm
board2_voffset = 49*mm
board3_voffset = 71*mm

set_hoffset = 45*mm

board1_hoffset = int(0*mm)
board2_hoffset = int(0*mm)
board3_hoffset = int(7.35*mm)

h_boards_count = 6

for i in range (0, h_boards_count):
	current_set_hoffset = i*set_hoffset
	panel.appendBoard(board1_path, panelOrigin + VECTOR2I(current_set_hoffset + board1_hoffset, board1_voffset), origin=Origin.Center, sourceArea=sourceArea1, netRenamer=netRenamer, refRenamer=refRenamer)
	panel.appendBoard(board2_path, panelOrigin + VECTOR2I(current_set_hoffset + board2_hoffset, board2_voffset), origin=Origin.Center, sourceArea=sourceArea2, netRenamer=netRenamer, refRenamer=refRenamer,  inheritDrc=False, rotationAngle=90*deg)
	panel.appendBoard(board3_path, panelOrigin + VECTOR2I(current_set_hoffset + board3_hoffset, board3_voffset), origin=Origin.Center, sourceArea=sourceArea3, netRenamer=netRenamer, refRenamer=refRenamer,  inheritDrc=False)


substrates = panel.substrates[substrateCount:] # Collect set of newly added boards

# Prepare frame and partition
framingSubstrates = ki.dummyFramingSubstrate(substrates, preset)
panel.buildPartitionLineFromBB(framingSubstrates)
backboneCuts = ki.buildBackBone(preset["layout"], panel, substrates, preset)


######## --------------------- Continue doPanelization

tabCuts = ki.buildTabs(preset, panel, substrates, framingSubstrates)

frameCuts = ki.buildFraming(preset, panel)


ki.buildTooling(preset, panel)
ki.buildFiducials(preset, panel)
for textSection in ["text", "text2", "text3", "text4"]:
	ki.buildText(preset[textSection], panel)
ki.buildPostprocessing(preset["post"], panel)

ki.makeTabCuts(preset, panel, tabCuts)
ki.makeOtherCuts(preset, panel, chain(backboneCuts, frameCuts))


ki.buildCopperfill(preset["copperfill"], panel)

ki.setStackup(preset["source"], panel)
ki.setPageSize(preset["page"], panel, board1)
ki.positionPanel(preset["page"], panel)

ki.runUserScript(preset["post"], panel)

ki.buildDebugAnnotation(preset["debug"], panel)

panel.save(reconstructArcs=preset["post"]["reconstructarcs"],
		   refillAllZones=preset["post"]["refillzones"])
