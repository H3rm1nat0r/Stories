#!/bin/sh
git pull
conda activate stories
conda update --all -y
python --version
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
