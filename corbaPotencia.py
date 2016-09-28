#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Utilitat concreta a nivell usuari: extreure corba horària de potència
	ASDU 123 amb registre 11 dóna corba de potència (respon ASDU 11)
'''
import crea     as C
import pregunta as P

'''CONFIGURACIÓ'''
#direccio comptador i password
di=1; psw=1 
#data inici i final
diaInici=1; mesInici=7; anyInici=16
diaFinal=2; mesFinal=7; anyFinal=16
'''FI CONFIGURACIÓ'''

#omplirem aquest array amb les respostes que s'hauran de processar
respostes=[] 

'''Inicia sessió al comptador ('pregunta.py')'''
P.pregunta(C.creaTramaVar(0b01110011,di,C.creaASDU183(psw))) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011,di)) #request data

#pregunta: trama variable amb asdu 123, registre 11, objecte 1 (inicial i final)
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU123(11,1,1,C.creaTemps(diaInici,mesInici,anyInici,0,0),C.creaTemps(diaFinal,mesFinal,anyFinal,0,0))))
while(1): #vés consultant fins que doni senyal de fi
	respostes.append(P.pregunta(C.creaTramaFix(0b01011011,d))) #request data
	respostes.append(P.pregunta(C.creaTramaFix(0b01111011,d))) #request data (flip FCB)

#mostra les trames
for i in len(respostes):
	print(respostes[i])
