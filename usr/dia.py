#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Mostra la corba horària d'una dia concret 
(NOMÉS ES POT FER DE TOT UN DIA, no només d'una sola hora)
No es crea un arxiu, només es mostren les dades (24)
'''
print "+-------------------------------------------+";
print "| LLEGIR CORBA DE POTENCIA D'UN DIA CONCRET |";
print "+-------------------------------------------+";

import sys
import time
#local imports
sys.path.insert(0,"../bin") #add bin folder to path
import crea        as C
import pregunta    as P
import processaA11 as E

#data del dia que es vol llegir
if(len(sys.argv)<2):
    #print 'Ús: python %s dd-mm-yy su' % sys.argv[0]
    #sys.exit()
    print "Escriu el dia que vols llegir (dd-mm-aa):";

    #esbrina data actual per fer defaults
    ara=time.localtime()
    ara_dia=ara.tm_mday
    ara_mes=ara.tm_mon
    ara_yea=ara.tm_year-2000 #0-99
    ara_dst=ara.tm_isdst

    dia=raw_input("dia (dd) ["+str(ara_dia)+"]: ")
    mes=raw_input("mes (mm) ["+str(ara_mes)+"]: ")
    yea=raw_input("any (aa) ["+str(ara_yea)+"]: ")
    estiu=raw_input("horari estiu (GMT+1)? (0,1) ["+str(ara_dst)+"]: ")

    #aplica defaults si els inputs son buits 
    if dia=='': dia=ara_dia
    if mes=='': mes=ara_mes
    if yea=='': yea=ara_yea
    if estiu=='': estiu=ara_dst
    print "Data:",dia,mes,yea,estiu
else:
    #processa args
    data=sys.argv[1]
    data=data.split("-")
    dia=int(data[0])
    mes=int(data[1])
    yea=int(data[2])
    #horari estiu? <0,1>
    estiu=sys.argv[2]
    if estiu=="": estiu=0 #default value

'''Login ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''ASDU 123, registre 11, objecte 1 (inicial i final)'''
P.pregunta(
    C.creaTramaVar(0b01110011,
        C.creaASDU123(11,1,1,
            C.creaTemps(yea,mes,dia,0,0,estiu),
		C.creaTemps(yea,mes,dia+1,0,0,estiu))))

P.pregunta(C.creaTramaFix(0b01011011)) #request data
respostes=[] #array per contenir les respostes a processar (trames amb asdus 11)
while True: #vés consultant fins que doni senyal de fi
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: #quan s'acabi donarà runtime error
        break
'''FI REQUEST'''

# mostra corba potència
print("CORBA POTÈNCIA\n==============");
for i in range(len(respostes)): 
    E.extreuPotencia(respostes[i])
