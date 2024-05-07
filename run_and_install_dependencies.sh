#!/bin/bash

# Check for Python installation and install if not present
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Installing Python 3..."
    # Command to install Python; varies based on operating system
    sudo apt-get install python3
fi

# Set up a Python virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate the virtual environment
source venv/bin/activate

# Install required Python packages
echo "Installing required Python packages..."
pip install opencv-python-headless pandas matplotlib numpy argparse pytesseract tensorflow keras

# Run the main Python script with all necessary arguments
echo "Running the program..."
python main.py "$@"

# Deactivate the virtual environment
deactivate
