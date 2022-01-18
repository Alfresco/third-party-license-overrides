#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a temporary war file from the project directory.
cd "$SCRIPT_DIR/project"
zip -q "$SCRIPT_DIR//project.war" -r *
cd "$SCRIPT_DIR"

# Run the generator script.
python3 "$1" --zippaths "$SCRIPT_DIR/project.war" --version "1.2.3" --output "$SCRIPT_DIR/actual"

# Tidy up.
rm "$SCRIPT_DIR/project.war"
