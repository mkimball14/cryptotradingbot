#!/bin/bash

# Script to stop the running scheduler

# Go to the project directory
cd "$(dirname "$0")"

# Check if PID file exists
if [ -f "scheduler.pid" ]; then
    PID=$(cat scheduler.pid)
    echo "Stopping scheduler with PID $PID..."
    
    # Check if process is running
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "Scheduler stopped."
    else
        echo "No scheduler process found with PID $PID."
    fi
    
    # Remove PID file
    rm scheduler.pid
    echo "PID file removed."
else
    echo "No scheduler.pid file found. Scheduler may not be running."
fi 