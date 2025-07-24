#!/usr/bin/env python

import os
import re

# Function to group files into R1, R2, I1, and I2 columns
def group_files(files):
    grouped_data = {}

    # Regular expression pattern to match common part of the file names
    pattern = re.compile(r'(.*_S\d+_L\d{3})')

    # Go through each file and assign to appropriate group
    for file in files:
        match = pattern.match(file)
        if match:
            key = match.group(1)
            if key not in grouped_data:
                grouped_data[key] = {}
            if '_R1_' in file:
                grouped_data[key]['R1'] = file
            elif '_R2_' in file:
                grouped_data[key]['R2'] = file
            elif '_I1_' in file:
                grouped_data[key]['I1'] = file
            elif '_I2_' in file:
                grouped_data[key]['I2'] = file

    return grouped_data

# Function to output the result in a TSV format
def output_tsv(grouped_data, output_file):
    with open(output_file, 'w') as f:
        for key in grouped_data:
            # Extract R1, R2, I1, I2 files for each group
            R1 = grouped_data[key].get('R1', '')
            R2 = grouped_data[key].get('R2', '')
            I1 = grouped_data[key].get('I1', '')
            I2 = grouped_data[key].get('I2', '')
            f.write(f"{R1}\t{R2}\t{I1}\t{I2}\n")

# Function to read the file list from a text file
def read_file_list(input_file):
    with open(input_file, 'r') as f:
        files = [line.strip() for line in f if line.strip()]
    return files
import sys
# Input: file containing list of files
input_file = sys.argv[1]  # Replace with your actual file name

# Read file list
input_files = read_file_list(input_file)

# Group files based on R1, R2, I1, I2
grouped_files = group_files(input_files)

# Output to TSV file
output_file = sys.argv[2]
output_tsv(grouped_files, output_file)

print(f"TSV file generated: {output_file}")

