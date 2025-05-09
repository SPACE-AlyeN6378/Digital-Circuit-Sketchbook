#!/bin/bash
# This script retrieves all the TODO comments from all the files in the current directory and its subdirectories.
# It then prints the file name, line number, and the TODO comment.
grep -r --include="*.*" -i "TODO:" .