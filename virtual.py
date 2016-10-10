#!/usr/bin/env python
'''
	Crea un serial virtual per quan no hi ha l'arduino (per testejar)
	TO DO
'''

class Serial:
	Trama = "TRAMA VIRTUAL" #no canvia mai
	trama = Trama
	port ="VIRTUAL"
	def read(self):
		n=len(self.trama)
		if n is 0: 
			self.trama=self.Trama
			n=len(self.trama)
		c=self.trama[0]
		self.trama=self.trama[1:n]
		return c
	def flush(self): pass
	def flushInput(self): pass
	def flushOutput(self): pass
	def isOpen(self): return True
	def write(self,ordre): pass #print "Has enviat %s" % ordre

#test
'''
ser = Serial()    
trama=""
while True:
	c=ser.read()
	trama+=c
	if c is "F":
		print trama
		break
		'''
