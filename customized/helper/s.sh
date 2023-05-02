#!/bin/bash

#declare -a arr=("element1" "element2" "element3")
SERVICE_NAMES="selenium-service-1,selenium-service-2"

## now loop through the above array
for i in $(echo $SERVICE_NAMES | tr "," "\n")
do
   echo "$i"
   # or do whatever with individual element of the array
done
