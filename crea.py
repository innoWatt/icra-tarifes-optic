#!/usr/bin/env python
# -*- coding: utf-8 -*-
import processa as Pro
'''
	funcions que permeten crear trames (format bytearray) 
	trama fixa o variable 
	asdu122
	asdu134
	asdu183
	etiquetes de temps
'''

def creaTramaFix(control,direccio):
	trama=[None]*6
	trama[0]=0x10     #inici
	trama[1]=control  #byte control [RES,PRM,FCB,FCV,FUN]
	trama[2]=direccio & 0xff
	trama[3]=direccio & 0xff00
	trama[4]=(trama[1]+trama[2]+trama[3])%256
	trama[5]=0x16
	return bytearray(trama)
	''' tests trames fixes
		trama=creaTramaFix(0b01001001,1) #solicitud d'estat d'enllaç
		Pro.processa(trama)
		trama=creaTramaFix(0b01000000,1) #reset d'enllaç remot
		Pro.processa(trama)
	'''

def creaTramaVar(control,direccio,asdu):
	trama = [None]*8
	trama[0]=0x68 #inici
	trama[1]=0x00 #longitud
	trama[2]=0x00 #longitud
	trama[3]=0x68 #inici
	trama[4]=control
	trama[5]=direccio & 0xff
	trama[6]=direccio & 0xff00
	trama[7:7+len(asdu)]=asdu
	checksum=0
	for i in range(4,len(trama)): checksum+=trama[i]
	checksum%=256
	trama.append(checksum)
	trama.append(0x16)
	trama[1]=3+len(asdu)
	trama[2]=3+len(asdu)
	return bytearray(trama)

'''IMPLEMENTACIÓ DELS DIFERENTS TIPUS D'ASDU'''
'''implementar ASDUS per peticions: 122,134,183 '''
def creaASDU122(direccio_inici,direccio_final,data_inici,data_final):
	'''
		direccio_inici = byte
		direccio_final = byte
		data_inici = bytearray
		data_final = bytearray

		18 bytes
		+---------------+-------------------------------+
		| IUD (6 bytes) | objecte informacio (12 bytes) |
		+---------------+-------------------------------+
	'''
	asdu=[None]*18
	asdu[0]=122 #idt identificador de tipo
	asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
	asdu[2]=6   #cdt: causa=activación (6)
	asdu[3]=1   #punt mesura (1 bytes)
	asdu[4]=(11&0x00ff)    #direccio registre (2 bytes)
	asdu[5]=(11&0xff00)>>8 #direccio registre: 11: Totales integrados con período de integración 1 (curva de carga)
	asdu[6]=direccio_inici
	asdu[7]=direccio_final
	asdu[8:13]=data_inici
	asdu[13:18]=data_final
	return bytearray(asdu)

def creaASDU134(data_inici,data_final):
	'''
		A134: LEER INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)
		és una petició dels valors de la tarifa. 
		la resposta és un A136
		16 bytes
		+---------------+----------------------+----------------------+
		| IUD (6 bytes) | data inici (5 bytes) | data final (5 bytes) |
		+---------------+----------------------+----------------------+
	'''
	asdu=[None]*16
	asdu[ 0]=134 #idt identificador de tipo
	asdu[ 1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
	asdu[ 2]=5   #cdt: causa=peticion o solicitada (5)
	asdu[ 3]=1   #punt mesura (1 bytes)
	asdu[ 4]=(136&0x00ff)    #direccio registre (2 bytes)
	asdu[ 5]=(136&0xff00)>>8 #direccio registre: 136: Información de Tarificación relativa al Contrato III
	asdu[ 6:11] = data_inici
	asdu[11:16] = data_final
	return bytearray(asdu)

def creaASDU183(clau):
	'''
		A183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO
		A183 és una petició d'inici de sessió

		10 bytes
		+---------------+----------------+
		| IUD (6 bytes) | clau (4 bytes) |
		+---------------+----------------+
	'''
	asdu=[None]*10
	asdu[0]=183 #idt identificador de tipo
	asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
	asdu[2]=6   #cdt: causa=activación (6)
	asdu[3]=1   #punt mesura (1 bytes)
	asdu[4]=(0&0x00ff)    #direccio registre (2 bytes)
	asdu[5]=(0&0xff00)>>8 #direccio registre: 0 : cap registre

	asdu[6]=(clau & 0x000000ff)
	asdu[7]=(clau & 0x0000ff00)>>8
	asdu[8]=(clau & 0x00ff0000)>>16
	asdu[9]=(clau & 0xff000000)>>32
	return bytearray(asdu)

def creaASDU187():
	'''
		REQUEST de finalitzar sessió
		ASDU buit, només té el camp IUD (6 bytes)
	'''
	asdu=[None]*6
	asdu[0]=187 #idt identificador de tipo
	asdu[1]=0   #qev: byte [SQ=0 (1 bit), N=0 (7 bits)]
	asdu[2]=6   #cdt: causa=activación (6)
	asdu[3]=1   #punt mesura (1 bytes)
	asdu[4]=(0&0x00ff)    #direccio registre (2 bytes)
	asdu[5]=(0&0xff00)>>8 #direccio registre: 0 : cap registre
	return bytearray(asdu)

'''crea etiqueta de temps'''
def creaTemps(diames,mes,year,hora,minut):
	'''
		minut:int, hora:int, diames:int, mes:int, year:int (0-99)
		returns: objecte bytearray

		tipus a: 5 bytes. Estructura 40 bits:

			 1-6     7     8   9-13   14-15   16    17-21     22-24     25-28   29-30   31-32   33-39    40
		+-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
		| minut | TIS | IV | hora |  RES1 | SU | diames | diasemana |  mes  |  ETI  |  PTI  |  year | RES2 |
		+-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
		           0     1           0-0    0              0                    0       0              0

		minut     = (etiqueta[0] & 0b00111111)
		TIS       = (etiqueta[0] & 0b01000000) == 64
		IV        = (etiqueta[0] & 0b10000000) == 128
		hora      = (etiqueta[1] & 0b00011111)
		RES1      = (etiqueta[1] & 0b01100000) >> 5
		SU        = (etiqueta[1] & 0b10000000) == 128
		diames    = (etiqueta[2] & 0b00011111)
		diasemana = (etiqueta[2] & 0b11100000) >> 5
		mes       = (etiqueta[3] & 0b00001111)
		ETI       = (etiqueta[3] & 0b00110000) >> 4
		PTI       = (etiqueta[3] & 0b11000000) >> 6
		year      = (etiqueta[4] & 0b01111111)
		RES2      = (etiqueta[4] & 0b10000000) == 128
	'''
	trama=[None]*5
	trama[0] = minut + 128 # IV=1
	trama[1] = hora
	trama[2] = diames
	trama[3] = mes
	trama[4] = year
	return bytearray(trama)

'''
	Sintaxi:
		creaTramaFix(control,direccio)
		creaTramaVar(control,direccio,asdu)
		creaASDU122(registre_inici,registre_final,data_inici,data_final)
		creaASDU134(data_inici,data_final)
		creaASDU183(clau)
		creaASDU187()
		creaTemps(diames,mes,year,hora,minut)
'''

'''tests
trama=creaTramaFix(0x49,1)
trama=creaTramaVar(0x73,1,creaASDU122(1,2,creaTemps(25,1,16,6,5),creaTemps(25,1,16,8,5)))
trama=creaTramaVar(0x73,1,creaASDU134(creaTemps(25,1,14,0,0),creaTemps(26,1,14,0,0)))
trama=creaTramaVar(0x73,1,creaASDU183(12345678))
trama=creaTramaVar(0x53,1,creaASDU187())
Pro.processa(trama)
'''
