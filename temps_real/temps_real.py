#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Extreure corba horària a temps real per link amb projecte "pantalla3"
(github.com/holalluis/pantalla3)

Des del dia 1 del mes actual fins al dia actual

'''
import crea     as C
import pregunta as P
import processaA11 as E
import sys
import time

#dia, mes i any acutals?
ara=time.localtime()
dia=ara.tm_mday

dia=2 #TEMPORAL TESTING

mes=ara.tm_mon
yea=ara.tm_year-2000 #0-99

'''Login amb asdu 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183(1))) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''Request amb asdu 123'''
#trama variable amb asdu 123, registre 11, objecte 1 (inicial i final)
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU123(11,1,1,C.creaTemps(1,mes,yea,0,0),C.creaTemps(dia,mes,yea,0,0))))
P.pregunta(C.creaTramaFix(0b01011011)) #request data

respostes=[] #array per contenir les respostes a processar (asdus 11)

#consulta fins que doni senyal de fi
while True: 
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: break
'''FI REQUEST'''

print(" CORBA POTÈNCIA ")
print("================")

#obre arxiu
f=open('corba.txt','w')

for i in range(len(respostes)):
    trama=respostes[i]
    #estructura dada: [diames,mes,year,hora,minut,nrg_valor]
    dada=E.extreuPotencia(trama) 
    #escriu a l'arxiu la potencia "nrg_valor"
    f.write(str(dada[5])+"\n")

# a partir d'aqui esperar una hora i escriure la següent dada. Si el mes canvia, acaba el programa

#espera 1 hora i agafa l'últim integrat disponible
f.close()
