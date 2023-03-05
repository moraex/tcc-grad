#!/bin/bash

for f in $(ls raw_datasets); do 
	if grep -q "_GO" <<< $f; then
		echo "=== DOING $f ==="
		target=raw_datasets/${f}/${f}.trainvalid.arff
		# python3 dag2tree.py $target
		echo "=== $f DONE! ==="
	fi
done