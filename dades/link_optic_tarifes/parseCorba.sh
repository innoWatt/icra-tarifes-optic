#!/bin/bash

#Aquest fitxer processa la respota de l'script "usuari_extreuPotencia.py"
: '
	Ús: $0 fitxer.txt
	* Exemple INPUT (fitxer.txt):

		PREGUNTA
		RESPOSTA
		<missatge>
			6 bytes: 10 0 1 0 1 16 
			<control>
				Byte control: 0x0=0=0b0
				bit PRM=0: Aquest missatge es una RESPOSTA
				FUN: 0b0 [32m[Funció 0] [Resposta: ACK][0m
			</control>
			Direcció comptador: 0x1=1
		</missatge>

		[...]

		CORBA POTÈNCIA  <--el grep buscarà aquesta línia
		================
		01/09/2016 01:00 97 kW
		01/09/2016 02:00 96 kW
		01/09/2016 03:00 95 kW
		01/09/2016 04:00 98 kW
		01/09/2016 05:00 97 kW
		01/09/2016 06:00 97 kW
		01/09/2016 07:00 98 kW

	* Exemple OUTPUT:
		97
		96
		95
		98
		97
		97
		98
'

if (($#<1)); then echo "Falta arxiu d'entrada. Ús: $0 [corba_carrega.txt]";exit;fi

file=$1

cat $file\
	| sed -n -e '/ CORBA POTÈNCIA/,$p'\
	| sed -n -e "3,$ p"\
	| awk '{print $3}'\
