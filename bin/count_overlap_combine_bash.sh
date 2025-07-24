#!/bin/bash

# Usage: compare_col1_col2.sh file1 file2 [delimiter]
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage: $0 file1 file2 [delimiter]"
    exit 1
fi

file1="$1"
file2="$2"
delim="${3:-$'\t'}"  # default delimiter: tab

# Check files
for f in "$file1" "$file2"; do
    if [ ! -r "$f" ]; then
        echo "Error: cannot read '$f'"
        exit 2
    fi
done

# Temp files
tmp1=$(mktemp)
tmp2=$(mktemp)
trap 'rm -f "$tmp1" "$tmp2"' EXIT

# Extract and combine columns 1 and 2 (joined with tab or another separator)
awk -F"$delim" '{print $1 FS $2}' "$file1" | sort -u > "$tmp1"
awk -F"$delim" '{print $1 FS $2}' "$file2" | sort -u > "$tmp2"

# Counts
unique1=$(wc -l < "$tmp1")
unique2=$(wc -l < "$tmp2")
common=$(comm -12 "$tmp1" "$tmp2" | wc -l)

# Output
echo "Unique (col1+col2) in $file1: $unique1"
echo "Unique (col1+col2) in $file2: $unique2"
echo "Common combinations: $common"

