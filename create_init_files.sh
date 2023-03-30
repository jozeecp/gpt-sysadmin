#!/bin/bash

# Find all directories in the current directory and its subdirectories
find . -type d | while read -r dir; do
  # Check if __init__.py exists in the directory
  if [ ! -f "$dir/__init__.py" ]; then
    # If __init__.py does not exist, create an empty one
    touch "$dir/__init__.py"
    echo "Created __init__.py in $dir"
  fi
done
