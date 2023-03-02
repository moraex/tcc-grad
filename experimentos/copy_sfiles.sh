#!/bin/bash

for f in $(ls raw_datasets); do
	ORIGIN="raw_datasets/$f/$f.s"
	if [ -d "raw_datasets/$f" ]; then
		for d in $(ls "output_relief_method/$f/"); do
			DESTIN="output_relief_method/$f/$d/$f.s"
			sed "s/raw_datasets\/$f/output_relief_method\/$f\/$d/" $ORIGIN > $DESTIN
		done
	fi
done
