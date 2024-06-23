#!/bin/bash

# PharmaSee Medicine Scanner - Quick Start Script

echo "================================================"
echo "   PharmaSee - Medicine Scanner"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/lib/python*/site-packages/cv2/__init__.py" ]; then
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check if config file exists
if [ ! -f "config/config.json" ]; then
    echo ""
    echo "❌ Error: config/config.json not found"
    echo "Please copy config/config.example.json to config/config.json"
    echo "and add your OpenAI API key"
    exit 1
fi

# Check if API key is set
if grep -q '"api_key": ""' config/config.json; then
    echo ""
    echo "⚠️  Warning: OpenAI API key not set in config/config.json"
    echo "Please add your API key before running"
    exit 1
fi

echo ""
echo "✓ Configuration loaded"
echo ""
echo "================================================"
echo "Starting PharmaSee..."
echo "================================================"
echo ""

# Run the application
cd src
python3 medicine_scanner.py

# Deactivate virtual environment when done
deactivate


