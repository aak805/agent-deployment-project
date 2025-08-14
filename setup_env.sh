#!/bin/bash

# ---
# A script to create a Python virtual environment and install dependencies
# from pyproject.toml using uv.
#
# Usage:
# 1. Save this script as `setup_venv.sh` in your project's root directory.
# 2. Make it executable: `chmod +x setup_venv.sh`
# 3. Run it: `./setup_venv.sh`
# ---

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# The name of the virtual environment directory. ".venv" is a common standard.
VENV_DIR=".venv"

# --- Script Logic ---

# 1. Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: 'uv' is not installed or not in your PATH."
    echo "   Please install it first to continue."
    echo "   Installation command for macOS/Linux:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 2. Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: 'pyproject.toml' not found in the current directory."
    echo "   Please make sure you are in the root of your project."
    exit 1
fi

echo "✅ 'uv' is installed and 'pyproject.toml' is present."

# 3. Create the virtual environment
echo "🚀 Creating virtual environment in './${VENV_DIR}'..."
uv venv -p python3

echo "✅ Virtual environment created."

# 4. Install dependencies using uv sync
echo "📦 Installing dependencies from 'pyproject.toml'..."
# The `uv sync` command reads the pyproject.toml file and installs the
# dependencies into the virtual environment found in the .venv directory.
uv sync

echo "🎉 Setup complete!"
echo ""
echo "To activate your new virtual environment, run the following command:"
echo "source ${VENV_DIR}/bin/activate"