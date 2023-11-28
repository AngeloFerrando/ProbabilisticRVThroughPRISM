#!/bin/bash

# Check if an input file was provided
if [[ -z "$1" ]]; then
    echo "Usage: $0 <inputfile> <outputfile>"
    exit 1
fi

inputfile=$1
outputfile=$2

# Check if an output file was provided
if [[ -z "$outputfile" ]]; then
    echo "Error: No output file specified."
    exit 1
fi

# Replace the first line with "dtmc" and write to a new file
sed '1s/.*/dtmc/' "$inputfile" > "$outputfile"
