#!/usr/bin/env bash

cat <(printf "id\tover80fract\n") <(tail -n+21 $1| awk -F";" '{print $1"\t0."substr($3,1,length($3)-2)}')
