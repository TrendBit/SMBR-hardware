#!/bin/bash

REPO_URL="https://github.com/TheColonelYoung/jlcpcb-partlint.git"
TARGET_DIR="./resources/jlcpcb_partlint"
REPORT_FILE="partlint_report.txt"
QUIET_MODE=false

# Parse arguments
for arg in "$@"; do
    case "$arg" in
        -q) QUIET_MODE=true ;;
        *) PROJECT_DIR="$arg" ;;
    esac
done

# Check if project location is provided
if [ -z "$PROJECT_DIR" ]; then
    echo "Usage: $0 [-q] <project_directory>"
    exit 1
fi

# Clone or update repository
if [ "$QUIET_MODE" = false ]; then echo "Cloning JLCPCB partlint."; fi
if [ -d "$TARGET_DIR/.git" ]; then
    if [ "$QUIET_MODE" = false ]; then echo "Repository already exists. Pulling latest changes..."; fi
    git -C "$TARGET_DIR" pull > /dev/null 2>&1
else
    if [ "$QUIET_MODE" = false ]; then echo "Cloning repository..."; fi
    git clone "$REPO_URL" "$TARGET_DIR" > /dev/null 2>&1
fi

# Run partlint and capture output
python3 "$TARGET_DIR/partlint.py" check "$PROJECT_DIR" > "$REPORT_FILE"

# Extract number of issues
ISSUES=$(grep -oP '(?<=Found )\d+(?= issues)' "$REPORT_FILE")

# Check if there are issues
if [ "$ISSUES" -gt 0 ]; then
    cat "$REPORT_FILE"
    echo -e "\033[31mFound $ISSUES issues with components.\033[0m"
else
    echo -e "\033[32mNo components issues found.\033[0m"
fi

# Remove report file
rm -f "$REPORT_FILE"

# Exit with the number of issues found
exit "$ISSUES"
