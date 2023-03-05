#!/bin/bash

# exemplo de execucao
# ./run-build-subsets.sh raw_datasets genie3

source_folder=$1
method=$2

for f in $(ls $source_folder); do
	if [ -d "$source_folder/$f" ]; then
		if grep -q "_GO" <<< $f; then
			echo "=== DOING $f... ==="
			target=$source_folder/${f}/${f}
			rfeatures=${target}.fTrees10Symbolic.fimp
			python3 build_subsets.py $method $target $rfeatures
			echo "=== $f DONE! ==="
		fi
		if grep -q "_FUN" <<< $f; then
			echo "=== DOING $f... ==="
			target=$source_folder/${f}/${f}
			rfeatures=${target}Trees10Symbolic.fimp
			python3 build_subsets.py $method $target $rfeatures
			echo "=== $f DONE! ==="
		fi
	fi
done
