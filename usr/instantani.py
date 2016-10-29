#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Extreu valors instantanis. Opcions:
	ASDU 162 amb objecte 192 (només necessita un request data després del 1r request)
	ASDU 162 amb objecte 193 (idem)
	ASDU 162 amb objecte 194 (idem)
'''

import sys
sys.path.insert(0,"../bin") #add bin folder to path
import crea     as C
import pregunta as P

#login
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request class 2 data

#request amb asdu 162 i objecte 192
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU162(192)))
P.pregunta(C.creaTramaFix(0b01011011)) #request data

