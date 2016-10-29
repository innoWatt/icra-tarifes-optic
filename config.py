#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Edita aquest arxiu per configurar la connexió al comptador.
    Direcció, password, punt de mesura i connexió serial
'''

#dades per crear trames (bin/crea.py)
direccio=1
password=1
puntMesura=1

#connexió serial per enviar trames (bin/pregunta.py)
port="/dev/ttyUSB0"
baudrate=9600
bytesize=8
parity='E' #even
stopbits=1
xonxoff=False
rtscts=False
dsrdtr=False
timeout=1
