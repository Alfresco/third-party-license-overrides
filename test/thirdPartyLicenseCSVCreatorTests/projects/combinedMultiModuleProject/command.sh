#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$1" --project "$SCRIPT_DIR/project" --combined --version "1.2.3" --output "$SCRIPT_DIR/actual"
