#!/usr/bin/env bash

SCRIPT_DIR=`dirname "$0"`

# For some reason we prefer GPL-3.0 in this project.
python3 "$1" --project "$SCRIPT_DIR/project" --desired="GPL-3.0|CDDL-1.0|EPL-2.0" --version "1.2.3" --output "$SCRIPT_DIR/actual"
