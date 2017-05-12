#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    asdu 187 fi sessio
'''
import sys
sys.path.insert(0,"../bin") #add bin folder to path
import crea     as C
import pregunta as P

#login
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU187())) #request user data & send password

#request data
while(1):
  P.pregunta(C.creaTramaFix(0b01011011)) #request class 2 data
  P.pregunta(C.creaTramaFix(0b01111011)) #request data (flip FCB)

