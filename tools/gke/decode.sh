#!/bin/bash

while read line
do
    echo -n $line | cut -f1 -d" "
    echo -n $line | cut -f2 -d" " | base64 --decode
    echo ""
done
