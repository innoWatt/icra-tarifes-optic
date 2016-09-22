'''
	D'aquí he de treure com implementar ASDU 162 (valors instantanis)
'''

def init(self):
		direccioContador = 1
		psw = 1
		tFixaNoms=['Inici','Control C','Direccio 1','Direccio 2','checksum','fi']
		tVariableNoms=['Inici1','Longitud1','Longitud2','Inici2','Control C','Direccio 1','Direccio 2','Id.Tipo','SQ N','Causa','PM 1','PM 2','dir.reg','         ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '         ', '         ', '         ', '         ', '         ', '         ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ', '      ']
		tVariableNomsClauAcces=['Inici1','Longitud1','Longitud2','Inici2','Control C','Direccio 1','Direccio 2','Id.Tipo','SQ N','Causa','P.Medida','dir.reg1','dir.reg2','X Clau1','X Clau2','Clau3','Clau4','checksum','fi']
		valorsTrama = dict(tipus = '', ccc = 0, direccioContador = 0, idASDU = 0, SQN = 0, causa = 0, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [None])
		tempsImpres = False

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

	##====(17 i 18) enviar contrasenya
	#REQUEST
	unitats = psw & 0xFF
	desenes = (psw & 0xFF00) >> 8
	centenes = (psw & 0xFF0000) >> 16
	milers = (psw & 0xFF000000) >> 24
	valorsTrama=dict(tipus='v',ccc=0x73,idASDU=0xB7,SQN=0x01,causa=0x06,direccioRegistre=0,objecteInformacio1=[unitats,desenes,centenes,milers])
	valorsTrama=self.envia(valorsTrama,0,0)

	##====(22 i 23)
	#REQUEST
	valorsTrama=dict(tipus='v',ccc=0x73,idASDU=0x8D,SQN=0,causa=5,direccioPM=0,direccioRegistre=0,objecteInformacio1=[])
	valorsTrama = self.envia(valorsTrama, 0, 0)

	##====(26 i 27)
	#REQUEST
	valorsTrama = dict(tipus = 'v', ccc = 0x73, idASDU = 0xBB, SQN = 0, causa = 6, direccioPM = 0, direccioRegistre = 0, objecteInformacio1 = [])
	valorsTrama = self.envia(valorsTrama, 0, 0)

	##====(32 i 33)
	#REQUEST
	unitats = psw & 0xFF
	desenes = (psw & 0xFF00) >> 8
	centenes = (psw & 0xFF0000) >> 16
	milers = (psw & 0xFF000000) >> 24
	valorsTrama = dict(tipus = 'v', direccioContador = direccioContador, ccc = 0x73, idASDU = 0xB7, SQN = 0x01, causa = 0x06, direccioRegistre = 0, objecteInformacio1 = [unitats, desenes, centenes, milers])
	valorsTrama = self.envia(valorsTrama, 0, 0)

	#===(34 i 35)
	#REQUEST
	valorsTrama['tipus'] = 'f'
	valorsTrama['ccc'] = 0x5B
	valorsTrama = self.envia(valorsTrama, 0, 0)

	##====(37 i 38) ::Read Instantaneous Values ccc=115, ASDU=162, causa=5, dir.reg=0, obj inf=192,193,194
	#REQUEST
	vT = dict(tipus='v',ccc=0x73,idASDU = 0xA2,SQN=3,causa=5,direccioPM=0,direccioRegistre=0,objecteInformacio1=[0xC0,0XC1,0xC2,0x62,0x16])
	vT = self.envia(vT, 0, 0)

	print("accedim a data i hora: "),

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
	self.diccionari["La P. Activa Fase I es importada"] = 1
	else:
	self.diccionari["La P. Activa Fase I es importada"] = 0

	#Objecte 2 (193) - K
	if (0b00010000 & objInfo[46]) == 0:
	self.diccionari["P.Reactiva Fase I es Q1/Q2"] = 1
	else:
	self.diccionari["P.Reactiva Fase I es Q1/Q2"] = 0

	#Objecte 2 (193) - L
	if (0b1 & objInfo[46]) == 1:
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
