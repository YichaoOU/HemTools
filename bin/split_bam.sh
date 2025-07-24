#!/bin/bash

# Function to check if a command exists
command_exists () {
    command -v "$1" >/dev/null 2>&1 ;
}

# Check for samtools installation
if ! command_exists samtools; then
    echo "samtools is not installed. Please install samtools and try again."
    exit 1
fi

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.bam> <number_of_parts>"
    exit 1
fi

# Input arguments
input_bam=$1
num_parts=$2

# Check if num_parts is a positive integer
if ! [[ "$num_parts" =~ ^[0-9]+$ ]] || [ "$num_parts" -le 0 ]; then
    echo "Number of parts must be a positive integer."
    exit 1
fi

# Get the base name of the input BAM file (without extension)
base_name=$(basename "$input_bam" .bam)

# Get the total number of alignments in the BAM file
total_alignments=$(samtools view -c $input_bam)

# Calculate the number of alignments per part
alignments_per_part=$((total_alignments / num_parts))
remaining_alignments=$((total_alignments % num_parts))

# Check if the input BAM file exists
if [ ! -f $input_bam ]; then
    echo "Input BAM file does not exist."
    exit 1
fi

# Generate split BAM files
start=0
for ((i=1; i<=num_parts; i++)); do
    # Calculate the number of alignments for the current part
    if [ $i -le $remaining_alignments ]; then
        num_alignments=$((alignments_per_part + 1))
    else
        num_alignments=$alignments_per_part
    fi

    # Output BAM file name
    output_bam="${base_name}_part${i}.bam"

    # Create the split BAM file
    samtools view -h $input_bam | head -n $((start + num_alignments + 1)) | samtools view -b -o $output_bam

    # Index the split BAM file
    samtools index $output_bam

    echo "Created $output_bam with $num_alignments alignments"

    # Update start for the next part
    start=$((start + num_alignments))
done

echo "BAM file split into $num_parts parts."


