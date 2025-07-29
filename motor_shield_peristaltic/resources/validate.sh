#!/bin/bash

# Default values
PROJECT_NAME=""
PROJECT_PATH="./"  # Default to current directory
ENABLE_WARNING=false  # Default to no warning

# Parse command-line arguments
while getopts "p:n:w" opt; do
    case $opt in
        p)
            PROJECT_PATH="$OPTARG"  # Set project path from argument
            ;;
        n)
            PROJECT_NAME="$OPTARG"  # Set project name from argument
            ;;
        w)
            ENABLE_WARNING=true  # Enable -w for KiCad CLI
            ;;
        *)
            echo "Usage: $0 [-p path] [-n project_name] [-w]"
            exit 1
            ;;
    esac
done

# Ensure the project path ends with a slash
if [[ "${PROJECT_PATH}" != */ ]]; then
    PROJECT_PATH="${PROJECT_PATH}/"
fi

# If the project name is not provided, use the last part of the project path as the name
if [[ "$PROJECT_NAME" == "" ]]; then
    PROJECT_NAME=$(basename "$PROJECT_PATH")
fi

# Define color codes
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
NC="\e[0m" # No color

# Function to count ERC errors from a JSON file using jq
count_erc_errors() {
    local file="$1"
    local violations_sum=$(jq "[.sheets[].violations | length] | add" "$file")
    echo $violations_sum
}

# Function to count DRC errors from a JSON file using jq
count_drc_errors() {
    local file="$1"
    local errors_sum=$(jq "[.schematic_parity, .unconnected_items, .violations] | map(length) | add" "$file")
    echo $errors_sum
}

# Function to run KiCad ERC and return the exit code, suppressing output
run_erc() {
    echo -e "${BLUE}--- Electrical rule check ---${NC}"
    if $ENABLE_WARNING; then
        kicad-cli sch erc "$PROJECT_NAME.kicad_sch" --severity-error --severity-warning --exit-code-violations &>/dev/null
    else
        kicad-cli sch erc "$PROJECT_NAME.kicad_sch" --severity-error --exit-code-violations &>/dev/null
    fi
}

# Function to process ERC errors
process_erc_errors() {
    local exit_code="$1"
    local file="$2"

    if [[ $exit_code -eq 5 ]]; then
        echo -e "${RED}Electrical rule check failed!${NC}"
        cat "$PROJECT_NAME-erc.rpt"

        if $ENABLE_WARNING; then
            kicad-cli sch erc "$PROJECT_NAME.kicad_sch" --severity-error --severity-warning --exit-code-violations --format json &>/dev/null
        else
            kicad-cli sch erc "$PROJECT_NAME.kicad_sch" --severity-error --exit-code-violations --format json &>/dev/null
        fi

        ERC_ERRORS=$(count_erc_errors "$file")
        rm -f $file
    elif [[ $exit_code -eq 0 ]]; then
        ERC_ERRORS=0
    else
        echo -e "${RED}Unexpected exit code from ERC: $exit_code${NC}"
        exit 1
    fi
}

# Function to run KiCad DRC and return the exit code, suppressing output
run_drc() {
    echo -e "${BLUE}--- Design rule check ---${NC}"
    kicad-cli pcb drc "$PROJECT_NAME.kicad_pcb" --severity-error --severity-warning --all-track-errors --schematic-parity --exit-code-violations &>/dev/null
}

# Function to process DRC errors
process_drc_errors() {
    local exit_code="$1"
    local file="$2"

    if [[ $exit_code -eq 5 ]]; then
        echo -e "${RED}Design rule check failed!${NC}"
        cat "$PROJECT_NAME-drc.rpt"

        kicad-cli pcb drc "$PROJECT_NAME.kicad_pcb" --severity-error --severity-warning --all-track-errors --schematic-parity --exit-code-violations --format json &>/dev/null
        DRC_ERRORS=$(count_drc_errors "$file")
        rm -f $file
    elif [[ $exit_code -eq 0 ]]; then
        DRC_ERRORS=0
    else
        echo -e "${RED}Unexpected exit code from DRC: $exit_code${NC}"
        exit 1
    fi
}

# Function to calculate total errors and exit with color output
calculate_total_errors() {
    local drc_errors="$1"
    local erc_errors="$2"

    TOTAL_ERRORS=$((drc_errors + erc_errors))

    if [[ $TOTAL_ERRORS -gt 0 ]]; then
        echo -e "${RED}Total errors found: $TOTAL_ERRORS (Schema: $erc_errors, PCB: $drc_errors)${NC}"
        exit $TOTAL_ERRORS
    else
        echo -e "${GREEN}Total errors found: $TOTAL_ERRORS (Schema: $erc_errors, PCB: $drc_errors)${NC}"
        exit 0
    fi
}

# Main function to handle the checks and error counting
main() {
    # Change to the project path
    cd "$PROJECT_PATH" || { echo "Failed to change directory to $PROJECT_PATH"; exit 1; }

    run_erc
    ERC_EXIT_CODE=$?
    process_erc_errors $ERC_EXIT_CODE "$PROJECT_NAME-erc.json"

    run_drc
    DRC_EXIT_CODE=$?
    process_drc_errors $DRC_EXIT_CODE "$PROJECT_NAME-drc.json"

    rm "$PROJECT_NAME-drc.rpt"
    rm "$PROJECT_NAME-erc.rpt"

    calculate_total_errors $DRC_ERRORS $ERC_ERRORS
}

# Run the main function
main
