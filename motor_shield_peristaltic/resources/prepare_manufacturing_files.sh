RESULTS_LOCATION="pcb_output_data/manufacturers/jlcpcb"
MAIN_PCB="pcb/${PROJECT_FILE}.kicad_pcb"
PANEL_PCB="pcb/panel/panel.kicad_pcb"
PANEL_CONFIG="resources/panel_configuration.json"

mkdir -p pcb/panel

REPO_URL="https://github.com/bennymeg/Fabrication-Toolkit.git"
TOOLKIT_DIR="resources/jlcpcb_toolkit"
TOOLKIT_VERSION="5.1.0"
MODULE="plugins.cli"
QUIET_MODE=false

echo ${MAIN_PCB}

print() {
    if [ "$QUIET_MODE" = false ]; then
        echo "$@"
    fi
}

# Parse arguments
for arg in "$@"; do
    case "$arg" in
        -q) QUIET_MODE=true ;;
    esac
done

# Clone or update repository to specific version
print "Setting up JLCPCB fabrication tools..."
if [ -d "$TOOLKIT_DIR/.git" ]; then
    cd "$TOOLKIT_DIR"
    CURRENT_COMMIT=$(git rev-parse HEAD)
    TARGET_COMMIT=$(git rev-parse "$TOOLKIT_VERSION" 2>/dev/null || echo "")
    
    if [ "$CURRENT_COMMIT" != "$TARGET_COMMIT" ]; then
        print "Repository exists but not at target version. Updating to $TOOLKIT_VERSION..."
        git fetch > /dev/null 2>&1
        git checkout "$TOOLKIT_VERSION" > /dev/null 2>&1
    fi
    cd - > /dev/null
else
    print "Cloning repository at version $TOOLKIT_VERSION..."
    git clone --branch "$TOOLKIT_VERSION" "$REPO_URL" "$TOOLKIT_DIR" > /dev/null 2>&1
fi

print "Generating panels."
kikit panelize --preset ${PANEL_CONFIG} ${MAIN_PCB} ${PANEL_PCB}

print "Generating JLCPCB manufacturing files."
export PYTHONPATH="$TOOLKIT_DIR"
print "   --- Single board ---"
python3 -m "$MODULE" -p ${MAIN_PCB} -t -e -aL User.1
print "   --- Panel ---"
python3 -m "$MODULE" -p ${PANEL_PCB} -t -e -aL User.1

# Copy files to results location
rm -rf ${RESULTS_LOCATION}

mkdir -p ${RESULTS_LOCATION}/single
mkdir -p ${RESULTS_LOCATION}/panel

cp pcb/production/bom.csv ${RESULTS_LOCATION}/single/
cp pcb/production/positions.csv ${RESULTS_LOCATION}/single/
cp pcb/production/*.zip ${RESULTS_LOCATION}/single/

cp pcb/panel/production/bom.csv ${RESULTS_LOCATION}/panel/
cp pcb/panel/production/positions.csv ${RESULTS_LOCATION}/panel/
cp pcb/panel/production/*.zip ${RESULTS_LOCATION}/panel/

rm -rf pcb/production
rm -rf pcb/panel/production
