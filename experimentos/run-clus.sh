#!/bin/bash

#for f in $(ls raw_datasets); do
#	if [ -d "raw_datasets/$f" ]; then
#		for d in $(ls "output_relief_method/$f/"); do
#			DESTIN="output_relief_method/$f/$d/$f.s"
#			java -jar clus.jar $DESTIN
#		done
#	fi
#done

for f in $(ls raw_datasets); do
	if [ -d "raw_datasets/$f" ]; then
		DESTIN="raw_datasets/$f/$f.s"
		java -jar clus.jar $DESTIN
	fi
done