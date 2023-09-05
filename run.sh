#!/bin/sh

# exit if not run from project root directory
[ ! -f "pyproject.toml" ] && echo "run command from project root directory!" && exit 1

# activate virtual environment
# check platform
uname="$(uname)" # unix based systems
if [ "$uname" = "Linux" ] || [ "$uname" = "Darwin" ]; then
    . env/bin/activate
else # windows; why tf are you using windows anyway?
    . env/Scripts/activate
fi

# run script with no op
python3 main.py -n

# ask user if they want to continue running the script
echo "Run script? [y/n]:"
read -r ans

# run script if ans is y
[ "$ans" = "y" ] && python3 main.py
