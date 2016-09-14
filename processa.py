#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Protocol IEC 60870-5-102
	Autor: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

	Mòdul per processar missatges (peticions i respostes)
	Testejat amb un comptador Actaris SL761

	Bibliografia: #TODO

	Els missatge provenen de la comanda serial.readlines()
	normalment sera un array de tamany 1

	Estructura global:

		* Processa missatge
			* fix
				* control
			* variable
				* control
				* asdu
					* iud
					* objectes
'''

def processa(missatge):
	'''transformar string (exemple: '\x10\x49\x01\x00\x4a\x16') a bytearray'''
	global buf #disponible a totes les funcions per agafar bits d'altres camps
	buf=bytearray(missatge)

	'''comptar numero de bytes del buffer'''
	n=len(buf) 

	print("<missatge>\n  "+str(n)+" bytes:"),

	'''mostra tots els bytes del missatge'''
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
'''fi'''

'''processa una trama fixa de 6 bytes'''
def processaTramaFixa(buf):
	''' 
		buf: objecte bytearray de tamany 6

		estructura:

				6        5      4   3      2        1
		+-------+---------+-------+----------+----+
		| inici | control | direc | checksum | fi |
		+-------+---------+-------+----------+----+
	'''
	n=len(buf)

	'''comprovacions'''
	if(n!=6): 
		raise RuntimeError('La trama no te longitud 6')
	if(buf[0]!=0x10 and buf[n-1]!=0x16): 
		raise RuntimeError('Bytes inici (0x10) i final (0x16) erronis')

	'''comprova checksum'''
	if(buf[1]+buf[2]+buf[3]==buf[4]):    
		print("  Checksum correcte ("+hex(buf[4])[2:4]+" = "+str(buf[4])+")")
	else:
		raise RuntimeError('Checksum erroni')

	print("  La trama es de tipus FIXE [inici (0x10), control, direccio1, direccio2, checksum, fi (0x16)]")

	'''processa el byte de control'''
	control=buf[1]
	campControl(control)

	'''2 bytes de direccio: ajuntar-los'''
	direccio = buf[3] << 8 | buf[2]
	print("  Direccio comptador: "+hex(direccio)[2:4]+" = "+str(direccio))
'''fi'''

'''processa una trama de llargada variable'''
def processaTramaVariable(buf):
	'''
		buf: objecte bytearray

		estructura:

		+--------------+------+------+--------------+---------+-----+------+----------+--------------+
		| Inici (0x68) | Long | Long | Inici (0x68) | Control | A A | ASDU | Checksum | Final (0x16) |
		+--------------+------+------+--------------+---------+-----+------+----------+--------------+
	'''
	n=len(buf)

	'''comprovacions'''
	if(buf[0]!=0x68 and buf[3]!=0x68 and buf[n-1]!=0x16): 
		raise RuntimeError("Bytes inici i final erronis")

	'''comprova que els dos bytes de longitud (Long) tinguin el mateix valor'''
	if(buf[1]!=buf[2]): 
		raise RuntimeError("Els bytes de longitud (2n i 3r) son diferents")

	'''comprova checksum'''
	checksum=0
	for i in range(4,n-2): checksum += buf[i]
	if(checksum % 256 == buf[n-2]): 
		print("  Checksum correcte ("+hex(buf[n-2])[2:4]+" = "+str(buf[n-2])+")")
	else:
		raise RuntimeError("Checksum incorrecte")

	print("  La trama es de tipus VARIABLE [inici (0x68), L, L, inici (0x68), ASDU, checksum, final (0x16)]")

	'''byte de control'''
	control=buf[4]
	campControl(control)

	'''bytes de direccio (2)'''
	direccio = buf[6] << 8 | buf[5]
	print("  Direccio comptador: "+str(hex(direccio))+" = "+str(direccio))

	'''ASDU: del byte 4 fins al el n-3'''
	ASDU=buf[7:n-2]

	'''Comprova si el camp longitud coincideix amb control+direccio+asdu'''
	if(buf[1]==3+len(ASDU)):
		print("  Camp longitud correcte ("+hex(buf[1])[2:4]+" = "+str(buf[1])+" = "+str(len(ASDU))+"+3)")
	else:
		raise RuntimeError("Camp Longitud ("+str(buf[1])+") incorrecte")
	
	campASDU(ASDU)
'''fi'''

'''processa el byte Control'''
def campControl(control):
	'''
			 8     7     6     5     4   3   2   1
		+-----+-----+-----+-----+-----------------+
		| RES | PRM | FCB | FCV |       FUN       | (si PRM=1)
		+-----+-----+-----+-----+-----------------+

		o bé

		+-----+-----+-----+-----+-----------------+
		| RES | PRM | ACD | DFC |       FUN       | (si PRM=0)
		+-----+-----+-----+-----+-----------------+
	'''

	if(control==0):
		raise RuntimeError('Camp de control no definit')

	print("  <control>")
	print("    Byte control: "+str(control)+" = "+hex(control)+" = "+bin(control))
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
	if(res): 
		raise RuntimeError("Bit de reserva no és 0")

	'''bit prm: direccio del missatge'''
	if(prm): print("    PRM = 1 : Aquest missatge es una PETICIO");
	else:    print("    PRM = 0 : Aquest missatge es una RESPOSTA");

	'''bits acd i dfc'''
	if(prm==False): 
		if(acd): 
			print("    ACD = 1 : Es permet l'acces a les dades de classe 1")
		else:
			print("    ACD = 0 : No es permet l'acces a les dades de classe 1 (ignorat per reglament REE)")

		if(dfc): 
			print("    DFC = 1. ELS MISSATGES FUTURS CAUSARAN DATA OVERFLOW")

	'''Mostra el text de la funcio "fun" (4 bits) '''

	if(prm):
		print({
			 0:"    [Funció 0] [Petició: RESET DEL LINK REMOT]",
			 3:"    [Funció 3] [Petició: ENVIAMENT DE DADES D'USUARI]",
			 9:"    [Funció 9] [Petició: SOL·LICITUD DE L'ESTAT DEL LINK]",
			11:"    [Funció 11] [Petició: SOL·LICITUD DE DADES DE CLASSE 2]",
		}[fun])
	else:
		print({
			 0:"    [Funció 0] [Resposta: ACK]",
			 1:"    [Funció 1] [Resposta: NACK. COMANDA NO ACCEPTADA]",
			 8:"    [Funció 8] [Resposta: DADES DE L'USUARI]",
			 9:"    [Funció 9] [Resposta: NACK. DADES DEMANADES NO DISPONIBLES]",
			11:"    [Funció 11] [Resposta: ESTAT DEL LINK O DEMANDA D'ACCÉS]",
		}[fun])
	print("  </control>")
'''fi'''

'''camp iud dins del camp ASDU'''
def campIUD(iud):
	'''
		iud: bytearray (6 bytes)

			 6     5     4     3   2   1
		+-----+-----+-----+-------------+
		| IDT | QEV | CDT |    DCO      |
		+-----+-----+-----+-------------+

		idt = identificador de tipus
		qev = qualificador d'estructura variable
		cdt = causa de transmissió
		dco = direcció comuna
	'''
	n=len(iud)
	print("    <iud>")
	print("      "+str(n)+" bytes: [idt, qev, cdt, dco]:"),

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
		102:"LEER REGISTRO DE INFORMACIÓN DE EVENTO (SINGLE-POINT) POR INTERVALO DE TIEMPO",
		103:"LEER FECHA Y HORA ACTUALES",
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

	'''byte qualificador estructura variable. Estructura: [SQ (1 bit), N (7 bits)]'''
	'''
		bit SQ:
			0 : Para cada objeto de información se indica su dirección
			1 : Se indica la dirección exclusivamente al primer objeto, siendo las direcciones del resto consecutivas.
		N: quantitat d'objectes d'informació
	'''
	SQ = qev & 0b10000000 == 128
	N  = qev & 0b01111111

	'''causa de transmissio (CDT) (1 byte). Estructura: [T (1 bit), PN (1 bit), causa (6 bits)]'''
	T     = cdt & 0b10000000 == 128 # bit "test" val 1 si la trama es un test
	PN    = cdt & 0b01000000 == 64  # bit PN: "confirmacio positiva" o "negativa"
	causa = cdt & 0b00111111

	dicc_causa={
			4 :'Inicializada',
			5 :'Peticion o solicitada (request or requested)',
			6 :'Activacion',
			7 :'Confirmacion de activacion',
			8 :'Desactivacion',
			9 :'Desactivacion confirmada',
			10:'Finalizacion de la activacion',
			13:'Registro de datos solicitado no disponible',
			14:'Tipo de ASDU solicitado no disponible',
			15:'Número de registro en el ASDU enviado por CM desconocido',
			16:'Especificacion de direccion en el ASDU enviado por CM desconocida',
			17:'Objeto de informacion no disponible',
			18:'Periodo de integracion no disponible',
	}

	'''direccio comuna (DCO) (3 bytes). Estructura : [punt_mesura (2 bytes), registre (1 byte) ]'''
	dco_punt_mesura = dco[1] << 8 | dco[0]
	dco_registre    = dco[2]

	dicc_registre = {
			  0 :"Dirección de defecto",
			 11 :"Totales integrados con período de integración 1 (curva de carga)",
			 12 :"RESERVA. [Posible uso futuro para Totales integrados con período de integración 2(curva de carga, habitualmente cuartohoraria)].  ",
			 13 :"RESERVA. [Posible uso futuro para Totales integrados con período de integración 3(curva de carga)] ",
			 21 :"Totales integrados (valores diarios) con período de integración 1 (resumen diario)",
			 22 :"RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con período de integración 2 (resumen diario)]",
			 23 :"RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con período de integración 3 (resumen diario)] ",
			 52 :"Información de evento (single-point), sección 1: incidencias de arranques y tensión bajo límites ",
			 53 :"Información de evento (single-point), sección 2: incidencias de sincronización y cambio de hora ",
			 54 :"Información de evento (single-point), sección 3: incidencias de cambio de parámetros ",
			 55 :"Información de evento (single-point), sección 4: errores internos ",
			128 :"Información de evento (single-point), sección 5: incidencias de intrusismo ",
			129 :"Información de evento (single-point), sección 6: incidencias de comunicaciones ",
			130 :"Información de evento (single-point), sección 7: incidencias de clave privada ",
			131 :"Información de evento (single-point), sección 8: incidencias de Contrato I ",
			132 :"Información de evento (single-point), sección 9: incidencias de Contrato II ",
			133 :"Información de vento (single-point), sección 10: incidencias de Contrato III ",
			134 :"Información de Tarificación relativa al Contrato I",
			135 :"Información de Tarificación relativa al Contrato II",
			136 :"Información de Tarificación relativa al Contrato III",
			137 :"Información de Tarificación relativa al Contrato Latente I",
			138 :"Información de Tarificación relativa al Contrato Latente II",
			139 :"Información de Tarificación relativa al Contrato Latente III",
	}
      
	''' mostra informació de tot el iud desglossat'''
	print("      idt: "+hex(idt)+" = tipus "+str(idt)+" : "+dicc_idt[idt])
	print("      qev: "+hex(qev)+" = "+bin(qev)+": [SQ="+str(SQ)+", N="+str(N)+" objectes d'informació]")
	print("      cdt: "+hex(cdt)+": [T="+str(T)+", PN="+str(PN)+", causa="+str(causa)+" : "+dicc_causa[causa]+"]")
	print("      dco (3 bytes): [punt mesura (2 bytes), direccio registre (1 byte)] = "+str(map(hex,dco)))
	print("        * punt mesura: "+str(dco_punt_mesura))
	print("        * direccio registre: "+str(dco_registre)+" = "+dicc_registre[dco_registre])
	print("    </iud>")
'''fi'''

'''processa camp ASDU, dins trama variable'''
def campASDU(ASDU):
	'''
		ASDU: objecte bytearray

          6 bytes
		+----------------------------+---------------------+-----------------------------------+
		|  id unitat de dades (iud)  | information objects | etiqueta de temps comu (opcional) |
		+-----+-----+-----+----------+---------------------+-----------------------------------+

	'''
	n=len(ASDU)
	print("  <asdu>")
	print('    '+str(n)+' bytes:'),
	for i in range(len(ASDU)): print hex(ASDU[i])[2:4], 
	print('')

	'''iud'''
	iud=ASDU[0:6]
	campIUD(iud)

	'''objectes informacio'''
	objsInfo=ASDU[6:n]
	campObjsInfo(objsInfo)

	'''etiqueta de temps comú'''
	# NO ESTÀ CLAR

	print("  </asdu>")
'''fi'''

def campObjsInfo(objsInfo):
	'''
		objsInfo: objecte bytearray

		estructura:

			1 byte
		+----------+---------------+-------------------+
		| direccio | elements info | etiqueta de temps |
		+----------+---------------+-------------------+
	'''
	n=len(objsInfo)
	print("    <objectesInfo>\n      "+str(n)+" bytes:"),

	'''mostra tots els bytes'''
	for i in range(n): print hex(objsInfo[i])[2:4],
	print("")

	'''quants objectes info hi ha? (7 bits "N" del byte QEV del camp IUD del camp ASDU)
	N=[     ASDU      ][IUD][QEV] & 7 bits    '''
	N=buf[7:len(buf)-2][0:6][ 1 ] & 0b01111111
	print("      N = "+str(N)+" objectes d'informació de "+str(n/N)+" bytes")

	'''el residu entre n/N ens dona la llargada de l'etiqueta de temps comuna'''
	longitud_etiqueta = n % N
	if(longitud_etiqueta>0):
		if(longitud_etiqueta==5): print("      Amb Etiqueta comuna de 5 bytes (tipus a)")
		if(longitud_etiqueta==7): print("      Amb Etiqueta comuna de 7 bytes (tipus b)")
		if(longitud_etiqueta not in [5,7]): raise RuntimeError('Etiqueta erronia')
	else:
		print("      Sense etiqueta comuna de temps")

	'''itera els elements'''
	for i in range(N):
		inici = 0+i*(n/N) #posicio del byte inicial
		final = n/N*(i+1) #posició del byte final
		objInfo=objsInfo[inici:final] #talla l'array
		campObjInfo(objInfo)

	'''processa etiqueta si n'hi ha'''
	if(longitud_etiqueta):
		etiquetaTemps=objsInfo[n-longitud_etiqueta:n]
		campEtiquetaTemps(etiquetaTemps)

	print("    </objectesInfo>")
	'''fi'''

'''mostra un sol element d'informació'''
def campObjInfo(objInfo):
	'''
		objInfo: classe bytearray
		estructura:

			| direccio objecte | element |
	'''
	n=len(objInfo)
	print("      <objecte>"),

	'''mostra tots els bytes'''
	for i in range(n): print hex(objInfo[i])[2:4],
	print("")

	'''byte 1: direccio'''
	direccio=objInfo[0]
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
	print("        Direccio "+hex(direccio)[2:4]+": "+dicc_direccio[direccio])

	'''si tipus ASDU==8, 4 bytes per energia: suma'ls '''
	'''
	idt=[    A S D      ][iud][idt] '''
	idt=buf[7:len(buf)-2][0:6][ 0 ]

	if(idt==8):
		nrg       = objInfo[1:5]
		nrg_valor = nrg[3] << 32 | nrg[2] << 16 | nrg[1] << 8 | nrg[0]
		# cal sumar aquests bytes!!!!!
		print("        Energia: "+str(nrg_valor)+" (kWh o kVARh)")
		'''byte cualificador: 8 bits '''
		cualificador = objInfo[5]
		IV = cualificador & 0b10000000 == 128 # la lectura es vàlida?
		CA = cualificador & 0b01000000 == 64  # el comptador està sincronitzat?
		CY = cualificador & 0b00100000 == 32  # overflow?
		VH = cualificador & 0b00010000 == 16  # verificació horària durant el període?
		MP = cualificador & 0b00001000 == 8   # modificació de paràmetres durant el període?
		IN = cualificador & 0b00000100 == 4   # hi ha hagut intrusió durant el període?
		AL = cualificador & 0b00000010 == 2   # període incomplet per fallo d'alimentació durant el període?
		RES= cualificador & 0b00000001 == 1   # bit de reserva
		print("        byte Cualificador: "+hex(cualificador)+" : [IV="+str(IV)+",CA="+str(CA)+",CY="+str(CY)+",VH="+str(VH)+",MP="+str(MP)+",IN="+str(IN)+",AL="+str(AL)+",RES="+str(RES)+"]")
	elif(idt==122):
		direccio2=objInfo[1]
		print("        Direccio última: "+str(direccio2)+": "+dicc_direccio[direccio2])

		'''etiqueta de temps inicial'''
		etiquetaInicial = objInfo[2:7]
		campEtiquetaTemps(etiquetaInicial)
		'''etiqueta de temps final'''
		etiquetaFinal = objInfo[7:12]
		campEtiquetaTemps(etiquetaFinal)

	else:
		print("        **** tipus no implementat encara")


	print("      </objecte>")
	'''fi'''

def campEtiquetaTemps(etiqueta):
	'''
		etiqueta: classe bytearray
		pot ser de tipus a (5 bytes) o tipus b (7 bytes)
	'''
	n=len(etiqueta)

	'''comprova el tipus d'etiqueta de temps'''
	if(n==5): tipus="a"
	elif(n==7): tipus="b"
	else: raise RuntimeError("Etiqueta de temps desconeguda")

	if tipus=="b":
		print("          Etiqueta Tipus b encara no implementada")
		return

	'''mostra l'etiqueta'''
	print("        <etiqueta> tipus "+tipus+" ("+str(n)+" bytes):"),
	for i in range(n): print hex(etiqueta[i])[2:4],
	print('')

	'''desglossa els 5 bytes = 40 bits'''
	'''
			 1-6     7     8   9-13   14-15   16    17-21     22-24     25-28   29-30   31-32   33-39    40
		+-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
    | minut | TIS | IV | hora |  RES1 | SU | diames | diasemana |  mes  |  ETI  |  PTI  |  year | RES2 |
    +-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
	'''
	minut     = etiqueta[0] & 0b11111100 >> 2 
	TIS       = etiqueta[0] & 0b00000010 == 2
	IV        = etiqueta[0] & 0b00000001 
	hora      = etiqueta[1] & 0b11111000 >> 3
	RES1      = etiqueta[1] & 0b00000110 >> 1
	SU        = etiqueta[1] & 0b00000001
	diames    = etiqueta[2] & 0b11111000 >> 3
	diasemana = etiqueta[2] & 0b00000111 
	mes       = etiqueta[3] & 0b11110000 >> 4
	ETI       = etiqueta[3] & 0b00001100 >> 2
	PTI       = etiqueta[3] & 0b00000011
	year      = etiqueta[4] & 0b11111110 >> 1
	RES2      = etiqueta[4] & 0b00000001

	'''completa l'any'''
	year+=2000

	'''posa un zero davant els dies, mesos, hores i minuts més petits de 10'''
	if(diames<10): diames="0"+str(diames)
	if(mes<10):    mes="0"+str(mes)
	if(hora<10): hora="0"+str(hora)
	if(minut<10): minut="0"+str(minut)

	'''mostra'''
	print("          Data: "+str(diames)+"/"+str(mes)+"/"+str(year)+", "+str(hora)+":"+str(minut))
	print("        </etiqueta>")

#==# #==# #==# #==# #==# #==# #==#
'''TRAMES TEST'''
'''FIXES 
pregunta='\x10\x49\x01\x00\x4a\x16'; processa(pregunta)
resposta='\x10\x0b\x01\x00\x0c\x16'; processa(resposta)
'''

'''VARIABLES'''

'''integrados totales
'''
pregunta='\x68\x15\x15\x68\x73\x58\x1B\x7A\x01\x06\x01\x00\x0B\x01\x08\x00\x0B\x07\x02\x0A\x00\x11\x0A\x02\x0A\xC1\x16'
processa(pregunta)
'''
resposta='\x68\x3E\x3E\x68\x08\x58\x1B\x08\x08\x05\x01\x00\x0B\x01\x18\x01\x00\x00\x00\x02\x6E\x1F\x03\x00\x00\x03\x04\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x05\xCC\xBE\x00\x00\x00\x06\x98\x0D\x00\x00\x00\x07\x00\x00\x00\x00\x80\x08\x00\x00\x00\x00\x80\x00\x81\xB2\x09\x09\xE1\x16'
processa(resposta)
'''

'''lecturas de cierre
pregunta='\x68\x13\x13\x68\x73\x58\x1B\x86\x01\x06\x01\x00\x88\x00\x00\x01\x0A\x09\x00\x00\x01\x02\x0A\x1D\x16'
processa(pregunta)
resposta='\x68\x48\x48\x68\x08\x58\x1B\x88\x01\x05\x01\x00\x88\x14\x61\x71\x00\x00\xE4\x25\x00\x00\x00\x0B\x47\x00\x00\x88\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x54\x00\x00\x00\x00\x0E\xBA\x0C\x08\x00\x00\x00\x00\x00\x80\x00\x00\x21\x0C\x08\x00\x00\x81\x01\x09\xD4\x16'
processa(resposta)
'''
