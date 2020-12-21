#!/bin/bash

echo "pulling"
git pull

echo "activating venv"
source venv/bin/activate

echo "installing dependancies"
pip install -r requirements.txt

echo "starting bot"
./main.py