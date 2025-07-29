.PHONY: all part_lint validate outputs
.SILENT:

PROJECT_FILE=pump_board
PROJECT_NAME=SMPBR
BOARD_NAME=Pump_board
COMPANY=TrendBit
DESIGNER=Petr_Malaník

all: part_lint validate outputs

part_lint:
	resources/part_lint.sh -p pcb

validate:
	resources/validate.sh -p pcb -n $(PROJECT_FILE) -w

outputs:
	PROJECT_FILE=$(PROJECT_FILE) resources/prepare_manufacturing_files.sh

kibot:
	PROJECT_NAME=$(PROJECT_NAME) PROJECT_FILE=$(PROJECT_FILE) BOARD_NAME=$(BOARD_NAME) COMPANY=$(COMPANY) DESIGNER=$(DESIGNER) pcb/kibot/kibot_resources/scripts/kibot_launch_in_docker.sh

clean:
	rm -rf pcb_output_data

clean_template:
	rm -rf 3d
	rm -rf images
	rm -rf pcb_output_data
	rm -rf pcb/TrendBit_template-backups
	rm -f pcb/fp-info-cache
	rm -f pcb/TrendBit_template.xml
	rm -f pcb/*-bak
	rm -f pcb/*.lck
	rm -f pcb/kibot_*
	rm -f TrendBit_template-schematic.pdf
	rm -f index.html
