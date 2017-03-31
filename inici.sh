#!/bin/bash

options=("test" "instantani" "dia" "mes actual" "historic")

select opt in "${options[@]}"
do
	echo $opt
done
