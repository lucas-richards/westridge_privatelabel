#!/bin/bash

# Activate the virtual environment
source /Users/lucasrichards/.local/share/virtualenvs/westridge_django-We07XwXp/bin/activate
#/Users/lucasrichards/desktop/projects/westridge_django/westridgeApp/run_collect_kpi.sh

# Navigate to the project directory
cd ~/Desktop/projects/westridge_django/westridgeApp

# Run the Django management command
python3 collect_kpi.py
