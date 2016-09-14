#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
	print("REQUEST")
	Pro.processa(trama)
	print("RESPOSTA...")
	ser.write(bytearray(trama))
	resposta=ser.readlines()

	respostaTotal=""
	for i in range(len(resposta)): 
		respostaTotal+=resposta[i]
	Pro.processa(respostaTotal)

pregunta('\x68\x15\x15\x68\x73\x01\x00\x7A\x01\x06\x01\x00\x0B\x01\x02\x01\x00\x12\x09\x09\x00\x00\x13\x09\x09\x4e\x16')
'''
pregunta("\x10\x5B\x01\x00\x5C\x16")
pregunta("\x10\x7B\x01\x00\x7C\x16")
'''
