# icra-tarifes-optic

DOCUMENTACIÓ ICRA – TARIFES – OPTIC

Autors: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

Aquest paquet inclou:

 * Intèrpret de trames del Protocol IEC 60870-5-102 (processa.py)
 * Un creador de trames de bytes (crea.py)
 * Una funció per enviar trames i llegir la resposta (pregunta.py)
 * Una funció per extreure corba horària de potència (extreuPotencia.py)

Tenim una Raspberry Pi connectada a un comptador Actaris SL762B amb un sensor òptic (port serial)

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


ASDUS implementats (peticions): 122, 123, 134, 183, 190

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

EN DESENVOLUPAMENT

Referències:

* http://www.ree.es/sites/default/files/01_ACTIVIDADES/Documentos/Documentacion-Simel/protoc_RMCM10042002.pdf
* http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

Pendent:

L'arxiu processa.py crea un xml que llavors es podria obrir amb un format més bonic. Per indentar un arxiu xml de resultat:

```
	xmllint --format arxiu.xml
```

Exemple GIF (creat amb ffmpeg)
![](https://raw.githubusercontent.com/holalluis/icra-tarifes-optic/master/gif/serialProva.gif)
