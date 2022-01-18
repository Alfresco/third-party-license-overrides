#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a temporary war file from each project directory.
for project in projectA projectB projectC
do
    cd "$SCRIPT_DIR/$project"
    zip -q "$SCRIPT_DIR/$project.zip" -r *
    cd "$SCRIPT_DIR"
done

# Run the generator script.
python3 "$1" --zippaths "$SCRIPT_DIR/projectA.zip|$SCRIPT_DIR/projectB.zip|$SCRIPT_DIR/projectC.zip" --combined --version "1.2.3" --output "$SCRIPT_DIR/actual"

# Tidy up.
rm $SCRIPT_DIR/project*.zip
