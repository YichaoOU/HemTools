#!/usr/bin/env bash
myFile=$1
awk -F'\t' '{print ">" $1 "\n" $2}' $myFile