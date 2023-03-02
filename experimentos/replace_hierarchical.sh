#!/bin/bash

for f in $(ls raw_datasets); do
	if [ -d "raw_datasets/${f}" ]; then
		ORIGIN="raw_datasets/${f}/${f}.trainvalid.arff"
		DESTIN="raw_datasets/${f}/${f}.trainvalid.temp.arff"
		#sed 's/.*@ATTRIBUTE class .*/@ATTRIBUTE class string/' $ORIGIN > $DESTIN
	fi
done