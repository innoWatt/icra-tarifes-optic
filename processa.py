#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Intèrpret de trames del Protocol IEC 60870-5-102

	Mòdul per traduir a nivell llegible missatges (peticions i respostes)
	Testejat amb un comptador Actaris SL762B

	El missatge que s'ha de passar ha de ser de la forma
	bytestring, com per exemple: ('\x10\x49\x01\x00\x4a\x16')

	Exemple de com fer servir:

	processa(trama)
	processa('\x10\x49\x01\x00\x4a\x16')

	Dins de la funció es tradueix el bytestring a la classe "bytearray"

	Estructura global:

	* Processa missatge
		* trama fixe
			* camp control
		* trama variable
			* camp control
			* asdu
				* iud
				* objectes
'''

def processa(missatge):
	'''
		Analitza la trama i crea un format llegible, semblant a HTML, com ara:
			<missatge>
				<control>
					[...]
				</control>
				<asdu>
					[...]
				</asdu>
			</missatge>

		missatge: bytestring com ara: '\x10\x49\x01\x00\x4a\x16'
	'''
	global buf #global perquè altres funcions agafen bits d'altres camps

	'''transformar a bytearray'''
	buf=bytearray(missatge)

	'''comptar numero de bytes del buffer'''
	n=len(buf) 

	'''comprova trama buida'''
	if n==0: quit("TRAMA BUIDA")


	'''mostra tots els bytes del missatge'''
	print("<missatge>\n  "+str(n)+" bytes:"),
	for i in range(n): print hex(buf[i])[2:4], 
	print('')
	
	'''primer pas: descobrir si la trama es fixa o variable, mirant bytes d'inici (0x10 ò 0x68) i final (0x16)'''
	if(buf[0]==0x10 and buf[n-1]==0x16):
		processaTramaFixa(buf) #trama fixa (6 bytes)
	elif(buf[0]==0x68 and buf[n-1]==0x16):
		processaTramaVariable(buf) #trama variable
	else:
		raise RuntimeError('Tipus de trama desconegut')

	'''fi'''
	print('</missatge>\n')
	detectaError(buf)

'''Processa una trama de longitud fixa (sempre són 6 bytes)'''
def processaTramaFixa(buf):
	''' 
		buf: objecte bytearray

		estructura (6 bytes):

		  6       5         4-3     2          1
		+-------+---------+-------+----------+----+
		| inici | control | direc | checksum | fi |
		+-------+---------+-------+----------+----+
	'''
	n=len(buf)

	'''comprova longitud i bytes inicials'''
	if(n!=6): 
		raise RuntimeError('La trama no te longitud 6')
	if(buf[0]!=0x10 and buf[n-1]!=0x16): 
		raise RuntimeError('Bytes inici (0x10) i final (0x16) erronis')

	'''calcula checksum'''
	checksum=(buf[1]+buf[2]+buf[3])%256
	if(checksum==buf[4]):    
		pass #print("  Checksum correcte ("+hex(buf[4])+"="+str(buf[4])+")")
	else:
		raise RuntimeError('Checksum incorrecte: '+str(checksum)+'=/='+str(buf[4]))

	#print("  Trama FIXE [inici (0x10), control, direccio1, direccio2, checksum, fi (0x16)]")

	'''processa el byte de control'''
	control=buf[1]
	campControl(control)

	'''mostra els 2 bytes de direccio: byte swap i suma'ls'''
	direccio = buf[3] << 8 | buf[2]
	print("  Direcció comptador: "+hex(direccio)+"="+str(direccio))
	'''fi'''

'''Processa una trama de longitud variable'''
def processaTramaVariable(buf):
	'''
		buf: objecte bytearray

		estructura en bytes:

      1              1      1      1              1         2     var    1          1
		+--------------+------+------+--------------+---------+-----+------+----------+--------------+
		| Inici (0x68) | Long | Long | Inici (0x68) | Control | A A | ASDU | Checksum | Final (0x16) |
		+--------------+------+------+--------------+---------+-----+------+----------+--------------+
	'''

	'''longitud'''
	n=len(buf)

	'''comprova bytes inici i final'''
	if(buf[0]!=0x68 and buf[3]!=0x68 and buf[n-1]!=0x16): 
		raise RuntimeError("Bytes inici i final erronis")

	'''comprova que els dos bytes de longitud duplicats (Long) siguin iguals'''
	if(buf[1]!=buf[2]): 
		raise RuntimeError("Els bytes de longitud (2n i 3r) son diferents")

	'''calcula i comprova checksum (penúltim byte)'''
	checksum=0
	for i in range(4,n-2): 
		checksum += buf[i]
	checksum%=256
	if checksum == buf[n-2]: 
		pass #print("  Checksum correcte ("+hex(buf[n-2])+"="+str(buf[n-2])+")")
	else:
		raise RuntimeError("Checksum incorrecte: "+str(buf[n-2])+"=/="+str(checksum))

	#print("  Trama VARIABLE [inici (0x68), L, L, inici (0x68), control, direccio, asdu, checksum, final (0x16)]")

	'''processa byte de control'''
	control=buf[4]
	campControl(control)

	'''2 bytes de direccio: byte swap i suma'ls'''
	direccio = (buf[6]<<8) | buf[5]
	print("  Direcció comptador: "+str(hex(direccio))+" = "+str(direccio))

	'''camp ASDU: del byte 6 fins al el n-3 inclòs'''
	ASDU=buf[7:n-2]

	'''Comprova si el byte de longitud coincideix amb la suma de control+direccio+asdu'''
	if(buf[1]==1+2+len(ASDU)):
		pass #print("  Camp longitud correcte ("+hex(buf[1])+"="+str(buf[1])+"="+str(len(ASDU))+"+3)")
	else:
		raise RuntimeError("Byte Longitud ("+str(buf[1])+") incorrecte")
	
	'''només queda processar camp asdu'''
	campASDU(ASDU)
	'''fi'''

'''processa el byte Control'''
def campControl(control):
	'''
		control: un byte (0-255) = 8 bits

		estructura (bits):
			 8     7     6     5     4   3   2   1
		+-----+-----+-----+-----+-----------------+
		| RES | PRM | FCB | FCV |       FUN       | (si PRM=1)
		+-----+-----+-----+-----+-----------------+

		o bé

		+-----+-----+-----+-----+-----------------+
		| RES | PRM | ACD | DFC |       FUN       | (si PRM=0)
		+-----+-----+-----+-----+-----------------+
	'''

	print("  <control>")
	print("    Byte control: "+hex(control)+"="+str(control)+"="+bin(control))
	res = control & 0b10000000 == 128
	prm = control & 0b01000000 == 64
	fcb = control & 0b00100000 == 32 #tambe acd
	fcv = control & 0b00010000 == 16 #tambe dfc
	fun = control & 0b00001111
	acd = fcb
	dfc = fcv
	#print([res,prm,fcb,fcv,fun]) #debugging

	'''mostra informacio de cada part'''
	'''bit res (reserva) sempre ha de ser 0'''
	if(res): raise RuntimeError("Bit de reserva no és 0")

	'''bit prm: direccio del missatge'''
	if(prm): print("    bit PRM=1: Aquest missatge es una PETICIO");
	else:    print("    bit PRM=0: Aquest missatge es una RESPOSTA");

	'''bits acd (accés permès) i dfc (data overflow)'''
	if(prm==False): 
		if(acd): 
			print("    ACD=1: Es permet l'acces a les dades de classe 1")
		else:
			#print("    ACD=0: No es permet l'acces a les dades de classe 1 (ignorat per reglament REE)")
			pass
		if(dfc): 
			raise RuntimeError("    bit DFC=1. ELS MISSATGES FUTURS CAUSARAN DATA OVERFLOW")

	'''Mostra el text de la funcio "fun" (4 bits) '''
	print("    FUN: "+bin(fun)),
	if(prm):
		print({
			 0:"[Funció 0] [Petició: RESET DEL LINK REMOT]",
			 3:"[Funció 3] [Petició: ENVIAMENT DE DADES D'USUARI]",
			 9:"[Funció 9] [Petició: SOL·LICITUD DE L'ESTAT DEL LINK]",
			11:"[Funció 11] [Petició: SOL·LICITUD DE DADES DE CLASSE 2]",
		}[fun])
	else:
		print({
			 0:"\033[32m[Funció 0] [Resposta: ACK]\033[0m",
			 1:"\033[31m[Funció 1] [Resposta: NACK. COMANDA NO ACCEPTADA]\033[0m",
			 8:"[Funció 8] [Resposta: DADES DE L'USUARI]",
			 9:"\033[31m[Funció 9] [Resposta: NACK. DADES DEMANADES NO DISPONIBLES]\033[0m",
			11:"[Funció 11] [Resposta: ESTAT DEL LINK O DEMANDA D'ACCÉS]",
		}[fun])

	'''fi'''
	print("  </control>")

'''Procssa Camp iud (data unit identifier): 6 primers bytes del camp ASDU'''
def campIUD(iud):
	'''
		iud: bytearray (6 bytes)

		  6     5     4     3   2   1
		+-----+-----+-----+-------------+
		| IDT | QEV | CDT |    DCO      |
		+-----+-----+-----+-------------+

		idt = identificador de tipus. IMPORTANT. Marca el tipus d'ASDU
		qev = qualificador d'estructura variable [SQ,N]
		cdt = causa de transmissió [T,PN,Causa]
		dco = direcció comuna [punt mesura, direccio registre]
	'''
	n=len(iud)
	print("    <iud> [idt,qev,cdt,dco]")
	print("      "+str(n)+" bytes:"),

	'''mostra tots els bytes'''
	for i in range(n): print hex(iud[i])[2:4],
	print('')

	'''agafa els bytes'''
	idt=iud[0]
	qev=iud[1]
	cdt=iud[2]
	dco=iud[3:6]

	'''Diccionari identificadors de tipus (idt)'''
	dicc_idt={
		8  :"TOTALES INTEGRADOS OPERACIONALES, 4 OCTETOS (LECTURAS DE CONTADORES ABSOLUTOS, EN KWH O KVARH)",
		11 :"TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)",
		71 :"IDENTIFICADOR DE FABRICANTE Y EQUIPO. EN LUGAR DE UN CODIGO DE PRODUCTO SE ENVIARA UN IDENTIFICADOR DE EQUIPO",
		72 :"FECHA Y HORA ACTUALES",
		100:"LEER IDENTIFICADOR DE FABRICANTE Y EQUIPO",
		101:"READ RECORD OF SINGLE-POINT INFORMATION WITH TIME TAG",
		102:"LEER REGISTRO DE INFORMACIÓN DE EVENTO (SINGLE-POINT) POR INTERVALO DE TIEMPO",
		103:"LEER FECHA Y HORA ACTUALES",
		115:"READ OPERATIONAL INTEGRATED TOTALS OF A SPECIFIC PAST INTEGRATION PERIOD AND OF A SELECTED RANGE OF ADDRESSES",
		122:"LEER TOTALES INTEGRADOS OPERACIONALES POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES",
		123:"LEER TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES",
		128:"FIRMA ELECTRÓNICA DE LOS TOTALES INTEGRADOS (LECTURAS)",
		129:"PARÁMETROS DEL PUNTO DE MEDIDA",
		130:"FIRMA ELECTRÓNICA DE LOS TOTALES INTEGRADOS REPUESTOS PERIÓDICAMENTE (INCREMENTOS DE ENERGÍA)",
		131:"FECHAS Y HORAS DE CAMBIO DE HORARIO OFICIAL",
		132:"CARGA DE CLAVE PRIVADA DE FIRMA",
		133:"LEER INFORMACIÓN DE TARIFICACIÓN (VALORES EN CURSO)",
		134:"LEER INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)",
		135:"INFORMACIÓN DE TARIFICACIÓN (VALORES EN CURSO)",
		136:"INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)",
		137:"CERRAR PERÍODO DE FACTURACIÓN",
		138:"RESERVADO PARA VERSIONES FUTURAS DEL PROTOCOLO RM-CM",
		139:"BLOQUES DE TOTALES INTEGRADOS OPERACIONALES (LECTURAS DE CONTADORES ABSOLUTOS, EN KWH O KVARH)",
		140:"BLOQUES DE TOTALES INTEGRADOS OPERACIONALES REPUESTOS DE ENERGÍA PERIÓDICAMENTE (INCREMENTOS DE ENERGÍA EN KWH O KVARH)",
		141:"LEER LA CONFIGURACIÓN DEL EQUIPO RM.",
		142:"ENVÍO DE LA CONFIGURACIÓN DEL EQUIPO RM.",
		143:"MODIFICACIÓN DE LA CONFIGURACIÓN DE LOS PUERTOS DE COMUNICACIONES.",
		144:"LECTURA DE POTENCIAS DE CONTRATO.",
		145:"ENVÍO DE POTENCIAS DE CONTRATO.",
		146:"MODIFICACIÓN DE POTENCIAS DE CONTRATO.",
		147:"LECTURAS DE DÍAS FESTIVOS.",
		148:"ENVÍO DE DÍAS FESTIVOS",
		162:"LLEGIR INSTANTANIS",
		163:"INSTANTANIS (RESPOSTA)",
		180:"MODIFICACIÓN DE DÍAS FESTIVOS",
		181:"LEER FIRMA ELECTRÓNICA DE LOS TOTALES INTEGRADOS POR INTERVALO DE TIEMPO (LECTURAS) CAMBIAR FECHA Y HORA",
		182:"LEER LOS PARÁMETROS DEL PUNTO DE MEDIDA",
		183:"INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO",
		184:"LEER FIRMA ELECTRÓNICA DE LOS TOTALES INTEGRADOS REPUESTOS PERIÓDICAMENTE, POR INTERVALO DE TIEMPO (INCREMENTOS DE ENERGÍA)",
		185:"LEER FECHAS Y HORAS DE CAMBIO DE HORARIO OFICIAL",
		186:"MODIFICAR FECHAS Y HORAS DE CAMBIO DE HORARIO OFICIAL",
		187:"FINALIZAR SESIÓN",
		189:"LEER BLOQUES DE TOTALES INTEGRADOS OPERACIONALES POR INTERVALO DE TIEMPO Y DIRECCIÓN",
		190:"LEER BLOQUES DE TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y DIRECCIÓN",
	}
	print("      idt: "+hex(idt)+": [\033[33mASDU "+str(idt)+": "+dicc_idt[idt]+"\033[0m]")

	'''
		QEV: byte qualificador estructura variable. Estructura: [SQ (1 bit), N (7 bits)]

			* bit SQ:
				0 : Para cada objeto de información se indica su dirección
				1 : Se indica la dirección exclusivamente al primer objeto, siendo las direcciones del resto consecutivas.

			* N (7 bits): quantitat d'objectes d'informació dins del camp ASDU
	'''
	SQ = qev & 0b10000000 == 128
	N  = qev & 0b01111111
	print("      qev: "+hex(qev)+" = "+bin(qev)+": [SQ="+str(SQ)+", N="+str(N)+" objectes d'informació]")

	if(SQ):quit("SQ encara no implementat (estructura variable)")

	'''causa de transmissio (cdt) (1 byte). Estructura: [T (1 bit), PN (1 bit), causa (6 bits)]'''
	T     = cdt & 0b10000000 == 128 # bit "test" val 1 si la trama es un test
	PN    = cdt & 0b01000000 == 64  # bit PN: "confirmacio positiva" o "negativa"
	causa = cdt & 0b00111111

	dicc_causa={
			4 :'INICIALIZADA',
			5 :'PETICION O SOLICITADA (REQUEST OR REQUESTED)',
			6 :'ACTIVACION',
			7 :'\033[32mCONFIRMACION DE ACTIVACION\033[0m',
			8 :'DESACTIVACION',
			9 :'DESACTIVACION CONFIRMADA',
			10:'\033[32mFINALIZACION DE LA ACTIVACION\033[0m',
			13:'\033[31mREGISTRO DE DATOS SOLICITADO NO DISPONIBLE\033[0m',
			14:'\033[31mTIPO DE ASDU SOLICITADO NO DISPONIBLE\033[0m',
			15:'\033[31mNÚMERO DE REGISTRO EN EL ASDU ENVIADO POR CM DESCONOCIDO\033[0m',
			16:'\033[31mESPECIFICACION DE DIRECCION EN EL ASDU ENVIADO POR CM DESCONOCIDA\033[0m',
			17:'\033[31mOBJETO DE INFORMACION NO DISPONIBLE\033[0m',
			18:'\033[31mPERIODO DE INTEGRACION NO DISPONIBLE\033[0m',
	}
	print("      cdt: "+hex(cdt)+": [T="+str(T)+", PN="+str(PN)+", Causa de transmissió="+str(causa)+": "+dicc_causa[causa]+"]")

	'''direccio comuna (DCO) (3 bytes). Estructura : [punt_mesura (2 bytes), registre (1 byte) ]'''
	dco_punt_mesura = (dco[1]<<8) | dco[0]
	dco_registre    = dco[2]
	dicc_registre = {
			  0 :"Dirección de defecto",
				1 :"Record address of integrated totals from the start of the accounting period",
			 11 :"Totales integrados con período de integración 1 (curva de carga)",
			 12 :"RESERVA. [Posible uso futuro para Totales integrados con período de integración 2(curva de carga, habitualmente cuartohoraria)]",
			 13 :"RESERVA. [Posible uso futuro para Totales integrados con período de integración 3(curva de carga)]",
			 21 :"Totales integrados (valores diarios) con período de integración 1 (resumen diario)",
			 22 :"RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con período de integración 2 (resumen diario)]",
			 23 :"RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con período de integración 3 (resumen diario)] ",
			 31 :"Record address of integrated totals (monthly values) integration period 1",
			 32 :"Record address of integrated totals (monthly values) integration period 2",
			 33 :"Record address of integrated totals (monthly values) integration period 3",
			 52 :"Información de evento (single-point), sección 1: incidencias de arranques y tensión bajo límites",
			 53 :"Información de evento (single-point), sección 2: incidencias de sincronización y cambio de hora",
			 54 :"Información de evento (single-point), sección 3: incidencias de cambio de parámetros",
			 55 :"Información de evento (single-point), sección 4: errores internos",
			128 :"Información de evento (single-point), sección 5: incidencias de intrusismo",
			129 :"Información de evento (single-point), sección 6: incidencias de comunicaciones",
			130 :"Información de evento (single-point), sección 7: incidencias de clave privada",
			131 :"Información de evento (single-point), sección 8: incidencias de Contrato I",
			132 :"Información de evento (single-point), sección 9: incidencias de Contrato II",
			133 :"Información de vento (single-point), sección 10: incidencias de Contrato III",
			134 :"Información de Tarificación relativa al Contrato I",
			135 :"Información de Tarificación relativa al Contrato II",
			136 :"Información de Tarificación relativa al Contrato III",
			137 :"Información de Tarificación relativa al Contrato Latente I",
			138 :"Información de Tarificación relativa al Contrato Latente II",
			139 :"Información de Tarificación relativa al Contrato Latente III",
	}
	print("      dco->punt mesura: "+hex(dco_punt_mesura)+"="+str(dco_punt_mesura)+" (2 bytes)")
	print("      dco->registre: \033[33m"+hex(dco_registre)   +"="+str(dco_registre)   +": "+dicc_registre[dco_registre]+"\033[0m")

	'''fi'''
	print("    </iud>")

'''Processa camp ASDU, dins trama variable'''
def campASDU(ASDU):
	'''
		ASDU: objecte bytearray

     6 bytes                       variable              5 bytes (a) ò 7 bytes (b)
		+-----------------------------+---------------------+-----------------------------------+
		|  data unit identifier (iud) | information objects | etiqueta de temps comu (opcional) |
		+-----------------------------+---------------------+-----------------------------------+

	'''
	n=len(ASDU)

	'''mostra els bytes'''
	print("  <asdu>\n    "+str(n)+" bytes:"),
	for i in range(len(ASDU)): print hex(ASDU[i])[2:4], 
	print('')

	'''processa camp iud'''
	iud=ASDU[0:6]
	campIUD(iud)

	'''processa camp objectes d'informació'''
	objsInfo=ASDU[6:n]
	campObjsInfo(objsInfo)

	'''fi'''
	print("  </asdu>")

'''Processa camp objectes d'informació, dins camp ASDU'''
def campObjsInfo(objsInfo):
	'''
		objsInfo: objecte bytearray

		estructura (bytes):

			1 byte        variable        5 ò 7 bytes
		+----------+---------------+-------------------+
		| direccio | elements info | etiqueta de temps |
		+----------+---------------+-------------------+
	'''
	n=len(objsInfo)

	'''mostra tots els bytes'''
	print("    <objectesInfo>\n      "+str(n)+" bytes:"),
	for i in range(n): print hex(objsInfo[i])[2:4],
	print('')

	'''quants objectes info hi ha? (7 bits "N" del byte QEV del camp IUD del camp ASDU)
	N=[     ASDU      ][IUD][QEV] & 7 bits    '''
	N=buf[7:len(buf)-2][0:6][ 1 ] & 0b01111111

	'''si no hi ha objectes, ja hem acabat'''
	if N==0:
		print("      N=0 objectes d'informació\n    <objectesInfo>")
		return
	else:
		print("      N="+str(N)+" objectes d'informació")

	'''
	Comprova idt (tipus asdu)
	idt=[     ASDU      ][IUD][idt] '''
	idt=buf[7:len(buf)-2][0:6][ 0 ]

	'''Troba si porta o no etiqueta comuna de temps'''
	'''Si saps l'ASDU, perfecte, sinó, intenta endevina-ho'''
	if(idt in [8,11]):
		print("      Amb Etiqueta comuna de temps tipus a (5 bytes)")
		longitud_etiqueta=5
	elif(idt in [122,183,134,139,140,162,163]):
		#print("      Sense etiqueta comuna de temps")
		longitud_etiqueta=0
	else:
		'''mira d'endevinar l'estructura'''
		if(n%N!=0 and (n-5)%N==0 and (n-7)%N!=0):
			print("      Detectada etiqueta comuna de temps tipus a (5 bytes)")
			longitud_etiqueta=5
		elif(n%N!=0 and (n-5)%N!=0 and (n-7)%N==0):
			print("      Detectada etiqueta comuna de temps tipus b (7 bytes)")
			longitud_etiqueta=7
		elif(n%N!=0 and (n-5)%N==0 and (n-7)%N==0):
			print("      WARNING: etiqueta tipus a i b possibles, assumint tipus a (5 bytes)")
			longitud_etiqueta=5
		else:
			print("      WARNING: etiqueta no detectada, assumint no etiqueta")
			longitud_etiqueta=0

	'''itera els elements'''
	longitud_camp=(n-longitud_etiqueta)/N
	for i in range(N):
		inici = 0+i*(longitud_camp) #posicio del byte inicial
		final = longitud_camp*(i+1) #posició del byte final
		objInfo=objsInfo[inici:final] #talla l'array
		'''processa camp i'''
		campObjInfo(objInfo)

	'''processa etiqueta comuna si n'hi ha'''
	if(longitud_etiqueta):
		etiquetaTemps=objsInfo[n-longitud_etiqueta:n]
		campEtiquetaTemps(etiquetaTemps)

	'''fi'''
	print("    </objectesInfo>")

'''Processa un sol objecte d'informació, dins camp Objectes Informació'''
def campObjInfo(objInfo):
	'''
		objInfo: classe bytearray
		estructura: MOLT VARIABLE DEPENENT DE L'ASDU TRIAT (mirar byte idt)
	'''
	n=len(objInfo)

	'''mostra tots els bytes del camp'''
	print("      <objecte>")
	print("        "+str(n)+" bytes: "),
	for i in range(n): print hex(objInfo[i])[2:4],
	print("")

	'''mira el tipus d'ASDU'''
	'''
	idt=[    A S D      ][iud][idt] '''
	idt=buf[7:len(buf)-2][0:6][ 0 ]

	'''diccionari de direccio d'objecte útil per asdu 8, 122, etc'''
	dicc_direccio={
		 1:"Totales Integrados de Activa Entrante",
		 2:"Totales Integrados de Activa Saliente",
		 3:"Totales Integrados de Reactiva primer cuadrante",
		 4:"Totales Integrados de Reactiva segundo cuadrante",
		 5:"Totales Integrados de Reactiva tercer cuadrante",
		 6:"Totales Integrados de Reactiva cuarto cuadrante",
		 7:"Datos de reserva 1",
		 8:"Datos de reserva 2",
		 9:"Bloque de totales integrados genérico con datos de reserva (Punto de medida con direcciones de objeto 1 al 8) ",
		10:"Bloque de totales integrados genérico sin datos de reserva (Punto de medida con de direcciones de objeto 1 al 6) ",
		11:"Bloque de totales integrados de consumo puro sin reservas (Punto de medida con direcciones de objeto 1, 3 y 6) ",
		20:"Información de Tarificación (Totales) ",
		21:"Información de Tarificación (período tarifario 1)",
		22:"Información de Tarificación (período tarifario 2)",
		23:"Información de Tarificación (periodo tarifario 3)",
		24:"Información de Tarificación (periodo tarifario 4)",
		25:"Información de Tarificación (período tarifario 5)",
		26:"Información de Tarificación (periodo tarifario 6)",
		27:"Información de Tarificación (período tarifario 7)",
		28:"Información de Tarificación (período tarifario 8)",
		29:"Información de Tarificación (período tarifario 9)",
	}

	'''IMPLEMENTACIÓ DELS DIFERENTS TIPUS D'ASDU'''
	'''si no està implementat, dóna un runtime error'''
	if(idt in [8,11]):
		'''A8: TOTALES INTEGRADOS OPERACIONALES, 4 OCTETOS (LECTURAS DE CONTADORES ABSOLUTOS EN KWH O KVARH)'''
		'''A8 és una resposta a la petició A122'''
		'''A11 és una resposta a A123'''
		'''byte 1: direccio de l'objecte'''
		direccio=totalIntegrat[0]
		print("        Registre "+hex(direccio)+"="+str(direccio)+": "+dicc_direccio[direccio])
		'''bytes 2 a 6: total integrat'''
		campTotalIntegrat(objInfo[1:6],'Energia')
	elif(idt in [122,123]):
		'''A122 i A123: LEER TOTALES INTEGRADOS OPERACIONALES POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES'''
		'''A122 és una petició de 4 elements: direcció inicial, direcció final, data inicial, data final'''
		'''A123 és incremental'''

		'''direccio inicial'''
		direccio_inici=objInfo[0]
		print("        Direcció inici: "+str(direccio_inici)+": "+dicc_direccio[direccio_inici])

		'''direccio final'''
		direccio_final=objInfo[1]
		print("        Direcció final: "+str(direccio_final)+": "+dicc_direccio[direccio_final])

		'''etiqueta de temps inicial'''
		etiquetaInicial = objInfo[2:7]
		campEtiquetaTemps(etiquetaInicial)

		'''etiqueta de temps final'''
		etiquetaFinal = objInfo[7:12]
		campEtiquetaTemps(etiquetaFinal)
	elif(idt in [189,190]):
		'''direccion objecto'''
		objecte=objInfo[0]
		print("        Direcció objecte: "+str(objecte))
		'''etiqueta de temps inicial'''
		etiquetaInicial = objInfo[1:6]
		campEtiquetaTemps(etiquetaInicial)
		'''etiqueta de temps final'''
		etiquetaFinal = objInfo[6:11]
		campEtiquetaTemps(etiquetaFinal)
	elif(idt in [163]):
		'''resposta a A162 (valors instantanis)'''
		n=len(objInfo)
		direccio=objInfo[0]
		print("        Direcció objecte: "+str(direccio))
		if direccio==192:
			energia = objInfo[1] + (objInfo[2] << 8) + (objInfo[3] << 16) + (((0b11111100 & objInfo[4]) >> 2) << 24)
			print("        KWh Activa Importació: "+str(energia))
			energia = objInfo[5] + (objInfo[6] << 8) + (objInfo[7] << 16) + (((0b11111100 & objInfo[8]) >> 2) << 24)
			print("        KWh Activa Exportació: "+str(energia))
			energia = objInfo[9] + (objInfo[10] << 8) + (objInfo[11] << 16) + (((0b11111100 & objInfo[12]) >> 2) << 24)
			print("        KVArh Reactiva Q1: "+str(energia))
			energia = objInfo[13] + (objInfo[14] << 8) + (objInfo[15] << 16) + (((0b11111100 & objInfo[16]) >> 2) << 24)
			print("        KVArh Reactiva Q2: "+str(energia))
			energia = objInfo[17] + (objInfo[18] << 8) + (objInfo[19] << 16) + (((0b11111100 & objInfo[20]) >> 2) << 24)
			print("        KVArh Reactiva Q3: "+str(energia))
			energia = objInfo[21] + (objInfo[22] << 8) + (objInfo[23] << 16) + (((0b11111100 & objInfo[24]) >> 2) << 24)
			print("        KVArh Reactiva Q4: "+str(energia))
		elif direccio==193:
			energia = objInfo[1] + (objInfo[2] << 8) + (objInfo[3] << 16)
			print("        Potencia Activa Total KW: "+str(energia))
			energia = objInfo[4] + (objInfo[5] << 8) + (objInfo[6] << 16)
			print("        Potencia Reactiva Total KVAr: "+str(energia))
			energia = objInfo[7] + (((0b11000000 & objInfo[8]) >> 6) << 8)
			print("        Factor de potencia total (en milessimes): "+str(energia))
			energia = objInfo[9] + (objInfo[10] << 8) + (objInfo[11] << 16)
			print("        P.Activa Fase I KW: "+str(energia))
			print("        P.Reactiva Fase I KVAr: "+ str(objInfo[12] + (objInfo[13] << 8) + (objInfo[14] << 16)))
			print("        Factor de Potencia (cos phi). Fase I (en milessimes): "+ str(objInfo[15] + (((0b11000000 & objInfo[16]) >> 6) << 8)))
			print("        P.Activa Fase II KW: "+ str(objInfo[17] + (objInfo[18] << 8) + (objInfo[19] << 16)))
			print("        P.Reactiva Fase II KVAr: "+ str(objInfo[20] + (objInfo[21] << 8) + (objInfo[22] << 16)))
			print("        Factor de Potencia (cos phi). Fase II (en milessimes): "+ str(objInfo[23] + (((0b11000000 & objInfo[24]) >> 6) << 8)))
			print("        P.Activa Fase III KW: "+ str(objInfo[25] + (objInfo[26] << 8) + (objInfo[27] << 16)))
			print("        P.Reactiva Fase III KVAr: "+ str(objInfo[28] + (objInfo[29] << 8) + (objInfo[30] << 16)))
			print("        Factor de Potencia (cos phi). Fase III (en milessimes): "+ str(objInfo[31] + (((0b11000000 & objInfo[32]) >> 6) << 8)))
		elif direccio==194:
			print("        Intensitat Fase I (decimes de A): "+ str(objInfo[1] + (objInfo[2] << 8) + (objInfo[3] << 16)))
			print("        Tensio Fase I (decimes de V): "+ str(objInfo[4] + (objInfo[5] << 8) + (objInfo[6] << 16) + (((0b11111100 & objInfo[7]) >> 2) << 24)))
			print("        Intensitat Fase II (decimes de A): "+ str(objInfo[8] + (objInfo[9] << 8) + (objInfo[10] << 16)))
			print("        Tensio Fase II (decimes de V): "+ str(objInfo[11] + (objInfo[12] << 8) + (objInfo[13] << 16) + (((0b11111100 & objInfo[14]) >> 2) << 24)))
			print("        Intensitat Fase III (decimes de A): "+ str(objInfo[15] + (objInfo[16] << 8) + (objInfo[17] << 16)))
			print("        Tensio Fase III (decimes de V): "+ str(objInfo[18] + (objInfo[19] << 8) + (objInfo[20] << 16) + (((0b11111100 & objInfo[21]) >> 2) << 24)))
		else:
			quit("Direcció desconeguda")
		campEtiquetaTemps(objInfo[n-5:n])
	elif(idt in [139,140]):
		'''direccion objecto'''
		n=len(objInfo)
		objecte=objInfo[0]
		print("        Direcció objecte: "+str(objecte))

		if objecte==9 : N=8
		if objecte==10: N=6
		if objecte==11: N=3

		for i in range(N):
			byte_inici = 1+i*5
			byte_final = 6+i*5
			nom=dicc_direccio[i+1]
			campTotalIntegrat(objInfo[byte_inici:byte_final],nom)

		'''etiqueta de temps'''
		temps=objInfo[n-5:n]
		campEtiquetaTemps(temps)
	elif(idt==134):
		'''A134: LEER INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)'''
		'''A134 és una petició dels valors de la tarifa. la resposta és un A136'''

		'''etiqueta de temps inicial'''
		etiquetaInicial = objInfo[0:5]
		campEtiquetaTemps(etiquetaInicial)

		'''etiqueta de temps final'''
		etiquetaFinal = objInfo[5:10]
		campEtiquetaTemps(etiquetaFinal)
	elif(idt==136):
		'''A136: INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)'''
		'''A136 és una resposta al A134'''

		'''byte 1: direccio'''
		direccio=objInfo[0]
		print("        Direcció: "+str(direccio)+": "+dicc_direccio[direccio])

		'''
			bytes 2 a 63: Informació de tarificació
		  infot (62 bytes) [VabA,VinA,CinA,VabRi,VinRi,CinRi,VabRc,VinRc,CinRc,R7,CR7,R8,CR8,VMaxA,FechaA,CMaxA,VExcA,CExcA,FechaIni,FechaFin]
		'''
		infot = objInfo[1:63]
		VabA     = infot[  0:4] #Energía absoluta Activa                     (4 bytes)
		VinA     = infot[  4:8] #Energía incremental Activa                  (4 bytes)
		CinA     = infot[    8] #Cualificador de Energía Activa              (1 bytes)
		VabRi    = infot[ 9:13] #Energía absoluta Reactiva Inductiva         (4 bytes)
		VinRi    = infot[13:17] #Energía incremental Reactiva Inductiva      (4 bytes)
		CinRi    = infot[   17] #Cualificador de Energía Reactiva Inductiva  (1 bytes)
		VabRc    = infot[18:22] #Energía absoluta Reactiva Capacitiva        (4 bytes)
		VinRc    = infot[22:26] #Energía incremental Reactiva Capacitiva     (4 bytes)
		CinRc    = infot[   26] #Cualificador de Energía Reactiva Capacitiva (1 bytes)
		R7       = infot[27:31] #Registro 7 reserva                          (4 bytes)
		CR7      = infot[   31] #Cualificador del Registro 7 de reserva      (1 bytes)
		R8       = infot[32:36] #Registro 8 reserva                          (4 bytes)
		CR8      = infot[   36] #Cualificador del Registro 8 de reserva      (1 bytes)
		VMaxA    = infot[37:41] #Máximo de las Potencias                     (4 bytes)
		FechaA   = infot[41:46] #Fecha del Máximo                            (5 bytes)
		CMaxA    = infot[   46] #Cualificador de Máximos                     (1 bytes)
		VexcA    = infot[47:51] #Excesos de las Potencias                    (4 bytes)
		CexcA    = infot[   51] #Cualificador de Excesos                     (1 bytes)
		FechaIni = infot[52:57] #Inicio del período                          (<etiqueta de tiempo tipo a> 5 bytes)
		FechaFin = infot[57:62] #Fin del período                             (<etiqueta de tiempo tipo a> 5 bytes)

		'''suma els bytes dels camps de 4 i 5 bytes'''
		VabA     =   VabA[3]<<32 |   VabA[2]<<16 |   VabA[1]<<8  |   VabA[0] 
		VinA     =   VinA[3]<<32 |   VinA[2]<<16 |   VinA[1]<<8  |   VinA[0] 
		VabRi    =  VabRi[3]<<32 |  VabRi[2]<<16 |  VabRi[1]<<8  |  VabRi[0] 
		VinRi    =  VinRi[3]<<32 |  VinRi[2]<<16 |  VinRi[1]<<8  |  VinRi[0] 
		VabRc    =  VabRc[3]<<32 |  VabRc[2]<<16 |  VabRc[1]<<8  |  VabRc[0] 
		VinRc    =  VinRc[3]<<32 |  VinRc[2]<<16 |  VinRc[1]<<8  |  VinRc[0] 
		R7       =     R7[3]<<32 |     R7[2]<<16 |     R7[1]<<8  |     R7[0] 
		R8       =     R8[3]<<32 |     R8[2]<<16 |     R8[1]<<8  |     R8[0] 
		VMaxA    =  VMaxA[3]<<32 |  VMaxA[2]<<16 |  VMaxA[1]<<8  |  VMaxA[0] 
		VexcA    =  VexcA[3]<<32 |  VexcA[2]<<16 |  VexcA[1]<<8  |  VexcA[0] 

		'''mostra'''
		print("        Energía absoluta Activa:                     "+str( VabA)+" kWh"   )
		print("        Energía incremental Activa:                  "+str( VinA)+" kWh"   )
		print("        Cualificador de Energía Activa:              "+str( CinA)          )
		print("        Energía absoluta Reactiva Inductiva:         "+str(VabRi)+" kVArh" )
		print("        Energía incremental Reactiva Inductiva:      "+str(VinRi)+" kVArh" )
		print("        Cualificador de Energía Reactiva Inductiva:  "+str(CinRi)          )
		print("        Energía absoluta Reactiva Capacitiva:        "+str(VabRc)+" kVArh" )
		print("        Energía incremental Reactiva Capacitiva:     "+str(VinRc)+" kVArh" )
		print("        Cualificador de Energía Reactiva Capacitiva: "+str(CinRc)          )
		print("        Registro 7 reserva:                          "+str(   R7)          )
		print("        Cualificador del Registro 7 de reserva:      "+str(  CR7)          )
		print("        Registro 8 reserva:                          "+str(   R8)          )
		print("        Cualificador del Registro 8 de reserva:      "+str(  CR8)          )
		print("        Máximo de las Potencias:                     "+str(VMaxA)+" kW"    )
		print("        Fecha del Máximo:                            "); campEtiquetaTemps(FechaA)
		print("        Cualificador de Máximos:                     "+str(CMaxA)          )
		print("        Excesos de las Potencias:                    "+str(VexcA)+" kW"    )
		print("        Cualificador de Excesos:                     "+str(CexcA)          )
		print("        Inicio del período:                          "); campEtiquetaTemps(FechaIni)
		print("        Fin del período:                             "); campEtiquetaTemps(FechaFin)
	elif(idt==183):
		'''A183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO'''
		'''A183 és una petició d'inici de sessió'''
		clau = objInfo[0:4]

		'''suma els 4 bytes de la clau d'accés'''
		clau = clau[3]<<32 | clau[2]<<16 | clau[1]<<8 | clau[0]
		print("        Clau d'accés: "+str(clau))
	elif(idt==187):
		'''A187: FINALIZAR SESIÓN'''
		'''A187 és una petició de fi de sessió'''
		'''
				Exemple de A187:
				in Lo Lo in Co Di Di [   ASDU==IUD   ] Cs Fi
			  68 09 09 68 53 58 1B BB 00 06 01 00 00 88 16
				és un objecte d'informació buit
		'''
		print("        Request de FINALITZAR SESSIÓ")
	else:
		print("      </objecte>")
		quit("[!] ERROR: ASDU "+str(idt)+" ENCARA NO IMPLEMENTAT")

	'''fi'''
	print("      </objecte>")

'''Processa una sola etiqueta de temps'''
def campEtiquetaTemps(etiqueta):
	'''
		etiqueta: classe bytearray

		l'etiqueta de temps conté una data

		pot ser: 
			* tipus a (5 bytes) 
			* tipus b (7 bytes)
	'''
	n=len(etiqueta)

	'''comprova el tipus d'etiqueta'''
	if(n==5):   tipus="a"
	elif(n==7): tipus="b"
	else: raise RuntimeError("Etiqueta de temps desconeguda")

	if tipus=="b":
		print("          Etiqueta Tipus b encara no implementada")
		return

	'''mostra l'etiqueta'''
	print("        [\033[34mETIQUETA\033[0m] tipus "+tipus+" ("+str(n)+" bytes):"),
	for i in range(n): print hex(etiqueta[i])[2:4],

	'''
		Estructura dels 5 bytes == 40 bits
		Cada byte s'ha de llegir al revés

			 1-6     7     8   9-13   14-15   16    17-21     22-24     25-28   29-30   31-32   33-39    40
		+-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
    | minut | TIS | IV | hora |  RES1 | SU | diames | diasemana |  mes  |  ETI  |  PTI  |  year | RES2 |
    +-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
	'''
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
	year      = (etiqueta[4]&0b01111111)
	RES2      = (etiqueta[4]&0b10000000) == 128

	'''detall estètic: posa un zero davant el número de: diames, mes, hora i minuts més petits de 10'''
	if(diames<10): diames="0"+str(diames)
	if(mes   <10): mes="0"+str(mes)
	if(hora  <10): hora="0"+str(hora)
	if(minut <10): minut="0"+str(minut)

	print("== Data: "+str(diames)+"/"+str(mes)+"/"+str(2000+year)+" "+str(hora)+":"+str(minut))
	'''fi'''

'''Processa un total integrat (dins alguns tipus d'asdu)'''
def campTotalIntegrat(totalIntegrat,nom):
	'''4 bytes primers per energia (kwh o kvarh): cal byte swap i suma'''
	nrg       = totalIntegrat[0:4]
	nrg_valor = nrg[3] << 32 | nrg[2] << 16 | nrg[1] << 8 | nrg[0]
	print("        "+nom+": "+str(nrg_valor)+" (kWh o kVARh)")
	'''últim byte: cualificador 8 bits '''
	cualificador = totalIntegrat[4]
	IV = cualificador & 0b10000000 == 128 # la lectura es vàlida?
	CA = cualificador & 0b01000000 == 64  # el comptador està sincronitzat?
	CY = cualificador & 0b00100000 == 32  # overflow?
	VH = cualificador & 0b00010000 == 16  # verificació horària durant el període?
	MP = cualificador & 0b00001000 == 8   # modificació de paràmetres durant el període?
	IN = cualificador & 0b00000100 == 4   # hi ha hagut intrusió durant el període?
	AL = cualificador & 0b00000010 == 2   # període incomplet per fallo d'alimentació durant el període?
	RES= cualificador & 0b00000001 == 1   # bit de reserva

	'''majúscules si bit=1, minúscules si bit=0'''
	IV  = 'IV'  if IV  else 'iv'
	CA  = 'CA'  if CA  else 'ca'
	CY  = 'CY'  if CY  else 'cy'
	VH  = 'VH'  if VH  else 'vh'
	MP  = 'MP'  if MP  else 'mp'
	IN  = 'IN'  if IN  else 'in'
	AL  = 'AL'  if AL  else 'al'
	RES = 'RES' if RES else 'res'

	'''fi'''
	print("        byte Cualificador: "+hex(cualificador)+": ["+str(IV)+","+str(CA)+","+str(CY)+","+str(VH)+","+str(MP)+","+str(IN)+","+str(AL)+","+str(RES)+"]")

'''Detecta errors emesos pel comptador. Es fa al final de processar tota la trama'''
def detectaError(trama):
	'''
		Detectar errors dins el protocol. Serveix per respostes, no per peticions
		trama: objecte bytearray
	'''
	n=len(trama)

	#comprova els bytes inicials
	if trama[0]==0x10:
		tipus="fix"
		control=trama[1]
	elif trama[0]==0x68 and trama[3]==0x68:
		tipus="var"
		control=trama[4]
	else: raise RuntimeError("bytes inicials incorrectes")

	#agafa el byte control, i mira si PRM=1. Ha de ser 0 (només mirem respostes)
	prm=control & 0b01000000 == 64
	if prm: return

	#agafa el byte control, i mira els 4 primers bits
	fun=control & 0b00001111
	if   fun==1: quit("NACK. COMANDA NO ACCEPTADA")
	elif fun==9: quit("NACK. DADES DEMANADES NO DISPONIBLES")

	#si la trama és fixa ja estem
	if tipus=="fix": return

	#si la trama és variable hem de mirar la causa de transmissió
	cdt=trama[7:n-2][0:6][2] & 0b00111111
	if   cdt==10: quit("FINALIZACIÓN DE LA ACTIVACIÓN")
	elif cdt==13: quit("REGISTRO DE DATOS SOLICITADO NO DISPONIBLE")
	elif cdt==14: quit("TIPO DE ASDU SOLICITADO NO DISPONIBLE")
	elif cdt==15: quit("NÚMERO DE REGISTRO EN EL ASDU ENVIADO POR CM DESCONOCIDO")
	elif cdt==16: quit("ESPECIFICACION DE DIRECCION EN EL ASDU ENVIADO POR CM DESCONOCIDA")
	elif cdt==17: quit("OBJETO DE INFORMACION NO DISPONIBLE")
	elif cdt==18: quit("PERIODO DE INTEGRACION NO DISPONIBLE")
	'''fi'''

#==#==#==#==#==#==#==#==#==#==#==#
#     T R A M E S   T E S T      #
#==#==#==#==#==#==#==#==#==#==#==#
'''trama buida'''
#processa('')
'''trames fixes: ok'''
#processa('\x10\x49\x01\x00\x4a\x16')
#processa('\x10\x0b\x01\x00\x0c\x16') 
'''trames variables, 2 tipus: integrados i lecturas'''
'''peticio de link i enviament de contrasenya'''
#processa("\x68\x0D\x0D\x68\x73\x58\x1B\xB7\x01\x06\x01\x00\x00\x4E\x61\xBC\x00\x10\x16")
'''integrados totales'''
#processa('\x68\x15\x15\x68\x73\x58\x1B\x7A\x01\x06\x01\x00\x0B\x01\x08\x00\x0B\x07\x02\x0A\x00\x11\x0A\x02\x0A\xC1\x16')
#processa('\x68\x3E\x3E\x68\x08\x58\x1B\x08\x08\x05\x01\x00\x0B\x01\x18\x01\x00\x00\x00\x02\x6E\x1F\x03\x00\x00\x03\x04\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x05\xCC\xBE\x00\x00\x00\x06\x98\x0D\x00\x00\x00\x07\x00\x00\x00\x00\x80\x08\x00\x00\x00\x00\x80\x00\x81\xB2\x09\x09\xE1\x16')
'''lecturas de cierre '''
#processa('\x68\x13\x13\x68\x73\x58\x1B\x86\x01\x06\x01\x00\x88\x00\x00\x01\x0A\x09\x00\x00\x01\x02\x0A\x1D\x16')
#processa('\x68\x48\x48\x68\x08\x58\x1B\x88\x01\x05\x01\x00\x88\x14\x61\x71\x00\x00\xE4\x25\x00\x00\x00\x0B\x47\x00\x00\x88\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x54\x00\x00\x00\x00\x0E\xBA\x0C\x08\x00\x00\x00\x00\x00\x80\x00\x00\x21\x0C\x08\x00\x00\x81\x01\x09\xD4\x16')
'''resposta real del comptador icra a A122 amb registre=21'''
#processa("\x68\x20\x20\x68\x08\x01\x00\x08\x03\x05\x01\x00\x15\x01\xe3\xc4\x7a\x00\x00\x02\x00\x00\x00\x00\x00\x03\xef\x9c\x08\x00\x00\x00\x80\xd5\x05\x10\x53\x16")
#processa("\x68\x15\x15\x68\x08\x01\x00\x7a\x01\x07\x01\x00\x15\x01\x02\x80\x00\x14\x05\x10\x80\x00\x17\x05\x10\xf9\x16")
'''resposta real ASDU 140 TODO'''
processa("\x68\x27\x27\x68\x08\x01\x00\xa3\x01\x05\x01\x00\x00\xc0\x2f\xcc\x7f\x00\x00\x00\x00\x00\x6f\xa0\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe6\x95\x15\x00\x1d\x80\x7c\x09\x10\xc6\x16")
