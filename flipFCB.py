def flipFCB(trama):
	'''1. Trama fixa o variable'''

	'''
		2. Agafa el byte control
		estructura:
			8     7     6     5     4   3   2   1
		+-----+-----+-----+-----+-----------------+
		| RES | PRM | FCB | FCV |       FUN       | (si PRM=1)
		+-----+-----+-----+-----+-----------------+
	'''

	''' 3. Gira el bit 6 amb un XOR (^) '''

	'''
		control ^ 0b00100000
	'''

	'''actualitza el checksum'''

	return trama
