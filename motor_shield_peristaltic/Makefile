.PHONY: all part_lint validate split outputs
.SILENT:

PROJECT_FILE=motor_shield_peristaltic
PROJECT_NAME=SMPBR
BOARD_NAME=shield-peristaltic
COMPANY=TrendBit
DESIGNER=Petr_Malaník

all: part_lint validate split panel outputs

part_lint:
	resources/part_lint.sh -p pcb

validate:
	resources/validate.sh -p pcb -n $(PROJECT_NAME) -w

split:
	@echo "Split is not implemented yet, but use KiKit to split board into separate files."

panel:
	@echo "Panel is not implemented yet, but use KiKit to generate it based on json config file."

outputs: panel
	@echo "Outputs are not implemented yet, example in resources/prepare_manufacturing_files.sh"

kibot:
	PROJECT_NAME=$(PROJECT_NAME) PROJECT_FILE=$(PROJECT_FILE) BOARD_NAME=$(BOARD_NAME) COMPANY=$(COMPANY) DESIGNER=$(DESIGNER) pcb/kibot/kibot_resources/scripts/kibot_launch_in_docker.sh

clean:
	rm -rf pcb_output_data
