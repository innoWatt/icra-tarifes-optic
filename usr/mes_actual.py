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

#obre arxiu
f=open('corba.txt','w')

for i in range(len(respostes)):
    trama=respostes[i]

    #estructura dada: [diames,mes,year,hora,minut,nrg_valor]
    d=E.extreuPotencia(trama) 

    #escriu a l'arxiu la potencia "nrg_valor" amb el format any-mes-dia hora:minut potencia
    f.write(str(d[2])+"-"+str(d[1])+"-"+str(d[0])+" "+str(d[3])+":"+str(d[4])+" "+str(d[5])+"\n")

#a partir d'aqui esperar una hora i escriure la següent dada. Si el mes canvia, acaba el programa
print "Esperant una hora per la següent lectura (dia/mes/any hora:minut)"; time.sleep(3600)

#espera 1 hora i agafa l'últim integrat disponible
f.close()
