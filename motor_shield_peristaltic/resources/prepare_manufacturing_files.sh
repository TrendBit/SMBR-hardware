RESULTS_LOCATION="pcb_output_data/manufacturers/jlcpcb"

MAIN_PCB="pcb/detector.kicad_pcb"

PALM_PCB="${RESULTS_LOCATION}/palm/palm.kicad_pcb"
HEAD_TOP_PCB="${RESULTS_LOCATION}/head_top/head_top.kicad_pcb"
HEAD_BOTTOM_PCB="${RESULTS_LOCATION}/head_bottom/head_bottom.kicad_pcb"

mkdir -p ${RESULTS_LOCATION}/palm
mkdir -p ${RESULTS_LOCATION}/head_top
mkdir -p ${RESULTS_LOCATION}/head_bottom

REPO_URL="https://github.com/bennymeg/Fabrication-Toolkit.git"
TOOLKIT_DIR="resources/jlcpcb_toolkit"
MODULE="plugins.cli"
QUIET_MODE=false

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

# Clone or update repository
print "Setting up JLCPCB fabrication tools..."
if [ -d "$TOOLKIT_DIR/.git" ]; then
    print "Repository already exists. Pulling latest changes..."
    git -C "$TOOLKIT_DIR" pull > /dev/null 2>&1
else
    print "Cloning repository..."
    git clone "$REPO_URL" "$TOOLKIT_DIR" > /dev/null 2>&1
fi


print "Separating boards."
kikit separate --source 'annotation; ref: Palm'         pcb/detector.kicad_pcb ${PALM_PCB}
kikit separate --source 'annotation; ref: Head-Top'     pcb/detector.kicad_pcb ${HEAD_TOP_PCB}
kikit separate --source 'annotation; ref: Head-Bottom'  pcb/detector.kicad_pcb ${HEAD_BOTTOM_PCB}

print "Generating JLCPCB manufacturing files."
export PYTHONPATH="$TOOLKIT_DIR"
print "   --- Palm unit board ---"
python3 -m "$MODULE" -p ${PALM_PCB} -t -e -aL User.1
print "   --- Head-Top board ---"
python3 -m "$MODULE" -p ${HEAD_TOP_PCB} -t -e -aL User.1
print "   --- Head-Bottom board ---"
python3 -m "$MODULE" -p ${HEAD_BOTTOM_PCB} -t -e -aL User.1
