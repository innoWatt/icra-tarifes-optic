#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Envia una trama per serial i mostra la resposta processada

	Sintaxi:
		pregunta(trama)

'''
import serial
import processa as Pro

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
	#Pro.processa(trama)
	print("\033[31mRESPOSTA\033[0m")
	ser.write(bytearray(trama))
	resposta=ser.readlines() #list
	respostaTotal="" #ajunta tots els elements en un sol string
	for i in range(len(resposta)): respostaTotal+=resposta[i]
	Pro.processa(respostaTotal)

#PREGUNTES TEST
#pregunta('\x68\x0D\x0D\x68\x73\x01\x00\xB7\x01\x06\x01\x00\x00\x01\x00\x00\x00\x34\x16')
#pregunta('\x68\x15\x15\x68\x73\x01\x00\x7A\x01\x06\x01\x00\x0B\x01\x02\x01\x00\x12\x09\x09\x00\x00\x13\x09\x09\x4e\x16')
#pregunta("\x10\x5B\x01\x00\x5C\x16")
#pregunta("\x10\x7B\x01\x00\x7C\x16")
