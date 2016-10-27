#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
LOGOUT per quan es queda pillat amb l'anterior consulta
'''
import sys
sys.path.insert(0,"../bin") #add bin folder to path

import crea     as C
import pregunta as P

#logout
P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU187())) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011)) #request class 2 data
