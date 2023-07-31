#!/bin/bash

# Find the process
pid=$(ps -ef | grep uvicorn | grep -v grep | awk '{print $2}')

# Check if the process is running
if [ -z "$pid" ]
then
  echo "No FastAPI server to stop"
  exit 1
fi

# Kill the process
kill -9 $pid

echo "FastAPI server stopped successfully"
