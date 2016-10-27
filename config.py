#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Edita aquest arxiu per entrar les dades del teu sistema:
    direcció, password i punt de mesura del comptador
    i dades de la connexió serial
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
