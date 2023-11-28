#!/usr/bin/env bash

# Check if both input and output files are provided
if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo "Usage: $0 <inputfile> <outputfile>"
    exit 1
fi

inputfile=$1
outputfile=$2
declare -A labels_map

# Function to process the labels line
process_labels() {
    local labels_line=$1
    # Split the labels_line into individual label assignments
    IFS=' ' read -r -a labels <<< "$labels_line"
    for label in "${labels[@]}"; do
        # Split the label into number and name
        IFS='=' read -r num name <<< "$label"
        # Remove quotes from name and trim whitespace
        name=${name//\"/}
        name=${name// /}
        # Assign the name to the number in labels_map
        labels_map[$num]=$name
    done
}

# Function to process the states lines and output to the output file
process_states() {
    local states_lines=$1
    {
        echo "#DECLARATION"
        for num in "${!labels_map[@]}"; do
            printf "%s " "${labels_map[$num]}"
        done
        echo -e "\n#END"
        IFS=$'\n' read -r -d '' -a states <<< "$states_lines"
        for state in "${states[@]}"; do
            IFS=': ' read -r state_num labels <<< "$state"
            printf "%s " "$state_num"
            for label_num in $labels; do
                printf "%s " "${labels_map[$label_num]}"
            done
            echo ""
        done
    } > "$outputfile"
}

# Read the file and split into labels and states parts
{
    read -r labels_line
    process_labels "$labels_line"
    rest_of_file=$(cat)
    process_states "$rest_of_file"
} < "$inputfile"
