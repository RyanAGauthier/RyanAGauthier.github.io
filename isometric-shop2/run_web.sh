#!/bin/bash
# Serve Artifact Emporium in the browser using pygbag.
#
# pygbag compiles the pygame app to WebAssembly and serves it locally.
# Open http://localhost:8000 after launch.
#
# Install:  pip install pygbag
# Build only (no server):  pygbag --build .

set -e
cd "$(dirname "$0")"

if ! command -v pygbag &>/dev/null; then
    echo "Installing pygbag..."
    pip install pygbag
fi

echo "Starting Artifact Emporium web server on http://localhost:8000"
pygbag .
