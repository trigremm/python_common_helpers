#!/bin/bash
# usage:
# bash generate_prompt.sh -i migrations -i test_permissions -p apps/abbreviations


# Initialize an empty prompt.txt
> prompt.txt

path=""
declare -a ignores

# Use getopts to parse command line arguments
while getopts ":p:i:" opt; do
  case $opt in
    p)
      path="$OPTARG"
      ;;
    i)
      ignores+=("$OPTARG")
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Build the find command
find_cmd="find \"$path\""

for ignore in "${ignores[@]}"; do
    find_cmd+=" -type d -name \"$ignore\" -prune -o"
done

find_cmd+=" -name \"*.py\" -type f -exec cat {} + > prompt.txt"

# Execute the dynamically built find command
eval $find_cmd

echo "Content of .py files from $path (excluding ${ignores[@]}) have been written to prompt.txt"
