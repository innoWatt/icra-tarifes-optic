#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Mostra la corba horària d'una dia concret 
(NOMÉS ES POT FER DE TOT UN DIA, no només d'una sola hora)
No es crea un arxiu, només es mostren les dades (24)
'''
import sys

if(len(sys.argv)<2):
    print 'Ús: python %s dd-mm-yy' % sys.argv[0]
    sys.exit()
else:
    data=sys.argv[1]
    data=data.split("-")
    dia=int(data[0])
    mes=int(data[1])
    yea=int(data[2])

#local imports
sys.path.insert(0,"../bin") #add bin folder to path
import crea        as C
import pregunta    as P
import processaA11 as E

'''Login ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''ASDU 123, registre 11, objecte 1 (inicial i final)'''
P.pregunta(
	C.creaTramaVar(0b01110011,
		C.creaASDU123(11,1,1,
			C.creaTemps(dia  ,mes,yea,0,0),
			C.creaTemps(dia+1,mes,yea,0,0))))

P.pregunta(C.creaTramaFix(0b01011011)) #request data
respostes=[] #array per contenir les respostes a processar (trames amb asdus 11)
while True: #vés consultant fins que doni senyal de fi
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: #quan s'acabi donarà runtime error
        break
'''FI REQUEST'''

print("CORBA POTÈNCIA");print("==============")
for i in range(len(respostes)):
    E.extreuPotencia(respostes[i])
