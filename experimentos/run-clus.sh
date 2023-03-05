#!/bin/bash

#for f in $(ls raw_datasets); do
#	if [ -d "raw_datasets/$f" ]; then
#		for d in $(ls "output_relief_method/$f/"); do
#			DESTIN="output_relief_method/$f/$d/$f.s"
#			java -jar clus.jar $DESTIN
#		done
#	fi
#done

source_folder=$1

for f in $(ls $source_folder); do
	if [ -d "$source_folder/$f" ]; then
		DESTIN="$source_folder/$f/$f.s"
		sed -i "s/%%//" $DESTIN && java -jar clus.jar $DESTIN
	fi
done