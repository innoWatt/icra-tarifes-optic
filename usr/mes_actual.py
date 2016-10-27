#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Extreure corba horària a temps real per link amb projecte "pantalla3"
    (github.com/holalluis/pantalla3)
    Des del dia 1 del mes actual fins al dia actual
'''
import sys
sys.path.insert(0,"../bin") #add bin folder to path

import time
import crea        as C
import pregunta    as P
import processaA11 as E

#esbrina dia, mes i any actuals
ara=time.localtime()
dia=ara.tm_mday+1 #dia següent: sinó es queda a les 00:00 del dia actual
mes=ara.tm_mon
yea=ara.tm_year-2000 #0-99

'''Login ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''ASDU 123'''
#pregunta: trama variable amb asdu 123, registre 11, objecte 1 (inicial i final)
P.pregunta(C.creaTramaVar(0b01110011,
	C.creaASDU123(11,1,1,
		C.creaTemps(1  ,mes,yea,0,0),
		C.creaTemps(dia,mes,yea,0,0))))

P.pregunta(C.creaTramaFix(0b01011011)) #request data

respostes=[] #array per contenir les respostes a processar (trames amb asdus 11)

#vés consultant fins que doni senyal de fi
while True: 
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: #quan s'acabi donarà runtime error
        break
'''FI REQUEST'''

#obre arxiu
f=open('corba.txt','w')

for i in range(len(respostes)):
    trama=respostes[i]
    #estructura dada: [diames,mes,year,hora,minut,nrg_valor]
    d=E.extreuPotencia(trama) 
    #escriu a l'arxiu la potencia "nrg_valor" amb el format any-mes-dia hora:minut potencia
    f.write(str(d[2])+"-"+str(d[1])+"-"+str(d[0])+" "+str(d[3])+":"+str(d[4])+" "+str(d[5])+"\n")

f.close()
