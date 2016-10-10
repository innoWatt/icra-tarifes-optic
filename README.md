## TO DO
	* Programar lectura única d'energia
	* Crear un serial virtual per quan no hi ha serial "virtual.py"
	* Crear un sol arxiu de configuració per tot que inclogui dades serial, direcció i punt de mesura

# Manual EN DESENVOLUPAMENT

# icra-tarifes-optic documentació

Autors: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

Aquest paquet inclou:

 * Intèrpret de trames del Protocol IEC 60870-5-102 (processa.py)
 * Un creador de trames de bytes (crea.py)
 * Una funció per enviar trames i llegir la resposta (pregunta.py)
 * Una funció per extreure corba horària de potència d'un ASDU 11 (processaA11.py)

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
El primer que s'ha de fer és editar l'arxiu `config.py` per posar les dades de connexió i tot seguit testejar si el Raspberry envia trames correctament:

```
vim config.py
python tests/serialProva.py
```
![](https://raw.githubusercontent.com/holalluis/icra-tarifes-optic/master/gif/serialProva.gif)

Després, s'ha de crear un script com ara `usuari.py` per fer les peticions desitjades. Exemple

```
	import crea     as C
	import pregunta as P

	#login
	P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183(1))) #request user data & send password=1
	P.pregunta(C.creaTramaFix(0b01011011)) #request class 2 data

	#prova asdu 190 amb registre 11 (Curva de carga) i direccio 9,10,11
	P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU190(11,10,C.creaTemps(21,7,16,0,0),C.creaTemps(22,7,16,0,0))))
	while 1:
		P.pregunta(C.creaTramaFix(0b01011011)) #request data
		P.pregunta(C.creaTramaFix(0b01111011)) #request data (flip FCB)
```

# Scripts a nivell usuari:
* usuari.py
* usuari_extreuPotencia.py

Exemple de resposta script extreuCorbaPotencia.py: 

	01/07/2016 01:00 114 kW
	01/07/2016 02:00 113 kW
	01/07/2016 03:00 108 kW
	01/07/2016 04:00 110 kW
	01/07/2016 05:00 107 kW
	01/07/2016 06:00 110 kW
	01/07/2016 07:00 111 kW
	01/07/2016 09:00 139 kW
	01/07/2016 10:00 175 kW
	01/07/2016 14:00 153 kW

Dades Rasbperry:

* ip local:   192.168.103.63
* ip externa: 84.89.61.64:22

Dades de la connexió serial --> `config.py`:

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

```
	plot [FILE] using [X]:[Y] with line
	plot "icra-20160701.txt" using 2:3 with line
```

Referències:

* http://www.ree.es/sites/default/files/01_ACTIVIDADES/Documentos/Documentacion-Simel/protoc_RMCM10042002.pdf
* http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

