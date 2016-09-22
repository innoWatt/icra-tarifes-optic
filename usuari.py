#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	SCRIPT PER CREAR I ENVIAR TRAMES AL COMPTADOR

		Sintaxi crea:
			C.creaTramaFix(control,direccio)
			C.creaTramaVar(control,direccio,asdu)
			C.creaASDU122(registre,integrat_inici,integrat_final,data_inici,data_final)
			C.creaASDU134(data_inici,data_final)
			C.creaASDU183(pass)
			C.creaASDU187()
			C.creaTemps(diames,mes,year,hora,minut):

			year: 0-99

		Sintaxi pregunta:
			P.pregunta(trama)
'''
#LES PROVES AMB ASDU 122, només funciona direccio de registre=21 :( (resum diari)
import crea     as C
import pregunta as P

d=1; psw=1 #direccio comptador=1 i password=1

#login
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU183(psw))) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data

#prova asdu 101
P.pregunta(C.creaTramaVar(0x01110011,d,C.creaASDU101(11)))
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data

#P.pregunta(C.creaTramaVar(0x73,1,C.creaASDU101(11,C.creaTemps(25,1,16,6,5),C.creaTemps(25,1,16,8,5))))
#P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU122(21,1,2,C.creaTemps(20,5,16,0,0),C.creaTemps(23,5,16,0,0))))
#P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
#P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)
#P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
#P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
#P.pregunta(C.creaTramaVar(0b01010011,d,C.creaASDU187())) #request end session
#P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)
