#!/bin/bash

# atencao, este script executa o comando "sed"
# "sed" e um comando que limpa o arquivo em caso de falha
# por isso manipule este bash se estiver seguro!

# exemplo de execucao
# ./copy_sfiles.sh raw_datasets output_genie3_method

source_folder=$1
target_folder=$2

for f in $(ls $source_folder); do
	ORIGIN="$source_folder/$f/$f.s"
	if [ -d "$source_folder/$f" ]; then
		for d in $(ls "$target_folder/$f/"); do
			DESTIN="$target_folder/$f/$d/$f.s"
			sed "s/$source_folder\/$f/$target_folder\/$f\/$d/" $ORIGIN > $DESTIN && sed -i "s/%%//" $DESTIN
		done
	fi
done
