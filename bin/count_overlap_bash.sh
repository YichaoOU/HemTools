#!/bin/bash

# Usage: compare_columns.sh file1 file2 column_number [delimiter]
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo "Usage: $0 file1 file2 column_number [delimiter]"
    exit 1
fi

file1="$1"
file2="$2"
col="$3"
delim="${4:-$'\t'}"   # default to tab if not provided

# Validate column number
if ! [[ "$col" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: column_number must be a positive integer"
    exit 2
fi

# Check files
for f in "$file1" "$file2"; do
    if [ ! -r "$f" ]; then
        echo "Error: cannot read '$f'"
        exit 3
    fi
done

# Create temps and ensure cleanup on exit
col1_file=$(mktemp)
col2_file=$(mktemp)
trap 'rm -f "$col1_file" "$col2_file"' EXIT

# Extract, sort, and unique
cut -d"$delim" -f"$col" "$file1" | sort -u > "$col1_file"
cut -d"$delim" -f"$col" "$file2" | sort -u > "$col2_file"

# Counts
unique1=$(wc -l < "$col1_file")
unique2=$(wc -l < "$col2_file")
common=$(comm -12 "$col1_file" "$col2_file" | wc -l)

# Output
echo "Unique in $file1 (column $col): $unique1"
echo "Unique in $file2 (column $col): $unique2"
echo "Common values in column $col: $common"

