#!/bin/bash

cd usr #move pwd (important for python import paths)

options=("test" "instantani" "dia" "mes_actual" "historic" "sortir")

echo "Tria una opció"

select opt in "${options[@]}"
do
	if [[ $opt == "sortir" ]]
	then
		echo "Adeu!"; 
		exit;
	else
		echo $opt;
		python $opt.py;
	fi
done
