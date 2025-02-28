#!/bin/bash

is_windows() {
    [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]
}

if [ ! -d "pll_venv" ]; then
    echo "Creating virtual environment..."
    python -m venv pll_venv
else
    echo "Virtual environment already exists."
fi

if is_windows; then
    pll_venv/Scripts/activate
else
    source pll_venv/bin/activate
fi

if [ -f "setup/requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r setup/requirements.txt
else
    echo "No requirements.txt file found!"
    exit 1
fi

if is_windows; then
    set PYTHONPATH=%PYTHONPATH%
    ./components
else
    export PYTHONPATH=$PYTHONPATH:'./components'
fi

if [ -f "setup/setup_test.py" ]; then
    echo "Running the Python script..."
    python setup/setup_test.py

    if [ $? -eq 0 ]; then
        echo "PLLpy has been setup successfully!"
    else
        echo "PLLpy has encountered an error while setting up."
        exit 1
    fi
else
    echo "Python script 'setup/setup_test.py' not found!"
    exit 1
fi
