#!/bin/bash

echo "Creating virtual environment (if not exists)..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required packages from requirements.txt..."
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "Setup complete. You can now run python run_llm_server.py"
