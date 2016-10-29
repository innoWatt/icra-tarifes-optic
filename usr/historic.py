#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Extreu corba horària entre un rang de dates i mostra-la per pantalla
'''
#dates inicial i final (dia,mes,any)
inici=[ 1,10,16]
final=[29,10,16]

#imports
import sys
sys.path.insert(0,"../bin") #add bin folder to path
import crea        as C
import pregunta    as P
import processaA11 as E

#processa dates
diaInici=inici[0]; mesInici=inici[1]; anyInici=inici[2]
diaFinal=final[0]; mesFinal=final[1]; anyFinal=final[2]

'''Login amb ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''REQUEST amb ASDU 123 registre 11 i objecte 1 inicial i final'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU123(11,1,1,C.creaTemps(diaInici,mesInici,anyInici,0,0),C.creaTemps(diaFinal,mesFinal,anyFinal,0,0))))
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''Array per contenir les respostes a processar (trames amb asdus 11)'''
respostes=[] 

#consulta fins que doni error
while True: 
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: #quan s'acabi donarà runtime error
        break
'''FI REQUEST'''

print("CORBA POTÈNCIA");print("==============")
for i in range(len(respostes)):
	E.extreuPotencia(respostes[i])
