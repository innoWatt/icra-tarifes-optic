#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	CREAR I ENVIAR TRAMES AL COMPTADOR a nivell usuari

	Sintaxi pregunta:
		trama=creaTrama([opcions])
		pregunta(trama)

	Per crear trames, veure sintaxi a "crea.py"

	Coses trobades fent proves:
		===FUNCIONA
			ASDU 162 amb objecte 192 (només necessita un request data després del 1r request)
			ASDU 162 amb objecte 193 (idem)
			ASDU 162 amb objecte 194 (idem)
			ASDU 190 amb registre 11 dóna corba de potència (per blocs, respon ASDU 140)
			ASDU 123 amb registre 11 dóna corba de potència (respon ASDU 11)
			ASDU 122 amb registre 21 dóna els resums diaris (respon ASDU 8)
		===NO FUNCIONA
			ASDU 122 amb registre 11 no funciona
			ASDU 115: no disponible (esborrat del codi)
			ASDU 118: no disponible (idem)

'''
import crea     as C
import pregunta as P

d=1; psw=1 #direccio comptador=1 i password=1

#login
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU183(psw))) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data

#curva de carga: asdu 123 amb registre 11, objecte 1
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU123(11,1,1,C.creaTemps(21,7,16,1,0),C.creaTemps(22,7,16,0,0))))
while(1): #vés consultant fins que doni senyal de fi
	P.pregunta(C.creaTramaFix(0b01011011,d)) #request data
	P.pregunta(C.creaTramaFix(0b01111011,d)) #request data (flip FCB)

quit('-S-T-O-P-')

#prova asdu 162: instantanis amb objecte 192
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU162(192)))
P.pregunta(C.creaTramaFix(0b01011011,d)) #request data

#prova asdu 190 amb registre 11 (Curva de carga) i direccio 9,10,11
'''La dirección de objeto selecciona la obtención de bloques de puntos de medida genéricos con reservas (9), 
bloques de puntos de medida genéricos sin reservas (10) 
o bloques de puntos de medida de consumo sin reservas (11).'''
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU190(11,10,C.creaTemps(21,5,16,0,0),C.creaTemps(22,5,16,0,0))))
while(1): #vés consultant fins que doni senyal de fi
	P.pregunta(C.creaTramaFix(0b01011011,d)) #request data
	P.pregunta(C.creaTramaFix(0b01111011,d)) #request data (flip FCB)

