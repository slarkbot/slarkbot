#!/bin/bash

echo "pulling"
git pull

echo "activating venv"
source venv/bin/activate

echo "installing dependencies"
pip install -r requirements.txt

echo "starting bot"
./main.py