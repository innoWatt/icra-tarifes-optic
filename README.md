## TO DO
	* Programar lectura única d'energia
	* Crear un serial virtual per quan no hi ha serial "virtual.py"
	* Crear un sol arxiu de configuració per tot que inclogui dades serial, direcció i punt de mesura

# icra-tarifes-optic documentació

Autors: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

Aquest paquet inclou:

 * Intèrpret de trames del Protocol IEC 60870-5-102 (processa.py)
 * Un creador de trames de bytes (crea.py)
 * Una funció per enviar trames i llegir la resposta (pregunta.py)
 * Una funció per extreure corba horària de potència (extreuPotencia.py)

Raspberry Pi connectada a un comptador Actaris SL762B, al sensor òptic (port serial)

Idea general:

		+-------------------+      crea.py        : l'usuari crea una trama                                    
		|      USUARI       |      processa.py    : la trama és traduïda a llenguatge humà         
		+-------------------+      pregunta.py    : la trama és enviada al comptador, i aquest respon
		  |               ^        processaA11.py : extreu la potencia d'una trama de resposta ASDU 11
		  |               |        
		  v               |
		 crea.py          |
		  |               |
		  |               |
		  v               |
		 TRAMA----->processa.py
		  |               ^
		  |               |
		  v               |
		 pregunta.py    TRAMA
		  |               ^
		  v               |
		+-------------------+
		|     COMPTADOR     |
		+-------------------+

ASDUS implementats (peticions): 122, 123, 134, 183, 190

#Inici 
El primer que s'ha de fer és testejar si el Raspberry pot enviar trames:

```
python tests/serialProva.py
```
![](https://raw.githubusercontent.com/holalluis/icra-tarifes-optic/master/gif/serialProva.gif)

Després, s'ha de crear un script com ara `usuari.py` per fer les peticions desitjades. Exemple

```
	import crea     as C
	import pregunta as P

	d=1; psw=1 #direccio comptador=1 i password=1

	#login
	P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU183(psw))) #request user data & send password
	P.pregunta(C.creaTramaFix(0b01011011,d)) #request class 2 data

	#prova asdu 190 amb registre 11 (Curva de carga) i direccio 9,10,11
	P.pregunta(C.creaTramaVar(0b01110011,d,C.creaASDU190(11,10,C.creaTemps(21,7,16,0,0),C.creaTemps(22,7,16,0,0))))
	while 1:
		P.pregunta(C.creaTramaFix(0b01011011,d)) #request data
		P.pregunta(C.creaTramaFix(0b01111011,d)) #request data (flip FCB)

	quit('-S-T-O-P-')
```

# Scripts a nivell usuari:
* usuari.py
* extreuCorbaPotencia.py

Exemple de resposta: 

(pendent)

Dades Rasbperry:

* ip local:   192.168.103.63
* ip externa: 84.89.61.64:22

Dades de la connexió serial:

```
	ser.port = "/dev/ttyUSB0"
	ser.baudrate=9600
	ser.bytesize=8
	ser.parity=serial.PARITY_EVEN
	ser.stopbits=1
	ser.xonxoff=False
	ser.rtscts=False
	ser.dsrdtr=False
	ser.timeout=1 
```

Com fer un grafic amb la comanda `gnuplot`
==========================================

plot [FILE] using [X]:[Y] with line

plot "icra-20160701.txt" using 2:3 with line

# Manual EN DESENVOLUPAMENT

Referències:

* http://www.ree.es/sites/default/files/01_ACTIVIDADES/Documentos/Documentacion-Simel/protoc_RMCM10042002.pdf
* http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

