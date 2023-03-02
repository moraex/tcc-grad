#!/bin/bash

for f in $(ls raw_datasets); do
	java -jar clus-relief.jar -relief raw_datasets/${f}/${f}.s
done