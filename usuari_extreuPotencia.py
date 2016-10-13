#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Extreure corba horària
'''
import crea     as C
import pregunta as P
import processaA11 as E

#data inici i final (dia,mes,any)
inici=[ 1,10,16]
final=[17,10,16]

#processa dates
diaInici=inici[0]; mesInici=inici[1]; anyInici=inici[2]
diaFinal=final[0]; mesFinal=final[1]; anyFinal=final[2]

'''Login (asdu 183) ('pregunta.py')'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183(1))) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''INICI REQUEST amb ASDU 123'''
#pregunta: trama variable amb asdu 123, registre 11, objecte 1 (inicial i final)
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU123(11,1,1,C.creaTemps(diaInici,mesInici,anyInici,0,0),C.creaTemps(diaFinal,mesFinal,anyFinal,0,0))))
P.pregunta(C.creaTramaFix(0b01011011)) #request data

#aquest array tindrà les trames que s'hauran de processar
respostes=[] 

#vés consultant fins que doni senyal de fi
while True: 
	try:                                          
		respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
		respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
	except: break
'''FI REQUEST'''

print(" CORBA POTÈNCIA ")
print("================")
#mostra les trames
for i in range(len(respostes)):
	trama=respostes[i]
	E.extreuPotencia(trama)
