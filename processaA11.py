#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Utilitat per extreure la dada de potència i la data 
	a partir d'un ASDU 11 amb registre 11 (corba de potència)
	ASDU 11 és una resposta al ASDU 123
'''
def extreuPotencia(trama):
	'''
		Extreu la data i la potencia d'una trama de bytes tipus ASDU 11 (resposta del comptador)
		trama: objecte bytestring exemple ('\x01\x02\x03')
	'''
	trama=bytearray(trama)
	n=len(trama)

	#comprova si es trama variable
	if(trama[0]!=0x68 and trama[n-1]!=0x16): raise RuntimeError("Trama desconeguda")
	#agafa camp ASDU i comprova si és un ASDU 11 (tipus = primer byte de ASDU)
	ASDU=trama[7:n-2]
	if(ASDU[0]!=11): print("[!] ASDU incorrecte ("+str(ASDU[0])+"). Aquesta funció processa ASDUs tipus 11"); return
	#agafa element d'informació i mira byte 1: direccio (ha de ser igual a 1)
	objInfo=ASDU[6:len(ASDU)]
	if(objInfo[0]!=1): print("[!] Objecte erroni, ha de ser 1 (és "+str(objInfo[0])+")"); return

	#bytes 2 a 6: total integrat'''
	totalIntegrat=objInfo[1:6]
	#els 4 bytes primers són la potència (kw): cal byte swap i suma
	nrg=totalIntegrat[0:4]
	nrg_valor = nrg[3]<<32 | nrg[2]<<16 | nrg[1]<<8 | nrg[0] #<---VALOR POTÈNCIA kW
	#últim byte: cualificador 8 bits
	cualificador=totalIntegrat[4]

	#majúscules si bit=1, minúscules si bit=0
	IV  = 'IV'  if (cualificador & 0b10000000 == 128) else 'iv'  # la lectura es vàlida?
	CA  = 'CA'  if (cualificador & 0b01000000 == 64 ) else 'ca'  # el comptador està sincronitzat?
	CY  = 'CY'  if (cualificador & 0b00100000 == 32 ) else 'cy'  # overflow?
	VH  = 'VH'  if (cualificador & 0b00010000 == 16 ) else 'vh'  # verificació horària durant el període?
	MP  = 'MP'  if (cualificador & 0b00001000 == 8  ) else 'mp'  # modificació de paràmetres durant el període?
	IN  = 'IN'  if (cualificador & 0b00000100 == 4  ) else 'in'  # hi ha hagut intrusió durant el període?
	AL  = 'AL'  if (cualificador & 0b00000010 == 2  ) else 'al'  # període incomplet per fallo d'alimentació durant el període?
	RES = 'RES' if (cualificador & 0b00000001 == 1  ) else 'res' # bit de reserva
	#print("byte Cualificador: "+hex(cualificador)+": ["+IV+","+CA+","+CY+","+VH+","+MP+","+IN+","+AL+","+RES+"]")

	#etiqueta temps: tipus a (5 bytes)
	etiqueta=ASDU[len(ASDU)-5:len(ASDU)]
	minut     = (etiqueta[0]&0b00111111)
	TIS       = (etiqueta[0]&0b01000000) == 64
	IV        = (etiqueta[0]&0b10000000) == 128
	hora      = (etiqueta[1]&0b00011111)
	RES1      = (etiqueta[1]&0b01100000) >> 5
	SU        = (etiqueta[1]&0b10000000) == 128
	diames    = (etiqueta[2]&0b00011111)
	diasemana = (etiqueta[2]&0b11100000) >> 5
	mes       = (etiqueta[3]&0b00001111)
	ETI       = (etiqueta[3]&0b00110000) >> 4
	PTI       = (etiqueta[3]&0b11000000) >> 6
	year      = (etiqueta[4]&0b01111111) + 2000 # any va de 0-99
	RES2      = (etiqueta[4]&0b10000000) == 128

	'''detall estètic: posa un zero davant el número de: diames, mes, hora i minuts més petits de 10'''
	if(diames<10): diames="0"+str(diames)
	if(mes   <10): mes="0"+str(mes)
	if(hora  <10): hora="0"+str(hora)
	if(minut <10): minut="0"+str(minut)

	#final: mostra info i retorna dades d'interés
	print(str(diames)+"/"+str(mes)+"/"+str(year)+" "+str(hora)+":"+str(minut)+" "+str(nrg_valor)+" kW")
	return [diames,mes,year,hora,minut,nrg_valor]

'''TESTS (dades reals icra)'''
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x72\x00\x00\x00\x00\x00\x81\xa1\x07\x10\xd2\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x71\x00\x00\x00\x00\x00\x82\xa1\x07\x10\xd2\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x6c\x00\x00\x00\x00\x00\x83\xa1\x07\x10\xce\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x6e\x00\x00\x00\x00\x00\x84\xa1\x07\x10\xd1\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x6b\x00\x00\x00\x00\x00\x85\xa1\x07\x10\xcf\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x6e\x00\x00\x00\x00\x00\x86\xa1\x07\x10\xd3\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x6f\x00\x00\x00\x00\x00\x87\xa1\x07\x10\xd5\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x8b\x00\x00\x00\x00\x00\x89\xa1\x07\x10\xf3\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\xaf\x00\x00\x00\x00\x00\x8a\xa1\x07\x10\x18\x16')
extreuPotencia('\x68\x14\x14\x68\x08\x01\x00\x0b\x01\x05\x01\x00\x0b\x01\x99\x00\x00\x00\x00\x00\x8e\xa1\x07\x10\x06\x16')
print("FI TEST")
