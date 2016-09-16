'''
	SCRIPT PER CREAR I ENVIAR TRAMES AL COMPTADOR

		Creador=C
		Pregunt=P

		Sintaxi crea:
			C.creaTramaFix(control,direccio)
			C.creaTramaVar(control,direccio,asdu)
			C.creaASDU122(registre_inici,registre_final,data_inici,data_final)
			C.creaASDU134(data_inici,data_final)
			C.creaASDU183(pass)
			C.creaASDU187()
			C.creaTemps(diames,mes,year,hora,minut):

			year: 0-99

		Sintaxi pregunta:
			P.pregunta(trama)
'''
import crea     as C
import pregunta as P

# EXEMPLE COMPLET D'ASDU 122

#direccio comptador
d=1 

P.pregunta(C.creaTramaFix(0b01001001,d)) #request link status
P.pregunta(C.creaTramaFix(0b01001001,d)) #request link status
P.pregunta(C.creaTramaFix(0b01000000,d)) #request link reset
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU183(1))) #request user data & send password
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
'''
P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU122(1,3,C.creaTemps(20,5,16,0,0),C.creaTemps(21,5,16,0,0))))
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)
P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data
P.pregunta(C.creaTramaVar(0b01010011,d,C.creaASDU187())) #request end session
P.pregunta(C.creaTramaFix(0b01111011,d)) #request class 2 data (flip FCB)
'''
