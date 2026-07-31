#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a temporary zip file from the project directory.
cd "$SCRIPT_DIR/project"
zip -q "$SCRIPT_DIR/project.zip" -r *
cd "$SCRIPT_DIR"

# Run the generator script with a project name override (--name).
# The output CSV filename should use "customName" instead of a value derived from the source.
python3 "$1" --zippaths "$SCRIPT_DIR/project.zip" --name "customName" --combined --version "1.2.3" --output "$SCRIPT_DIR/actual"

# Tidy up.
rm "$SCRIPT_DIR/project.zip"

