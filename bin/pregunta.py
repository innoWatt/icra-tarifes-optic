#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Funció a nivell d'usuari
	Inclou la connexió amb el serial
	Envia una trama i mostra la resposta processada

	Sintaxi:
		pregunta(trama)
	
	Les trames "trama" es generen amb les funcions de "crea.py" (veure comentaris dins)
'''
#add parent folder to path
import sys
sys.path.insert(0,"..") 

import serial
import config
import processa as Pro

#Configuració port serial (comptador)
ser=serial.Serial()
ser.port=config.port
ser.baudrate=config.baudrate
ser.bytesize=config.bytesize
ser.parity=config.parity
ser.stopbits=config.stopbits
ser.xonxoff=config.xonxoff
ser.rtscts=config.rtscts
ser.dsrdtr=config.dsrdtr
ser.timeout=config.timeout
ser.open()

'''envia la trama per la connexió serial que acabem de crear (ser)'''
def pregunta(trama):
	print("\033[32mPREGUNTA\033[0m")
	#Pro.processa(trama) #mostra la pregunta feta
	ser.write(bytearray(trama))
	print("\033[32mRESPOSTA\033[0m")
	resposta=ser.readlines() #resposta és una "list"
	respostaTotal="" #ajunta tots els elements en un sol string
	for i in range(len(resposta)): 
		respostaTotal+=resposta[i]
	Pro.processa(respostaTotal) #mostra la resposta (veure "processa.py")
	return respostaTotal

'''TEST
pregunta('\x68\x0D\x0D\x68\x73\x01\x00\xB7\x01\x06\x01\x00\x00\x01\x00\x00\x00\x34\x16')
pregunta('\x68\x15\x15\x68\x73\x01\x00\x7A\x01\x06\x01\x00\x0B\x01\x02\x01\x00\x12\x09\x09\x00\x00\x13\x09\x09\x4e\x16')
pregunta("\x10\x5B\x01\x00\x5C\x16")
pregunta("\x10\x7B\x01\x00\x7C\x16")
'''
