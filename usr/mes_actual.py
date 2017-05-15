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

#horari estiu <0,1>
estiu_inici=ara.tm_isdst
estiu_final=estiu_inici

#si és març o octubre, flip bit estiu (pel canvi d'hora)
if mes in [3,10]: estiu_final=int(not(estiu_inici))

#mostra per pantalla dia inici
print "Dia inici (dd/mm/aa): 1",mes,yea;
print "Dia final (dd/mm/aa):",dia,mes,yea;

#local imports
sys.path.insert(0,"../bin") #add bin folder to path
import crea        as C
import pregunta    as P
import processaA11 as E

'''Login ASDU 183'''
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

'''ASDU 123 amb registre 11 i objecte 1 (inicial i final)'''
P.pregunta(
	C.creaTramaVar(0b01110011,
		C.creaASDU123(11,1,1,
			C.creaTemps(yea,mes,1  ,0,0,estiu_inici),
			C.creaTemps(yea,mes,dia,0,0,estiu_final)
		)
	)
)
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

#obre arxiu de lectura
f=open('lectura.txt','w')
print "Creant arxiu 'lectura.txt'..."

'''Estructura: [diames,mes,year,hora,minut,nrg_valor] '''
for i in range(len(respostes)):
    d=E.extreuPotencia(respostes[i]) 
    #escriu a l'arxiu corba.txt amb el format any-mes-dia hora:minut potencia
    f.write(str(d[2])+"-"+str(d[1])+"-"+str(d[0])+" "+str(d[3])+":"+str(d[4])+" "+str(d[5])+"\n")

f.close()
