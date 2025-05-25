#!/bin/bash
# This script retrieves all the TODO comments from all the files in the current directory and its subdirectories.
# It then prints the file name, line number, and the TODO comment.
# Only check .py and .vhd files for TODO comments
grep -r --include="*.py" --include="*.vhd" -i "TODO:" .