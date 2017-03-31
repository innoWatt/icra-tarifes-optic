#!/bin/bash

cd usr #move pwd (important for python import paths)

options=("test" "instantani" "dia" "mes_actual" "historic")

echo "Tria una opció (ctrl-c per sortir)"

select opt in "${options[@]}"
do
	echo $opt
	python $opt.py
done
