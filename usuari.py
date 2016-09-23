#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	SCRIPT PER CREAR I ENVIAR TRAMES AL COMPTADOR

	Sintaxi pregunta:
		P.pregunta(trama)

	Per crear trames, veure sintaxi a "crea.py"

	year: 0-99

'''
#LES PROVES AMB ASDU 122, només funciona direccio de registre=21 :( (resum diari)
import crea     as C
import pregunta as P

d=1; psw=1 #direccio comptador=1 i password=1

#login
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU183(psw))) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data

#prova asdu 190 amb registre 11 (Curva de carga)
'''La dirección de objeto selecciona la obtención de bloques de puntos de medida genéricos con reservas (9), bloques de puntos de medida genéricos sin reservas (10) o bloques de puntos de medida de consumo sin reservas (11).'''
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU190(11,10,C.creaTemps(21,5,16,0,0),C.creaTemps(22,5,16,0,0))))
while(1):
	P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
	P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)

quit()
#curva de carga: asdu 123 amb registre 11, objecte 1
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU123(11,1,1,C.creaTemps(21,5,16,1,15),C.creaTemps(23,5,16,0,0))))
while(1):
	P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
	P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)

#P.pregunta(C.creaTramaVar(0b01010011,d,C.creaASDU187())) #request end session
#P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)

#P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU115(11,1,2,C.creaTemps(20,5,16,0,0)))) # asdu no disponible!
#P.pregunta(C.creaTramaVar(0x73,1,C.creaASDU101(11,C.creaTemps(25,1,16,6,5),C.creaTemps(25,1,16,8,5))))

#prova asdu 101
#P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU101(11)))
#P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
