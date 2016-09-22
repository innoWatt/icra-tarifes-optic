#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Envia una trama per serial i mostra la resposta processada

	Sintaxi:
		pregunta(trama)
'''
import serial
import processa as P

#obre serial
ser=serial.Serial()
ser.port="/dev/ttyUSB0"
ser.baudrate=9600
ser.bytesize=8
ser.parity=serial.PARITY_EVEN
ser.stopbits=1
ser.xonxoff=False
ser.rtscts=False
ser.dsrdtr=False
ser.timeout=1
ser.open()

def pregunta(trama):
	print("\033[32mREQUEST\033[0m")
	#P.processa(trama)
	print("\033[31mRESPOSTA\033[0m")
	ser.write(bytearray(trama))
	resposta=ser.readlines() #list
	respostaTotal="" #ajunta tots els elements en un sol string
	for i in range(len(resposta)): respostaTotal+=resposta[i]
	P.processa(respostaTotal)
	detectaError(respostaTotal)

def detectaError(trama):
	'''
		trama: byte string com ara: '\x10\x49\x01\x00\x4a\x16', s'ha de passar a bytearray
	'''
	trama=bytearray(trama)
	n=len(trama)
	#comprova el byte final
	if trama[n-1]!=0x16: raise RuntimeError("byte final de trama incorrecte")
	#comprova els bytes inicials
	if trama[0]==0x10:
		tipus="var"
		control=trama[1]
	elif trama[0]==0x68 and trama[3]==0x68:
		tipus="fix"
		control=trama[4]
	else:
		raise RuntimeError("bytes inicials incorrectes")
	#agafa el byte control, i mira els 4 primers bits
	fun=control & 0b00001111
	if   fun==1: raise RuntimeError("NACK. COMANDA NO ACCEPTADA")
	elif fun==9: raise RuntimeError("NACK. DADES DEMANADES NO DISPONIBLES")
	#si la trama és fixa ja estem
	if trama=="fix": return
	#si la trama és variable hem de mirar la causa de transmissió
	cdt=trama[7:n-2][0:6][2] & 0b00111111
	if   cdt==13: raise RuntimeError("REGISTRO DE DATOS SOLICITADO NO DISPONIBLE")
	elif cdt==14: raise RuntimeError("TIPO DE ASDU SOLICITADO NO DISPONIBLE")
	elif cdt==15: raise RuntimeError("NÚMERO DE REGISTRO EN EL ASDU ENVIADO POR CM DESCONOCIDO")
	elif cdt==16: raise RuntimeError("ESPECIFICACION DE DIRECCION EN EL ASDU ENVIADO POR CM DESCONOCIDA")
	elif cdt==17: raise RuntimeError("OBJETO DE INFORMACION NO DISPONIBLE")
	elif cdt==18: raise RuntimeError("PERIODO DE INTEGRACION NO DISPONIBLE")

#PREGUNTES TEST
#pregunta('\x68\x0D\x0D\x68\x73\x01\x00\xB7\x01\x06\x01\x00\x00\x01\x00\x00\x00\x34\x16')
#pregunta('\x68\x15\x15\x68\x73\x01\x00\x7A\x01\x06\x01\x00\x0B\x01\x02\x01\x00\x12\x09\x09\x00\x00\x13\x09\x09\x4e\x16')
#pregunta("\x10\x5B\x01\x00\x5C\x16")
#pregunta("\x10\x7B\x01\x00\x7C\x16")
