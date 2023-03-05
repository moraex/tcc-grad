#!/bin/bash

for f in $(ls raw_datasets); do 
	if grep -q "_GO" <<< $f; then
		echo "=== DOING $f ==="
		target=raw_datasets/${f}/${f}.f.s
		java -jar clus.jar -forest $target
		echo "=== $f DONE! ==="
	fi
	if grep -q "_FUN" <<< $f; then
		echo "=== DOING $f ==="
		target=raw_datasets/${f}/${f}.s
		java -jar clus.jar -forest $target
		echo "=== $f DONE! ==="
	fi
done