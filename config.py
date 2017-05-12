#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Edita aquest arxiu per configurar la connexió al comptador.
Direcció, password, punt de mesura i connexió serial
'''

#COMPTADOR - dades internes aparell, per crear trames (bin/crea.py)
direccio=1
password=1
puntMesura=1

#COMPTADOR - connexió serial, per enviar trames (bin/pregunta.py)
port="/dev/ttyUSB0"
baudrate=9600
bytesize=8
parity='E' #even
stopbits=1
xonxoff=False
rtscts=False
dsrdtr=False
timeout=1
