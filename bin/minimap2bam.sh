#!/bin/bash

genomeFasta=/home/yli11/Data/Human/hg38/fasta/hg38.fa
input=$1
label=$2
/home/yli11/.conda/envs/captureC/bin/minimap2 -ax splice $genomeFasta $input > $label.sam  
samtools view -bS $label.sam  > $label.bam
samtools sort -@ 6 -o $label.st.bam $label.bam
samtools index $label.st.bam
rm $label.bam
create_tracks.py --current_dir -g hg38 --skip_login

