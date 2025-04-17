#!/bin/bash

# Run scheduler script for crypto trading bot
# This script activates the virtual environment and runs the scheduled optimization
# in the background with proper logging

# Go to the project directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ensure logs directory exists
mkdir -p logs

# Check if schedule module is installed
if ! pip list | grep -q "schedule"; then
    echo "Installing required packages..."
    pip install schedule python-dotenv pandas numpy requests
fi

# Start the scheduler in the background
echo "Starting scheduled optimization script..."
nohup python scripts/strategies/scheduled_optimization.py > logs/scheduler_stdout.log 2> logs/scheduler_stderr.log &

# Save the process ID
echo $! > scheduler.pid
echo "Scheduler started with PID $(cat scheduler.pid)"
echo "Logs are written to logs/scheduler_stdout.log and logs/scheduler_stderr.log"
echo "To stop the scheduler, run: kill $(cat scheduler.pid)" 