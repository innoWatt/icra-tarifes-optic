import time
import socket

class Comptador:

    def __init__(self):
        global direccioContador
        direccioContador = 1

        global psw
        psw = 1

        #nou TCP SOCKET
        global sock
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("192.168.103.63", 3333))

        global tFixaNoms
        tFixaNoms=['Inici','Control C','Direccio 1','Direccio 2','checksum','fi']

        global tVariableNoms
        tVariableNoms=['Inici1','Longitud1','Longitud2','Inici2','Control C','Direccio 1','Direccio 2','Id.Tipo','SQ N','Causa','PM 1','PM 2','dir.reg','         ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ']

        global tVariableNomsClauAcces
        tVariableNomsClauAcces=['Inici1','Longitud1','Longitud2','Inici2','Control C','Direccio 1','Direccio 2','Id.Tipo','SQ N','Causa','P.Medida','dir.reg1','dir.reg2','X Clau1','X Clau2','Clau3','Clau4','checksum','fi']

        #tFixa=[0x10, None, 0x01, 0x00, None, 0x16]
        global tVariable
        tVariable=[None]

        global valorsTrama
        valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])

        global tempsImpres
        tempsImpres = False

    '''
        tipus 1: Mostrejat simple, en una sola linia sense descodificar camps
        tipus 2: Mostrejat en columna, en etiqueta al costat de cada camp
        tipus 3: Mostrejat en descodificat, nomes la informacio rellevant
    '''
    def imprimeixTrama(self,capcalera,trama,tipus):

        if type(tipus) != int:
            raise RuntimeError("Tipus no es un enter");
            
        if (tipus < 1 or tipus > 3):
            raise RuntimeError("Tipus te el valor = ",tipus);

        if type(trama) == list:
            raise RuntimeError("Trama no es una list");

        if len(trama) == 0:
            raise RuntimeError("Trama buida, possible TimeOut de rebuda de dades del port serie")

        if tipus == 1:
            print(capcalera),
            for i in range(len(trama)):
                print(trama[i],end="  ")
            print('')

        elif tipus == 2:
            if len(trama)==6:
                for i in range(6):
                    print(capcalera,'Byte',i,'-',tFixaNoms[i],'\t',trama[i],'\t',format(trama[i],'#04X'))
            else:
                for i in range(len(trama)):
                    print(capcalera,'Byte',i,'-',tVariableNoms[i],'\t',trama[i],'\t',format(trama[i], '#04X'))

        elif tipus == 3:
            if len(trama) == 6:
                print(capcalera, bcolors.OKBLUE, 'Valor CC:', format(trama[1], '#04X'), decodificaC(trama[1]), bcolors.ENDC)
            else:
                print(capcalera, end = " ")
            for i in range(len(trama)):
                if i == 7:
                    print(bcolors.OKBLUE, end = " ")
                if i == 13:
                    print(bcolors.OKGREEN, end = " ")
                if i == len(trama) - 2:
                    print(bcolors.ENDC, end = " ")
                    print(format(trama[i], '#04X'), end = " ")
                    print("")
                    print(bcolors.OKBLUE,'CCC:', trama[4], format(trama[4], '#04X'), decodificaC(trama[4]), bcolors.ENDC)
                    print('ASDU:', trama[7], format(trama[7], '#04X'), decodificaASDU(trama[7]))
                    print('Quantitat de Obj. Info:', trama[8])
                    print(bcolors.OKGREEN, 'Causa:', trama[9], format(trama[9], '#04X'),  decodificaCausa(trama[9]), bcolors.ENDC)
                    print('Direccio comu del ASDU', trama[12], format(trama[12], '#04X'), decodificaDireccio(trama[12]))
                    print('Objeto de Info:', '\t', trama[13],  format(trama[13], '#04X'), decodificaObjecte(trama[13]))
            print('')

def decodificaObjecte(self,valor):

    if type(valor) != int:
        raise RuntimeError("tipus objecte no es int")

    if valor < 1 and valor > 20:
        raise RuntimeError("objecte no val entre 1 i 20, val ",valor)

    if valor >= 12 and valor <= 19:
        return 'Reservados para futuras ampliaciones del Protocolo'

    dic={
        1: 'Totales Integrados de Activa Entrante',
        2: 'Totales Integrados de Activa Saliente',
        3: 'Totales Integrados de Reactiva primer cuadrante',
        4: 'Totales Integrados de Reactiva segundo cuadrante',
        5: 'Totales Integrados de Reactiva tercer cuadrante',
        6: 'Totales Integrados de Reactiva cuarto cuadrante',
        7: 'Datos de reserva 1',
        8: 'Datos de reserva 2',
        9: 'Bloque de totales integrados genérico con datos de reserva(Punto de medida con direcciones de objeto 1 al 8)',
        10:'Bloque de totales integrados genérico sin datos de reserva(Punto de medida con de direcciones de objeto 1 al 6)',
        11:'Bloque de totales integrados de consumo puro sin reservas (Punto de medida con direcciones de objeto 1, 3 y 6)',
        20:'Información de Tarificación (Totales)',
        21:'Información de Tarificación (período tarifario 1)',
        22:'Información de Tarificación (período tarifario 2)',
        23:'Información de Tarificación (período tarifario 3)',
        24:'Información de Tarificación (período tarifario 4)',
        25:'Información de Tarificación (período tarifario 5)',
        26:'Información de Tarificación (período tarifario 6)',
        27:'Información de Tarificación (período tarifario 7)',
        28:'Información de Tarificación (período tarifario 8)',
        29:'Información de Tarificación (período tarifario 9)',
    }
    return dic[valor];

def decodificaDireccio(self,valor):
    if valor >= 140 and valor <= 199:
        return 'Reservados para versiones futuras del protocolo RM–CM'

    if valor >= 200 and valor <= 255:
        return 'Uso libre para cada fabricante'

    dic={
        0:'Direccion de defecto',
        11:'Totales integrados con periodo de integracion 1 (curva de carga)',
        12:'RESERVA. [Posible uso futuro para Totales integrados con periodo de integracion 2(curva de carga, habitualmente cuartohoraria)].',
        13:'RESERVA. [Posible uso futuro para Totales integrados con periodo de integracion 3(curva de carga)]',
        21:'Totales integrados (valores diarios) con periiodo de integracion 1 (resumen diario)',
        22:'RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con periodo de integracion 2 (resumen diario)]',
        23:'RESERVA. [Posible uso futuro para Totales integrados (valores diarios) con periodo de integracion 3 (resumen diario)]',
        52:'Informacion de evento (single-point), seccion 1: incidencias de arranques y tension bajo limites',
        53:'Informacion de evento (single-point), seccion 2: incidencias de sincronizacion y cambio de hora',
        54:'Informacion de evento (single-point), seccion 3: incidencias de cambio de paraametros',
        55:'Informacion de evento (single-point), seccion 4: errores internos',
        128:'Informacion de evento (single-point), seccion 5: incidencias de intrusismo',
        129:'Informacion de evento (single-point), seccion 6: incidencias de comunicaciones',
        130:'Informacion de evento (single-point), seccion 7: incidencias de clave privada',
        131:'Informacion de evento (single-point), seccion 8: incidencias de Contrato I',
        132:'Informacion de evento (single-point), seccion 9: incidencias de Contrato II',
        133:'Informacion de vento (single-point), seccion 10: incidencias de Contrato III',
        134:'Informacion de Tarificacion relativa al Contrato I',
        135:'Informacion de Tarificacion relativa al Contrato II',
        136:'Informacion de Tarificacion relativa al Contrato III',
        137:'Informacion de Tarificacion relativa al Contrato Latente I',
        138:'Informacion de Tarificacion relativa al Contrato Latente II',
        139:'Informacion de Tarificacion relativa al Contrato Latente III',
    }
    return dic[valor]

def decodificaCausa(self,valor):
    if valor>=48 and valor<=52:
        return 'Reservados para versiones futuras del protocolo RM–CM'

    if valor>=53 and valor<=63:
        return 'Uso libre para cada fabricante'

    dic={
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
    return dic[valor]

def decodificaASDU(self,valor):
    if valor>=150 and valor<=179:
        return 'Reservados para versiones futuras del protocolo RM–CM'

    if valor>=191 and valor<=199:
        return 'Reservados para versiones futuras del protocolo RM–CM'

    if valor>=200 and valor<=255:
        return 'Uso libre para cada fabricante'

    dic={
        1:'Informacion de evento (single-point) con etiqueta de tiempo. Se empleara en la transmision de incidencias   M_SP_TA_2',
        8:'Totales integrados operacionales, 4 octetos (lecturas de contadores absolutos, en kWh o kVARh) M_IT_TG_2',
        11:'Totales integrados operacionales repuestos periodicamente, 4 octetos (incrementos de energia, en kWh o kVARh) M_IT_TK_2',
        71:'Identificador de fabricante y equipo. En lugar de un codigo de producto se enviara un identificador de equipo P_MP_NA_2',
        72:'Fecha y hora actuales M_TI_TA_2',
        100:'Leer identificador de fabricante y equipo C_RD_NA_2',
        102:'Leer registro de informacion de evento (single-point) por intervalo de tiempo C_SP_NB_2',
        103:'Leer fecha y hora actuales C_TI_NA_2',
        122:'Leer totales integrados operacionales por intervalo de tiempo y rango de direcciones C_CI_NT_2',
        123:'Leer totales integrados operacionales repuestos periodicamente por intervalo de tiempo y rango de direcciones C_CI_NU_2',
        128:'Firma electronica de los totales integrados (lecturas) M_DS_TA_2',
        129:'Parametros del punto de medida P_ME_NA_2',
        130:'Firma electronica de los totales integrados repuestos periodicamente (incrementos de energia) M_DS_TB_2',
        131:'Fechas y horas de cambio de horario oficial M_CH_TA_2',
        132:'Carga de Clave Privada de Firma C_PK_2',
        133:'Leer Informacion de Tarificacion (Valores en Curso) C_TA_VC_2',
        134:'Leer Informacion de Tarificacion (Valores Memorizados) C_TA_VM_2',
        135:'Informacion de Tarificacion (Valores en Curso) M_TA_VC_2',
        136:'Informacion de Tarificacion (Valores Memorizados) M_TA_VM_2',
        137:'Cerrar Periodo de Facturacion C_TA_CP_2',
        138:'Reservado para versiones futuras del protocolo RM-CM',
        139:'Bloques de totales integrados operacionales (lecturas de contadores absolutos, en kWh o kVARh) M_IB_TG_2',
        140:'Bloques de totales integrados operacionales repuestos de energia periodicamente (incrementos de energia en kWh o kVARh) M_IB_TK_2',
        141:'Leer la configuracion del equipo RM. C_RM_NA_2',
        142:'Envio de la configuracion del equipo RM. M_RM_NA_2',
        143:'Modificacion de la configuracion de los puertos de comunicaciones. C_MR_NA_2',
        144:'Lectura de potencias de contrato. C_PC_NA_2',
        145:'Envio de potencias de contrato. M_PC_NA_2',
        146:'Modificacion de potencias de contrato. C_MC_NA_2',
        147:'Lecturas de dias festivos. C_DF_NA_2',
        148:'Envio de dias festivos M_DF_NA_2',
        149:'Modificacion de dias festivos C_MF_NA_2',
        180:'Leer firma electronica de los totales integrados por intervalo de tiempo (lecturas) C_DS_TA_2',
        181:'Cambiar fecha y hora C_CS_TA_2',
        182:'Leer los parametros del punto de medida C_PI_NA_2',
        183:'Iniciar sesion y enviar clave de acceso C_AC_NA_2',
        184:'Leer firma electronica de los totales integrados repuestos periodicamente, por intervalo de tiempo (incrementos de energia) C_DS_TB_2',
        185:'Leer fechas y horas de cambio de horario oficial C_CH_TA_2',
        186:'Modificar fechas y horas de cambio de horario oficial C_MH_TA_2',
        187:'Finalizar sesion C_FS_NA_2',
        188:'Reservado para versiones futuras del protocolo RM-CM',
        189:'Leer bloques de totales integrados operacionales por intervalo de tiempo y dirección C_CB_NT_2',
        190:'Leer bloques de totales integrados operacionales repuestos periodicamente por intervalo de tiempo y direccion C_CB_NU_2',
    }
    return dic[valor]

def decodificaC(self, valor):

    if type(valor) != int:
        raise RuntimeError('valor no es un int')

    # "valor" és un byte (8 7 6 5 4 3 2 1)

    cadena1 = ''
    cadena2 = ''
    cadena3 = ''


    #mirar si el bit 7 es igual a 1
    if (valor) & 64 == 64:

        #comprovar els 4 bits (LSB)
        if valor & 0b1111 == 0:
            cadena1 = 'El Master diu: Reposicion del enlace remoto'

        #comprovar els 3 bits (LSB)
        elif valor& 0b1111 == 3:
            cadena1 = 'El Master diu: Envio de datos de usuario'

        elif (valor) & 0b1111 == 9:
            cadena1 = 'El Master diu: Solicitud de estado del enlace'

        elif (valor) & 0b1111 == 11:
            cadena1 = 'El Master diu: Solicitud de datos clase 2'
        elif (valor) & 64 == 0:
            if (valor) & 0b1111 == 0:
                cadena1 = 'L\'esclau diu: ACK. Reconeixament positiu'
            elif (valor) & 0b1111 == 1:
                cadena1 = 'L\'esclau diu: NACK. Comanda no acceptada'
            elif (valor) & 0b1111 == 8:
                cadena1 = 'L\'esclau diu: Datos de usuario'
            elif (valor) & 0b1111 == 9:
                cadena1 = 'L\'esclau diu: NACK. Datos solicitados no disponibles'
            elif (valor) & 0b1111 == 11:
                cadena1 = 'L\'esclau diu: Estado de enlace o demanda de acceso'

    if (valor) & 16 == 16:
        cadena2 = 'FCV=1/DFC=1 Els futurs missatges caursaran Overflow'
    else:
        cadena2 = 'FCV=0/DFC=0 S\'accepten futurs missatges'

    if (valor) & 32 == 32:
        cadena3 = 'FCB=1(bit alternant per cada transisio del master)/DFC=1 Acces a dades classe 1'
    else:
        cadena3 = 'FCB=0(bit alternant per cada transisio del master)/DFC=0 No acces a dades de classe 1'

    return cadena1, cadena2, cadena3


def calculChecksum(self,trama):
    checksum = 0
    if len(trama)==6:
        for i in range(1,4):
            checksum += trama[i]
    else:
        for i in range(4,len(trama)-2):
            checksum = checksum + trama[i]

    return checksum % 256


def llegeixTrama(self):
    varx=''
    checksum=0
    capcalera=sock.recv(1)

    if len(capcalera) > 0: #si hem rebut algun caracter

			if ord(capcalera) == 0x10: #en cas que sigui tFixa:
				varx=sock.recv(5)

			if len(varx) == 5:
				trama=list(capcalera + varx)

			for i in range(len(trama)):
			if type(trama[i]) == str:
			trama[i] = ord(trama[i])
			checksum = self.calculChecksum(trama)
			if trama[5] != 0x16: #comprovar ultim caracter
				print("ERROR en la funcio llegeixTrama():")
				print("L'ultim caracter de la trama no es 0x16 sino", (trama[5]))
				print(trama)
				trama = []
				return trama

			if checksum != (trama[4]): #comprovar checksum
				print("ERROR en la funcio llegeixTrama():")
				print("El Checksum no coincideix amb la informacio de la trama")
				print(trama)
				print('esperat:', checksum)
				print('obtingut:', (trama[4]))
				trama = []
				return trama

			#en cas que la capçalera, el final i el checksum siguin correctes envia:
			return trama

    elif len(varx) != 5:
    print("ERROR en la funcio llegeixTrama():")
    print("S\'esperava un paquet de 6 bytes i n'hem rebut:", len(varx))
    print(trama)
    trama = []
    return trama

    else:
    print("ERROR en la funcio llegeixTrama():")
    print("S'ha rebut una longitud de trama que no es ni 6, ni 0")
    print(trama)
    trama = []
    return trama

    elif ord(capcalera) == 0x68: #en cas de tVarialbe:
    longitud1=sock.recv(1)
    longitud2=sock.recv(1)
    if longitud1 != longitud2:
    print("ERROR en la funcio llegeixTrama():")
    print('Els bytes de longitud de tVariable no coincideixen entre ells')
    varx=sock.recv(ord(longitud1)+3)
    trama = list(capcalera+longitud1+longitud2+varx)
    for i in range(len(trama)):
    if type(trama[i]) == str:
    trama[i] = ord(trama[i])
    if trama[len(trama) - 1] != 0x16:
    print('ERROR en la funcio llegeixTrama():')
    print("L'ultim byte de la trama variable no val 0x16")
    trama = []
    return trama
    checksum = self.calculChecksum(trama)
    if checksum != trama[len(trama) - 2]:
    print('ERROR en la funcio llegeixTrama():')
    print("El Checksum de trama variable no coincideix")
    trama = []
    return trama
    if (len(trama) - 6) != ord(longitud1):
    print('ERROR en la funcio llegeixTrama():')
    print('El byte de longitud de tVariable', ord(longitud1))
    print("no coincideix amb la longitud real de la tVariable", len(trama) - 6)
    print(trama)
    trama = []
    return trama
    return trama #en cas que sigui tot correcte envia la trama omplerta

    elif len(capcalera) == 0: #no hem rebut cap caracter
    trama = []
    return trama

    else:
    print('errror raro a llegeixTrama()')
    trama = []
    return trama

def desmontaTrama(self, trama):
    if type(trama) != list:
        raise RuntimeError("la trama no es una llista")

    valors = dict(imprimeix='',tipus='',longitud=0,ccc=0,direccioContador=0,idASDU=0,SQN=0,causa=0,direccioPM=0,direccioRegistre=0,objecteInformacio1=[None],checksum=0,fi=0)

    if (trama[0]) == 0x10:
        valors['tipus']    = 'f'
        valors['ccc']      = trama[1]
        valors['checksum'] = trama[len(trama) - 2]
        valors['fi']       = trama[len(trama) - 1]
        return valors

    elif (trama[0]) == 0x68:
        valors['tipus']              = 'v'
        valors['logitud']            = trama[1]
        valors['ccc']                = trama[4]
        valors['idASDU']             = trama[7]
        valors['SQN']                = trama[8]
        valors['causa']              = trama[9]
        valors['direccioPM']         = (trama[10] + 256) + trama[11]
        valors['direccioRegistre']   = trama[12]
        valors['objecteInformacio1'] = list(trama[13:len(trama)-2])
        valors['checksum']           = trama[len(trama) - 2]
        valors['fi']                 = trama[len(trama) - 1]
        return valors

    valors['tipus'] = None
    valors['logitud'] = None
    valors['ccc'] = None
    valors['idASDU'] = None
    valors['SQN'] = None
    valors['causa'] = None
    valors['direccioPM'] = None
    valors['direccioRegistre'] = None
    valors['objecteInformacio1'] = None
    valors['checksum'] = None
    valors['fi'] = None
    return valors

def enviaTrama(self, trama):
    for i in range(len(trama)):
        time.sleep(1000000)
        sock.send(bytes(trama))
        sock.flush() # it is buffering. required to get the data out *now

def muntaTrama(self,valors):
    if valors['tipus'] == 'f':
        trama = [None] * 6
        trama[0] = 0x10 #byte inici de trama
        trama[1] = valors['ccc']
        trama[2] = valors['direccioContador'] % 100 #0x01
        trama[3] = int(valors['direccioContador'] / 100) #0x00
        trama[4] = self.calculChecksum(trama) #li afegim el checksum
        trama[5] = 0x16 #byte fi de trama
        return(trama)
    elif valors['tipus'] == 'v':
        trama = [None] * 13
        trama[0] = 0x68 #es una trama tipus variable
        trama[3] = 0x68 #inici trama2
        trama[4] = valors['ccc']
        trama[5] = valors['direccioContador'] % 100 #0x01
        trama[6] = int(valors['direccioContador'] / 100) #0x00
        trama[7] = valors['idASDU']
        trama[8] = valors['SQN']
        trama[9] = valors['causa']
        trama[10] = 0x01 #PM part baixa
        trama[11] = 0x00 #PM part alta
        trama[12] = valors['direccioRegistre']
        if len(valors['objecteInformacio1']) > 0:
        trama.extend(valors['objecteInformacio1'])
        trama.extend([0]) #checksum
        trama.extend([0x16]) #fi
        trama[1] = len(trama) - 6
        trama[2] = trama[1]
        trama[len(trama) - 2] = self.calculChecksum(trama)
        return(trama)
    else:
        raise RuntimeError("valors['tipus'] erroni")

def envia(self,valors,imprimeix_enviament,imprimeix_rebuda):
    trama = self.muntaTrama(valors)
    self.imprimeixTrama('pc-->',trama,imprimeix_enviament)
    self.enviaTrama(trama)
    trama = self.llegeixTrama()
    self.imprimeixTrama('pc<--',trama,imprimeix_rebuda)
    return self.desmontaTrama(trama)

def llegirInstantanis(self):

	self.diccionari = {
			"Data":0,
			"Hora":0,
			"kWh Activa Importacio":0,
			"kWh Activa Importacio Error":0,
			"kWh Activa Exportacio":0,
			"kWh Activa Exportacio Error":0,
			"KVArh Reactiva Q1":0,
			"KVArh Reactiva Q1 Error":0,
			"KVArh Reactiva Q2":0,
			"KVArh Reactiva Q2 Error":0,
			"KVArh Reactiva Q3":0,
			"KVArh Reactiva Q3 Error":0,
			"KVArh Reactiva Q4":0,
			"KVArh Reactiva Q4 Error":0,
			"Potencia Activa Total KW":0,
			"Potencia Reactiva Total KVAr":0,
			"Factor de potencia total (en milessimes)":0,
			"P. Activa total es importada":0,
			"P.Reactiva total es Q1/Q2":0,
			"P.Reactiva total es Q1/Q2 Error":0,
			"P.Activa Fase I KW":0,
			"P.Reactiva Fase I KVAr":0,
			"Factor de Potencia (cos phi). Fase I (en milessimes)":0,
			"La P. Activa Fase I es importada":0,
			"P.Reactiva Fase I es Q1/Q2":0,
			"Error de lectura en P.Total Fase I invalides":0,
			"P.Activa Fase II KW":0,
			"P.Reactiva Fase II KVAr":0,
			"Factor de Potencia (cos phi). Fase II (en milessimes)":0,
			"P. Activa Fase II es importada":0,
			"P.Reactiva Fase II es Q1/Q2":0,
			"Error de lectura P.Total Fase II":0,
			"P.Activa Fase III KW":0,
			"P.Reactiva Fase III KVAr":0,
			"Factor de Potencia (cos phi). Fase III (en milessimes)":0,
			"La P. Activa Fase III es importada":0,
			"P.Reactiva Fase III es Q1/Q2":0,
			"Error de Lectrua en P.Total Fase III":0,
			"Intensitat Fase I (decimes de A)":0,
			"Tensio Fase I (decimes de V)":0,
			"Error de Lectura mesures de Fase I":0,
			"Intensitat Fase II (decimes de A)":0,
			"Tensio Fase II (decimes de V)":0,
			"Error de Lectura de mesures de Fase II":0,
			"Intensitat Fase III (decimes de A)":0,
			"Tensio Fase III (decimes de V)":0,
			"Error de Lectura de les mesures de la Fase III":0,
	}

	#====(12 i 13)
	valorsTrama=dict(tipus='',ccc=0,direccioContador=0,idASDU=0,SQN=0,causa=0,direccioPM=0,direccioRegistre=0,objecteInformacio1=[None])
	valorsTrama['direccioContador']=direccioContador
	valorsTrama['tipus']='f'
	valorsTrama['ccc']=0x49
	valorsTrama=self.envia(valorsTrama,0,0)

	while valorsTrama['ccc'] == None:
	valorsTrama=dict(tipus='',ccc=0,direccioContador=0,idASDU=0,SQN=0,causa=0,direccioPM=0,direccioRegistre=0,objecteInformacio1=[None])
	valorsTrama['direccioContador']=direccioContador
	valorsTrama['tipus']='f'
	valorsTrama['ccc']=0x49
	valorsTrama=self.envia(valorsTrama,0,0)

	if valorsTrama['ccc'] != 0x0B:
	print ("Paquet 13 defectuos! (halt!)")
	time.sleep(10000)


	#====(14)
	valorsTrama=dict(tipus='',ccc=0,direccioContador=0,idASDU=0,SQN=0,causa=0,direccioPM=0,direccioRegistre=0,objecteInformacio1=[None])
	valorsTrama['direccioContador']=direccioContador
	valorsTrama['tipus']='f'
	valorsTrama['ccc']=0x40
	valorsTrama=self.envia(valorsTrama,0,0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 15 defectuos!:")


	##====(17 i 18) enviar contrasenya
	unitats = psw & 0xFF
	desenes = (psw & 0xFF00) >> 8
	centenes = (psw & 0xFF0000) >> 16
	milers = (psw & 0xFF000000) >> 24

	valorsTrama=dict(tipus='v',direccioContador=direccioContador,ccc=0x73,idASDU=0xB7,SQN=0x01,causa=0x06,direccioRegistre=0,objecteInformacio1=[unitats,desenes,centenes,milers])
	valorsTrama=self.envia(valorsTrama,0,0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 18 defectuos!:")

	#====(19 i 20)
	valorsTrama=dict(tipus='',ccc=0,direccioContador=0,idASDU=0,SQN=0,causa=0,direccioPM=0,direccioRegistre=0,objecteInformacio1=[None])
	valorsTrama['direccioContador']=direccioContador
	valorsTrama['tipus']='f'
	valorsTrama['ccc']=0x5B
	valorsTrama=self.envia(valorsTrama,0,0)
	if valorsTrama['ccc'] != 0x08 or valorsTrama['causa'] != 0x07 or valorsTrama['idASDU'] != 0xB7:
	print("Paquet 20 defectuos!:")

	##====(22 i 23)
	valorsTrama=dict(tipus='v',ccc=0x73,direccioContador=direccioContador,idASDU=0x8D,SQN=0,causa=5,direccioPM=0,direccioRegistre=0,objecteInformacio1=[])
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 23 defectuos")


	#===(24 i 25)
	valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])
	valorsTrama['direccioContador'] = direccioContador
	valorsTrama['tipus'] = 'f'
	valorsTrama['ccc'] = 0x5B
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x08 or valorsTrama['causa'] != 0x05 or valorsTrama['idASDU'] != 0x8E:
	print("Paquet 25 defectuos!:")

	##====(26 i 27)
	valorsTrama = dict(tipus = 'v', ccc = 0x73, direccioContador = direccioContador, idASDU = 0xBB, SQN = 0, causa = 6, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [])
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 27 defectuos")

	#===(28 i 29)
	valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])
	valorsTrama['direccioContador'] = direccioContador
	valorsTrama['tipus'] = 'f'
	valorsTrama['ccc'] = 0x5B
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x08 or valorsTrama['causa'] != 0x07 or valorsTrama['idASDU'] != 0xBB:
	print("Paquet 29 defectuos!:")

	##====(32 i 33)
	unitats = psw & 0xFF
	desenes = (psw & 0xFF00) >> 8
	centenes = (psw & 0xFF0000) >> 16
	milers = (psw & 0xFF000000) >> 24

	valorsTrama = dict(tipus = 'v', direccioContador = direccioContador, ccc = 0x73, idASDU = 0xB7, SQN = 0x01, causa = 0x06, direccioRegistre = 0, objecteInformacio1 = [unitats, desenes, centenes, milers])
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 33 defectuos!:")

	#===(34 i 35)
	valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])
	valorsTrama['direccioContador'] = direccioContador
	valorsTrama['tipus'] = 'f'
	valorsTrama['ccc'] = 0x5B
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x08 or valorsTrama['causa'] != 0x07 or valorsTrama['idASDU'] != 0xB7:
	print("Paquet 35 defectuos!:")

	##====(37 i 38) ::Read Instantaneous Values ccc=115, ASDU=162, causa=5, dir.reg=0, obj inf=192,193,194
	valorsTrama = dict(tipus = 'v', ccc = 0x73, direccioContador = direccioContador, idASDU = 0xA2, SQN = 3, causa = 5, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [0xC0, 0XC1, 0xC2, 0x62, 0x16])
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x00:
	print("Paquet 38 defectuos")


	#===(39 i 40)
	valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])
	valorsTrama['direccioContador'] = direccioContador
	valorsTrama['tipus'] = 'f'
	valorsTrama['ccc'] = 0x5B
	valorsTrama = self.envia(valorsTrama, 0, 0)
	if valorsTrama['ccc'] != 0x08 or valorsTrama['causa'] != 0x05 or valorsTrama['idASDU'] != 0xA3:
	print("Paquet 40 defectuos!:")
	else:
	objInfo = valorsTrama['objecteInformacio1']

	self.diccionari["Data"] = (time.strftime("%Y-%m-%d"))
	self.diccionari["Hora"] = (time.strftime("%H:%M:%S"))
	print("Dins de la classe, accedim a data i hora: ",
	self.diccionari["Data"],
	self.diccionari["Hora"])
	#Objecte 1 (192) - A
	temp = objInfo[1] + (objInfo[2] << 8) + (objInfo[3] << 16) + (((0b11111100 & objInfo[4]) >> 2) << 24)
	self.diccionari["kWh Activa Importacio"] = temp
	if (0b1 & objInfo[4]) == 1:
	self.diccionari["kWh Activa Importacio Error"] = 1
	else:
	self.diccionari["kWh Activa Importacio Error"] = 0

	#Objecte 1 (192) - B
	temp = objInfo[5] + (objInfo[6] << 8) + (objInfo[7] << 16) + (((0b11111100 & objInfo[8]) >> 2) << 24)
	self.diccionari["kWh Activa Exportacio"] = temp
	if (0b1 & objInfo[8]) == 1:
	self.diccionari["kWh Activa Exportacio Error"] = 1
	else:
	self.diccionari["kWh Activa Exportacio Error"] = 0

	#Objecte 1 (192) - C
	temp = objInfo[9] + (objInfo[10] << 8) + (objInfo[11] << 16) + (((0b11111100 & objInfo[12]) >> 2) << 24)
	self.diccionari["KVArh Reactiva Q1"] = temp
	if (0b1 & objInfo[12]) == 1:
	self.diccionari["KVArh Reactiva Q1 Error"] = 1
	else:
	self.diccionari["KVArh Reactiva Q1 Error"] = 0

	#Objecte 1 (192) - D
	temp = objInfo[13] + (objInfo[14] << 8) + (objInfo[15] << 16) + (((0b11111100 & objInfo[16]) >> 2) << 24)
	self.diccionari["KVArh Reactiva Q2"] = temp
	if (0b1 & objInfo[16]) == 1:
	self.diccionari["KVArh Reactiva Q2 Error"] = 1
	else:
	self.diccionari["KVArh Reactiva Q2 Error"] = 0

	#Objecte 1 (192) - E
	temp = objInfo[17] + (objInfo[18] << 8) + (objInfo[19] << 16) + (((0b11111100 & objInfo[20]) >> 2) << 24)
	self.diccionari["KVArh Reactiva Q3"] = temp
	if (0b1 & objInfo[20]) == 1:
	self.diccionari["KVArh Reactiva Q3 Error"] = 1
	else:
	self.diccionari["KVArh Reactiva Q3 Error"] = 0

	#Objecte 1 (192) - F
	temp = objInfo[21] + (objInfo[22] << 8) + (objInfo[23] << 16) + (((0b11111100 & objInfo[24]) >> 2) << 24)
	self.diccionari["KVArh Reactiva Q4"] = temp
	if (0b1 & objInfo[24]) == 1:
	self.diccionari["KVArh Reactiva Q4 Error"] = 1
	else:
	self.diccionari["KVArh Reactiva Q4 Error"] = 0

	#Objecte 1 (192) - G Hora i data
	#objInfo[55],56, 57, 58, 59

	#Objecte 2 (193) - A
	temp = objInfo[31] + (objInfo[32] << 8) + (objInfo[33] << 16)
	self.diccionari["Potencia Activa Total KW"] = temp

	#Objecte 2 (193) - B
	temp = objInfo[34] + (objInfo[35] << 8) + (objInfo[36] << 16)
	self.diccionari["Potencia Reactiva Total KVAr"] = temp

	#Objecte 2 (193) - C
	temp = objInfo[37] + (((0b11000000 & objInfo[38]) >> 6) << 8)
	self.diccionari["Factor de potencia total (en milessimes)"] = temp

	#Objecte 2 (193) - D
	if (0b00100000 & objInfo[38]) == 0:
	#print("La P. Activa total es importada")
	self.diccionari["P. Activa total es importada"] = 1
	else:
	#print("La P.Activa total es exportada")
	self.diccionari["P. Activa total es importada"] = 0

	#Objecte 2 (193) - E
	if (0b00010000 & objInfo[38]) == 0:
	#print("P.Reactiva total es Q1/Q2")
	self.diccionari["P.Reactiva total es Q1/Q2"] = 1
	else:
	#print("P.Reactiva total es Q3/Q4")
	self.diccionari["P.Reactiva total es Q1/Q2"] = 0

	#Objecte 2 (193) - F
	if (0b1 & objInfo[38]) == 1:
	#print("P.Total Mesures invalides")
	self.diccionari["P.Reactiva total es Q1/Q2 Error"] = 1
	else:
	self.diccionari["P.Reactiva total es Q1/Q2 Error"] = 0

	# Objecte 2 (193) - G
	self.diccionari["P.Activa Fase I KW"] = objInfo[39] + (objInfo[40] << 8) + (objInfo[41] << 16)

	# Objecte 2 (193) - H
	self.diccionari["P.Reactiva Fase I KVAr"] = objInfo[42] + (objInfo[43] << 8) + (objInfo[44] << 16)

	#Objecte 2 (193) - I
	self.diccionari["Factor de Potencia (cos phi). Fase I (en milessimes)"] = objInfo[45] + (((0b11000000 & objInfo[46]) >> 6) << 8)

	#Objecte 2 (193) - J
	if (0b00100000 & objInfo[46]) == 0:
	#print("La P. Activa Fase I es importada")
	self.diccionari["La P. Activa Fase I es importada"] = 1
	else:
	#print("La P.Activa Fase I es exportada")
	self.diccionari["La P. Activa Fase I es importada"] = 0

	#Objecte 2 (193) - K
	if (0b00010000 & objInfo[46]) == 0:
	# print("P.Reactiva Fase I es Q1/Q2")
	self.diccionari["P.Reactiva Fase I es Q1/Q2"] = 1
	else:
	#print("P.Reactiva Fase I es Q3/Q4")
	self.diccionari["P.Reactiva Fase I es Q1/Q2"] = 0

	#Objecte 2 (193) - L
	if (0b1 & objInfo[46]) == 1:
	#print("P.Total Fase I invalides")
	self.diccionari["Error de lectura en P.Total Fase I invalides"] = 1
	else:
	self.diccionari["Error de lectura en P.Total Fase I invalides"] = 0

	#Objecte 2 (193) - M
	self.diccionari["P.Activa Fase II KW"] = objInfo[47] + (objInfo[48] << 8) + (objInfo[49] << 16)

	#Objecte 2 (193) - N
	self.diccionari["P.Reactiva Fase II KVAr"] = objInfo[50] + (objInfo[51] << 8) + (objInfo[52] << 16)

	#Objecte 2 (193) - O
	self.diccionari["Factor de Potencia (cos phi). Fase II (en milessimes)"] = objInfo[53] + (((0b11000000 & objInfo[54]) >> 6) << 8)

	#Objecte 2 (193) - P
	if (0b00100000 & objInfo[54]) == 0:
	self.diccionari["P. Activa Fase II es importada"] = 1
	else:
	#print("La P.Activa Fase II es exportada")
	self.diccionari["P. Activa Fase II es importada"] = 0

	#Objecte 2 (193) - Q
	if (0b00010000 & objInfo[54]) == 0:
	#print("P.Reactiva Fase II es Q1/Q2")
	self.diccionari["P.Reactiva Fase II es Q1/Q2"] = 1
	else:
	# print("P.Reactiva Fase II es Q3/Q4")
	self.diccionari["P.Reactiva Fase II es Q1/Q2"] = 0

	#Objecte 2 (193) - R
	if (0b1 & objInfo[54]) == 1:
	self.diccionari["Error de lectura P.Total Fase II"] = 1
	else:
	self.diccionari["Error de lectura P.Total Fase II"] = 0

	#Objecte 2 (193) - S
	self.diccionari["P.Activa Fase III KW"] = objInfo[55] + (objInfo[56] << 8) + (objInfo[57] << 16)

	#Objecte 2 (193) - T
	self.diccionari["P.Reactiva Fase III KVAr"] = objInfo[58] + (objInfo[59] << 8) + (objInfo[60] << 16)

	#Objecte 2 (193) - U
	self.diccionari["Factor de Potencia (cos phi). Fase III (en milessimes)"] = objInfo[61] + (((0b11000000 & objInfo[62]) >> 6) << 8)

	#Objecte 2 (193) - V
	if (0b00100000 & objInfo[62]) == 0:
	self.diccionari["La P. Activa Fase III es importada"] = 1
	else:
	#print("La P.Activa Fase III es exportada")
	self.diccionari["La P. Activa Fase III es importada"] = 0

	#Objecte 2 (193) - W
	if (0b00010000 & objInfo[62]) == 0:
	self.diccionari["P.Reactiva Fase III es Q1/Q2"] = 1
	else:
	# print("P.Reactiva Fase III es Q3/Q4")
	self.diccionari["P.Reactiva Fase III es Q1/Q2"] = 0

	#Objecte 2 (193) - X
	if (0b1 & objInfo[62]) == 1:
	self.diccionari["Error de Lectrua en P.Total Fase III"] = 1
	else:
	self.diccionari["Error de Lectrua en P.Total Fase III"] = 0

	#Objecte 2 (193) - Y Hora i data
	#objInfo[63, 64, 65, 66, 67

	#Objecte 3 (194) - A
	self.diccionari["Intensitat Fase I (decimes de A)"] = objInfo[69] + (objInfo[70] << 8) + (objInfo[71] << 16)

	#Objecte 3 (194) - B
	self.diccionari["Tensio Fase I (decimes de V)"] = objInfo[72] + (objInfo[73] << 8) + (objInfo[74] << 16) + (((0b11111100 & objInfo[75]) >> 2) << 24)

	#Objecte 3 (194) - C
	if (0b1 & objInfo[75]) == 1:
		self.diccionari["Error de Lectura mesures de Fase I"] = 1
	else:
		self.diccionari["Error de Lectura mesures de Fase I"] = 0

	#Objecte 3 (194) - D
	self.diccionari["Intensitat Fase II (decimes de A)"] = objInfo[76] + (objInfo[77] << 8) + (objInfo[78] << 16)

	#Objecte 3 (194) - E
	self.diccionari["Tensio Fase II (decimes de V)"] = objInfo[79] + (objInfo[80] << 8) + (objInfo[81] << 16) + (((0b11111100 & objInfo[82]) >> 2) << 24)

	#Objecte 3 (194) - F
	if (0b1 & objInfo[83]) == 1:
	self.diccionari["Error de Lectura de mesures de Fase II"] = 1
	else:
	self.diccionari["Error de Lectura de mesures de Fase II"] = 0

	#Objecte 3 (194) - G
	self.diccionari["Intensitat Fase III (decimes de A)"] = objInfo[83] + (objInfo[84] << 8) + (objInfo[85] << 16)

	#Objecte 3 (194) - H
	self.diccionari["Tensio Fase III (decimes de V)"] = objInfo[86] + (objInfo[87] << 8) + (objInfo[88] << 16) + (((0b11111100 & objInfo[89]) >> 2) << 24)

	#Objecte 3 (194) - I
	if (0b1 & objInfo[89]) == 1:
		self.diccionari["Error de Lectura de les mesures de la Fase III"] = 1
	else:
		self.diccionari["Error de Lectura de les mesures de la Fase III"] = 0
