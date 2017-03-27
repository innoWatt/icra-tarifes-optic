#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Extreu la corba horària de tot un mes. 
    Des del dia 1 del mes actual fins al dia actual
		Es crearà un arxiu anomenat "corba.txt"
'''
import time
import sys

#esbrina dia, mes i any actuals
ara=time.localtime()
dia=ara.tm_mday+1 #dia següent: sinó es queda a les 00:00 del dia actual
mes=ara.tm_mon
yea=ara.tm_year-2000 #0-99

#mostra per pantalla dia inici
print "Dia inici:",[1,mes,yea];
print "Dia final:",[dia,mes,yea];

#local imports
sys.path.insert(0,"../bin") #add bin folder to path
import crea        as C
import pregunta    as P
import processaA11 as E

'''Login ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''ASDU 123 amb registre 11 i objecte 1 (inicial i final)'''
P.pregunta(C.creaTramaVar(0b01110011,
	C.creaASDU123(11,1,1,
		C.creaTemps(1  ,mes,yea,0,0),
		C.creaTemps(dia,mes,yea,0,0))))

P.pregunta(C.creaTramaFix(0b01011011)) #request data

respostes=[] #array de trames amb asdus 11

#consulta fins que doni error
while True: 
    try:                                          
        respostes.append(P.pregunta(C.creaTramaFix(0b01111011))) #flip FCB bit
        respostes.append(P.pregunta(C.creaTramaFix(0b01011011))) #request data
    except: #quan s'acabi donarà runtime error
        break
'''FI REQUEST'''

#obre arxiu de corba horària
f=open('corba.txt','w')

'''Estructura: [diames,mes,year,hora,minut,nrg_valor] '''
for i in range(len(respostes)):
    d=E.extreuPotencia(respostes[i]) 
    #escriu a l'arxiu corba.txt amb el format any-mes-dia hora:minut potencia
    f.write(str(d[2])+"-"+str(d[1])+"-"+str(d[0])+" "+str(d[3])+":"+str(d[4])+" "+str(d[5])+"\n")

f.close()
