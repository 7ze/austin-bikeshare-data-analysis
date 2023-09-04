#!/bin/sh

# exit if not run from project root directory
[ ! -f "pyproject.toml" ] && echo "run command from project root directory!" && exit 1
# activate virtual environment
. env/bin/activate
# run script with no op
python3 main.py -n

# ask user if they want to continue running the script
echo "Run script? [y/n]:"
read -r ans

# run script if ans is y
[ "$ans" = "y" ] && python3 main.py
