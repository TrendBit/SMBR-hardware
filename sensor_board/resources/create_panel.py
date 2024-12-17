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
		"hbackbone": "5mm",
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
netRenamer = lambda x, y: "{orig}-{n}".format(n=x, orig=y)
refRenamer = lambda x, y: "{orig}-{n}".format(n=x, orig=y)

# Actually place the individual boards
# Use existing grid positioner
# Place two boards above each other
panelOrigin = VECTOR2I(0,0)

# Panel rotation option (-90, 0, 90)
panel_rotation = 0  # Set to desired rotation angle (e.g., -90, 0, or 90)

h_boards_count = 4

# Increasing vertical board count can cause issues with CPL file for JLCPCB
v_boards_count = 1

board1_voffset = 0 * mm
board2_voffset = 49 * mm
board3_voffset = 71 * mm

set_hoffset = 45 * mm
set_voffset = 117 * mm

board1_hoffset = int(0 * mm)
board2_hoffset = int(0 * mm)
board3_hoffset = int(7.35 * mm)

# Function to rotate offsets
def rotate_offsets(h_offset, v_offset, angle):
    """Rotate offsets for any board based on panel rotation."""
    if angle == 90:
        return v_offset, -h_offset  # Swap and flip horizontal
    elif angle == -90:
        return -v_offset, h_offset  # Swap and flip vertical
    else:
        return h_offset, v_offset  # No rotation


# Iterate through vertical and horizontal boards
for v in range(v_boards_count):
    for h in range(h_boards_count):
        # Calculate set offsets
        if panel_rotation == 90:
            # Swap dimensions for 90° rotation
            current_set_hoffset = v * set_voffset
            current_set_voffset = h * set_hoffset
        elif panel_rotation == -90:
            # Swap dimensions for -90° rotation (reverse vertical order)
            current_set_hoffset = (v_boards_count - 1 - v) * set_voffset
            current_set_voffset = h * set_hoffset
        else:
            # Default layout (no rotation)
            current_set_hoffset = h * set_hoffset
            current_set_voffset = v * set_voffset

        # Rotate offsets for each board
        b1_hoffset, b1_voffset = rotate_offsets(board1_hoffset, board1_voffset, panel_rotation)
        b2_hoffset, b2_voffset = rotate_offsets(board2_hoffset, board2_voffset, panel_rotation)
        b3_hoffset, b3_voffset = rotate_offsets(board3_hoffset, board3_voffset, panel_rotation)

        # Calculate final positions
        pos1 = (current_set_hoffset + b1_hoffset, current_set_voffset + b1_voffset)
        pos2 = (current_set_hoffset + b2_hoffset, current_set_voffset + b2_voffset)
        pos3 = (current_set_hoffset + b3_hoffset, current_set_voffset + b3_voffset)

        # Add boards to the panel
        # Board 1: Rotate according to panel_rotation
        panel.appendBoard(
            board1_path,
            panelOrigin + VECTOR2I(*pos1),
            origin=Origin.Center,
            sourceArea=sourceArea1,
            netRenamer=netRenamer,
            refRenamer=refRenamer,
            rotationAngle=panel_rotation * deg,
        )

        # Board 2: Always rotated 90° plus any additional panel_rotation
        panel.appendBoard(
            board2_path,
            panelOrigin + VECTOR2I(*pos2),
            origin=Origin.Center,
            sourceArea=sourceArea2,
            netRenamer=netRenamer,
            refRenamer=refRenamer,
            inheritDrc=False,
            rotationAngle=(panel_rotation + 90) * deg,
        )

        # Board 3: Rotate according to panel_rotation
        panel.appendBoard(
            board3_path,
            panelOrigin + VECTOR2I(*pos3),
            origin=Origin.Center,
            sourceArea=sourceArea3,
            netRenamer=netRenamer,
            refRenamer=refRenamer,
            inheritDrc=False,
            rotationAngle=panel_rotation * deg,
        )

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
