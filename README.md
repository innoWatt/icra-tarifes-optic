# icra-tarifes-optic

DOCUMENTACIÓ ICRA – TARIFES – OPTIC

Autors: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

Aquest paquet inclou:
 * Intèrpret de trames del Protocol IEC 60870-5-102

Tenim una Raspberry Pi connectada a un comptador Actaris SL761 amb un sensor òptic (port serial)

El protocol implementat es el "iec 60870-5-102"

Abstracció, idea global:

		+-------------------+      crea.py     : l'usuari crea una trama                                    
		|      USUARI       |      processa.py : la trama és traduïda a llenguatge humà         
		+-------------------+      pregunta.py : la trama és enviada al comptador, i aquest respon
		  |               ^        
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


ASDUS implementats (peticions): 122, 134, 183

Dades Rasbperry: pi, icrahopetayea 

* ip local:   192.168.103.63
* ip externa: 84.89.61.64:22

Dades de la connexió serial:

	ser.port = "/dev/ttyUSB0"
	ser.baudrate=9600
	ser.bytesize=8
	ser.parity=serial.PARITY_EVEN
	ser.stopbits=1
	ser.xonxoff=False
	ser.rtscts=False
	ser.dsrdtr=False
	ser.timeout=1 

En un futur es podria configurar un servidor TCP, 'script "server/tcp_serial_redirect.py" al raspberry:

```
python tcp_serial_redirect.py --parity E -P 3333 /dev/ttyUSB0 9600
```

EN DESENVOLUPAMENT

Referències:

* http://www.ree.es/sites/default/files/01_ACTIVIDADES/Documentos/Documentacion-Simel/protoc_RMCM10042002.pdf
* http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

Pendent:

```
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
``` 
L'arxiu processa.py crea un xml que llavors es pot interpretar. 

Per indentar un arxiu xml de resultat:

```
	xmllint --format arxiu.xml
```

Exemple GIF (creat amb ffmpeg)
![](https://raw.githubusercontent.com/holalluis/icra-tarifes-optic/master/gif/serialProva.gif)
