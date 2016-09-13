#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Protocol IEC 60870-5-102
	Autor: Lluis Bosch

	Modul per processar missatges (peticions i respostes)
	Testejat amb un comptador Actaris SL761

	Bibliografia: #TODO

	els missatge provenen de la comanda serial.readlines()
	normalment sera un array de tamany 1
'''

def processa(missatge):
	buf=bytearray(missatge)

	'''comptem el numero de bytes del buffer'''
	n=len(buf) 
	print("<missatge>\n  Longitud "+str(n)+" bytes")

	'''mostra tots els bytes del missatge'''
	print(' '), 
	for i in range(n): print hex(buf[i])[2:4], 
	print('')
	
	'''primer pas: saber si la trama es fixa o variable. Es pot saber pels bits d'inici i final'''
	if(buf[0]==0x10 and buf[n-1]==0x16):
		processaTramaFixa(buf)
	elif(buf[0]==0x68 and buf[n-1]==0x16):
		processaTramaVariable(buf)
	else:
		raise RuntimeError('Tipus de trama desconegut')

	print('</missatge>\n')
	'''end'''


'''processa una trama fixa de 6 bytes'''
def processaTramaFixa(buf):
	''' 
		buf: es un objecte bytearray

				6        5      4   3      2        1
		+-------+---------+-------+----------+----+
		| inici | control | direc | checksum | fi |
		+-------+---------+-------+----------+----+
	'''
	n=len(buf)

	if(n!=6):                            raise RuntimeError('La trama no te longitud 6')
	if(buf[0]!=0x10 and buf[n-1]!=0x16): raise RuntimeError('Bytes inici (0x10) i final (0x16) erronis')

	'''Comprova checksum'''
	if(buf[1]+buf[2]+buf[3]==buf[4]):    
		print("  Checksum correcte ("+hex(buf[4])[2:4]+" = "+str(buf[4])+")")
	else:
		raise RuntimeError('Checksum erroni')

	print("  La trama es de tipus FIXE [inici (0x10) - control - direccio1 - direccio2 - checksum - fi (0x16)]")

	'''processa el byte de control'''
	control=buf[1]
	campControl(control)

	'''bytes de direccio (2)'''
	direccio = buf[3] << 8 | buf[2]
	print("  Direccio: "+hex(direccio)[2:4]+" == "+str(direccio))


'''processa una trama de llargada variable'''
def processaTramaVariable(buf):
	'''
		buf: es un objecte bytearray

		+-------+------+------+-------+---------+-----+------+----------+-------+
		| Inici | Long | Long | Inici | Control | A A | ASDU | Checksum | Final |
		+-------+------+------+-------+---------+-----+------+----------+-------+

	'''
	n=len(buf)
	if(n==0): raise RuntimeError("bytearray buit")
	if(buf[0]!=0x68 and buf[3]!=0x68 and buf[n-1]!=0x16): raise RuntimeError("Bytes inici i final erronis")

	'''comprova que els dos bytes de longitud (Long) siguin iguals'''
	if(buf[1]!=buf[2]): raise RuntimeError("Els bytes de longitud (bytes 2n i 3r) son diferents")

	'''Comprova checksum'''
	checksum=0
	for i in range(4,n-2): checksum += buf[i]
	if(checksum % 256 == buf[n-2]): 
		print("  Checksum correcte ("+str(hex(buf[n-2]))[2:4]+" = "+str(buf[n-2])+")")
	else:
		raise RuntimeError("Checksum incorrecte")

	print("  La trama es de tipus VARIABLE [inici (0x68) - L - L - inici (0x68) - ASDU - checksum - final (0x16)]")

	'''byte de control'''
	control=buf[4]
	campControl(control)

	'''bytes de direccio (2)'''
	direccio = buf[6] << 8 | buf[5]
	print("  Direccio: "+str(hex(direccio))+" = "+str(direccio))

	'''ASDU: del byte 4 fins al el n-3'''
	ASDU=buf[7:n-2]

	'''Comprova si el camp longitud coincideix amb control+direccio+asdu'''
	if(buf[1]==3+len(ASDU)):
		print("  Camp longitud correcte ("+hex(buf[1])[2:4]+" = "+str(buf[1])+" = "+str(len(ASDU))+"+3)")
	else:
		raise RuntimeError("Camp Longitud ("+str(buf[1])+") incorrecte")
	
	campASDU(ASDU)


'''processa el byte Control'''
def campControl(control):
	'''
			 8     7     6     5     4   3   2   1
		+-----+-----+-----+-----+-----------------+
		| RES | PRM | FCB | FCV |       FUN       | (si PRM=1)
		+-----+-----+-----+-----+-----------------+

		o be

		+-----+-----+-----+-----+-----------------+
		| RES | PRM | ACD | DFC |       FUN       | (si PRM=0)
		+-----+-----+-----+-----+-----------------+
	'''
	if(control==0):raise RuntimeError('Camp de control no definit')
	print("  <control>")
	print("    Byte control: "+str(control)+" = "+hex(control)+" = "+bin(control))
	res = control & 0b10000000 == 128
	prm = control & 0b01000000 == 64
	fcb = control & 0b00100000 == 32 #tambe acd
	fcv = control & 0b00010000 == 16 #tambe dfc
	fun = control & 0b00001111
	acd = fcb
	dfc = fcv
	#print([res,prm,fcb,fcv,fun])

	'''mostra informacio de cada part'''
	'''bit res (reserva) sempre ha de ser 0'''
	if(res): raise RuntimeError("Bit de reserva = 1, ha de ser 0")

	'''bit prm: direccio del missatge'''
	if(prm): print("    PRM = 1 : Aquest missatge es una PETICIO");
	else:    print("    PRM = 0 : Aquest missatge es una RESPOSTA");

	'''bits acd i dfc'''
	if(prm==False): 
		if(acd): 
			print("    ACD = 1 : Es permet l'acces a les dades de classe 1")
		else:
			print("    ACD = 0 : No es permet l'acces a les dades de classe 1 (ignorat per reglament REE)")

		if(dfc): print("    DFC = 1. ELS MISSATGES FUTURS CAUSARAN DATA OVERFLOW")

	'''Mostra que fa la funcio'''
	print("    Funcio "+str(fun))
	if(prm):
		print({
			 0:"    [Peticio: F0 RESET DEL LINK REMOT]",
			 3:"    [Peticio: F3 ENVIAMENT DE DADES D'USUARI]",
			 9:"    [Peticio: F9 SOLICITUD DE L'ESTAT DEL LINK]",
			11:"    [Peticio: F11 SOLICITUD DE DADES DE CLASSE 2]",
		}[fun])
	else:
		print({
			 0:"    [Resposta: F0 ACK]",
			 1:"    [Resposta: F1 NACK. COMANDA NO ACCEPTADA]",
			 8:"    [Resposta: F8 DADES DE L'USUARI]",
			 9:"    [Resposta: F9 NACK. DADES DEMANADES NO DISPONIBLES]",
			11:"    [Resposta: F11 ESTAT DEL LINK O DEMANDA D'ACCES]",
		}[fun])
	print("  </control>")


def campASDU(ASDU):
	'''
		ASDU: objecte bytearray

          6 bytes
		+-----------------------+--------------------+-----------------------------------+
		|  id unitat de dades   | information object | etiqueta de temps comu (opcional) |
		+-----+-----+-----+-----+--------------------+-----------------------------------+

	'''
	print("  <asdu>")
	print('    ASDU ('+str(len(ASDU))+' bytes):'),
	for i in range(len(ASDU)): print hex(ASDU[i])[2:4], 
	print('')

	iud=ASDU[0:6]
	campIUD(iud)

	print("    objectes informacio aqui")
	print("    etiquestes de temps comu aqui")

	print("  </asdu>")


def campIUD(iud):
	'''
		iud: bytearray

			 6     5     4     3   2   1
		+-----+-----+-----+-------------+
		| IDT | QEV | CDT |    DCO      |
		+-----+-----+-----+-------------+
	'''
	print("    iud [idt, qev, cdt, dco]:")
	idt=iud[0]
	qev=iud[1]
	cdt=iud[2]
	dco=iud[3:6]

	'''Diccionari de identificadors de tipus (idt)'''
	dicc_idt = {
		8  : "Totales integrados operacionales, 4 octetos (lecturas de contadores absolutos, en kWh o kVARh)",
		11 : "Totales integrados operacionales repuestos periódicamente, 4 octetos (incrementos de energía, en kWh o kVARh)",
		71 : "Identificador de fabricante y equipo. En lugar de un codigo de producto se enviara un identificador de equipo",
		72 : "Fecha y hora actuales",
		100: "Leer identificador de fabricante y equipo",
		102: "Leer registro de información de evento (single-point) por intervalo de tiempo",
		103: "Leer fecha y hora actuales",
		122: "Leer totales integrados operacionales por intervalo de tiempo y rango de direcciones",
		123: "Leer totales integrados operacionales repuestos periódicamente por intervalo de tiempo y rango de direcciones",
		128: "Firma electrónica de los totales integrados (lecturas)",
		129: "Parámetros del punto de medida",
		130: "Firma electrónica de los totales integrados repuestos periódicamente (incrementos de energía)",
		131: "Fechas y horas de cambio de horario oficial",
		132: "Carga de Clave Privada de Firma",
		133: "Leer Información de Tarificación (Valores en Curso)",
		134: "Leer Información de Tarificación (Valores Memorizados)",
		135: "Información de Tarificación (Valores en Curso)",
		136: "Información de Tarificación (Valores Memorizados)",
		137: "Cerrar Período de Facturación",
		138: "Reservado para versiones futuras del protocolo RM-CM",
		139: "Bloques de totales integrados operacionales (lecturas de contadores absolutos, en kWh o kVARh)",
		140: "Bloques de totales integrados operacionales repuestos de energía periódicamente (incrementos de energía en kWh o kVARh)",
		141: "Leer la configuración del equipo RM.",
		142: "Envío de la configuración del equipo RM.",
		143: "Modificación de la configuración de los puertos de comunicaciones.",
		144: "Lectura de potencias de contrato.",
		145: "Envío de potencias de contrato.",
		146: "Modificación de potencias de contrato.",
		147: "Lecturas de días festivos.",
		148: "Envío de días festivos",
		180: "Modificación de días festivos",
		181: "Leer firma electrónica de los totales integrados por intervalo de tiempo (lecturas) Cambiar fecha y hora",
		182: "Leer los parámetros del punto de medida",
		183: "Iniciar sesión y enviar clave de acceso",
		184: "Leer firma electrónica de los totales integrados repuestos periódicamente, por intervalo de tiempo (incrementos de energía)",
		185: "Leer fechas y horas de cambio de horario oficial",
		186: "Modificar fechas y horas de cambio de horario oficial",
		187: "Finalizar sesión",
		189: "Leer bloques de totales integrados operacionales por intervalo de tiempo y dirección",
		190: "Leer bloques de totales integrados operacionales repuestos periódicamente por intervalo de tiempo y dirección",
	}

	'''byte qualificador estructura variable [SQ (1 bit), N (7 bits)]'''
	SQ = qev & 0b10000000 == 128
	N  = qev & 0b01111111

	'''causa de transmissio (CDT) (1 byte) [T (1 bit), PN (1 bit), causa (6 bits)]'''
	T     = cdt & 0b10000000 == 128
	PN    = cdt & 0b01000000 == 64
	causa = cdt & 0b00111111

	dicc_causa={
			4:'Inicializada',
			5:'Peticion o solicitada (request or requested)',
			6:'Activacion',
			7:'Confirmacion de activacion',
			8:'Desactivacion',
			9:'Desactivacion confirmada',
			10:'Finalizacion de la activacion',
			13:'Registro de datos solicitado no disponible',
			14:'Tipo de ASDU solicitado no disponible',
			15:'Número de registro en el ASDU enviado por CM desconocido',
			16:'Especificacion de direccion en el ASDU enviado por CM desconocida',
			17:'Objeto de informacion no disponible',
			18:'Periodo de integracion no disponible',
	}

	'''direccio comuna (DCO) (3 bytes)'''
	dco_punto_medida = dco[1] << 8 | dco[0] # 2 bytes
	dco_registre     = dco[2]   # 1 byte

	print("      idt: "+hex(idt)+": "+dicc_idt[idt])
	print("      qev: "+hex(qev)+" = "+bin(qev)+": [SQ="+str(SQ)+", N = "+str(N)+" objectes informacio]")
	print("      cdt: "+hex(cdt)+": [T="+str(T)+", PN="+str(PN)+", causa="+str(causa)+" : "+dicc_causa[causa]+"]")
	print("      dco: "+str(map(hex,dco))+": [punt mesura: "+str(dco_punto_medida)+", direccio registre: "+str(dco_registre)+"]")




'''TEST'''
pregunta='\x10\x49\x01\x00\x4a\x16'
processa(pregunta)
resposta='\x10\x0b\x01\x00\x0c\x16'
processa(resposta)

pregunta='\x68\x15\x15\x68\x73\x58\x1B\x7A\x01\x06\x01\x00\x0B\x01\x08\x00\x0B\x07\x02\x0A\x00\x11\x0A\x02\x0A\xC1\x16'
processa(pregunta)
resposta='\x68\x3E\x3E\x68\x08\x58\x1B\x08\x08\x05\x01\x00\x0B\x01\x18\x01\x00\x00\x00\x02\x6E\x1F\x03\x00\x00\x03\x04\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x05\xCC\xBE\x00\x00\x00\x06\x98\x0D\x00\x00\x00\x07\x00\x00\x00\x00\x80\x08\x00\x00\x00\x00\x80\x00\x81\xB2\x09\x09\xE1\x16'
processa(resposta)
