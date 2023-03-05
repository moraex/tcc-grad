#!/bin/bash

source_folder=$1

for f in $(ls $source_folder); do
	if [ -d "$source_folder/$f" ]; then
		for d in $(ls "$source_folder/$f"); do
			echo "=== DOING $f... ==="
			DESTIN="$source_folder/$f/$d/$f.s"
			java -jar clus.jar $DESTIN
			echo "=== DONE $f ==="
		done
	fi
done



#for f in $(ls $source_folder); do
#	if [ -d "$source_folder/$f" ]; then
#		DESTIN="$source_folder/$f/$f.s"
#		sed -i "s/%%//" $DESTIN && java -jar clus.jar $DESTIN
#	fi
#done