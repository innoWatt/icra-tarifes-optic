#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    asdu 103 pregunta la hora al comptador
'''
import sys
sys.path.insert(0,"../bin") #add bin folder to path
import crea     as C
import pregunta as P

#login
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request data

#envia asdu 103
P.pregunta(C.creaTramaVar(0x73,C.creaASDU103())) 
P.pregunta(C.creaTramaFix(0b01011011)) #request data
