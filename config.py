#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Arxiu preparat per importar i cridar

	import config as con

	con.direccio
	con.password
	[...]
'''

#dades comptador "crea.py"
direccio = 1
password = 1
puntMesura = 1

#dades connexió serial "pregunta.py"
port="/dev/ttyUSB0"
baudrate=9600
bytesize=8
parity='E' #even
stopbits=1
xonxoff=False
rtscts=False
dsrdtr=False
timeout=1
