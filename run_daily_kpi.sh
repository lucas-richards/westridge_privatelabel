#!/bin/bash

# Activate the virtual environment
source /home/lr/path/to/venv/bin/activate
#/Users/lucasrichards/desktop/projects/westridge_django/westridgeApp/run_collect_kpi.sh

# Navigate to the project directory
cd ~/westridgeApp

# Run the Django management command
python3 collect_kpi.py
python3 maintenance_email.py

# backup data base
pg_dumpall > /home/lr/database_backup/backup.sql
# echo time of backup
echo "Backup completed at $(date)"
