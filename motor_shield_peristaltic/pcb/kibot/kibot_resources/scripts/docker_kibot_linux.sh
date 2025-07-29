#!/bin/sh

# Default image version
IMAGE="ghcr.io/inti-cmnb/kicad9_auto:dev_1.8.5-3ec9b8d_k9.0.1_d_sid"

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export USER_NAME=$(whoami)

docker run --rm -it \
    --user "$USER_ID:$GROUP_ID" \
    --env NO_AT_BRIDGE=1 \
    --env DISPLAY="$DISPLAY" \
    --workdir="/home/$USER_NAME" \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/home/$USER_NAME:/home/$USER_NAME:rw" \
    $IMAGE /bin/bash
