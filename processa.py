
''' 
	modul per processar respostes
	resposta prove de
	resposta=serial.readlines()
'''

def processa(resposta):
	'''resposta es un array de tamany 1'''
	buf=bytearray(resposta[0])

	'''comptem el numero de bytes'''
	n=len(buf) 
	print(str(n)+" bytes rebuts")

	'''mostra tots els bytes'''
	for i in range(n): print buf[i],
	print('')
	
	'''primer pas: saber si la trama es fixa o variable'''
	if(buf[0]==0x10 and buf[n-1]==0x16):
		print("La trama es fixa [0x10 C A A CS 0x16]")
		processaTramaFixa(buf)
	elif(buf[0]==0x68 and buf[n-1]==0x16):
		print("La trama es variable [0x68 L L 0x68 ASDU CS 0x16]")
		processaTramaVariable(buf)
	else:
		raise RuntimeError('Tipus de trama desconegut')


def processaTramaFixa(buf):
	''' [inici C A A checksum fi]'''
	n=len(buf)
	if(buf[0]!=0x16 and buf[n-1]!=0x16): raise RuntimeError('La trama no es fixa')

	'''Comprova checksum (5e bit)'''
	checksum=buf[4]
	if(buf[1]+buf[2]+buf[3]!=checksum): raise RuntimeError('Checksum erroni')

	'''Camps ASDU'''
	control=buf[1]  #byte de control
	direccio1=buf[2] #direccio comptador bit 1
	direccio2=buf[3] #direccio comptador bit 2

	'''processa el byte Control'''
	print("Control ["+bin(control)+"]")
	res = control & 0b10000000 == 128
	prm = control & 0b01000000 == 64
	fcb = control & 0b00100000 == 32
	fcv = control & 0b00010000 == 16
	fun = control & 0b00001111
	#print([res,prm,fcb,fcv,fun])

	'''mostra informacio de cada part'''
	'''prm,fcb,fcv TODO'''
	if(prm): print("bit PRM: Aquest missatge es una peticio:");
	else:    print("bit PRM: Aquest missatge es una resposta:");

	'''bits acd i dfc'''
	if(prm==False): 
		dfc=fcv;
		if(dfc):print("Els missatges futurs causaran data overflow")

	if(prm):
		print({
			0:"Peticio: Reset del link remot",
			3:"Peticio: Enviament de dades d'usuari",
			9:"Peticio: Solicitud de l'estat del link",
			11:"Peticio: Solicitud de dades de classe 2",
		}[fun])
	else:
		print({
			0:"Resposta: ACK",
			1:"Resposta: NACK. comanda no acceptada",
			8:"Resposta: Dades de l'usuari",
			9:"Resposta: NACK. dades demanades no disponibles",
			11:"Resposta: Estat del link o demanda d'acces",
		}[fun])


def processaTramaVariable(buf):
	print('no implementat')
	#TODO
	pass
	
pregunta=['\x10\x49\x01\x00\x4a\x16']
resposta=['\x10\x0b\x01\x00\x0c\x16']
resposta=pregunta
processa(resposta)
