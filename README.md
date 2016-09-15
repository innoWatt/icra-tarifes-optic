# icra-tarifes-optic

DOCUMENTACIÓ ICRA – TARIFES – OPTIC

Tenim una Raspberry Pi connectada a un comptador Actaris SL761 amb un sensor òptic (port serial)

El protocol implementat es el "iec 870-5-102"

Abstracció, idea global:

  +====================+      crea.py     : l'usuari crea una trama                                    
  |      USUARI        |      processa.py : la trama és traduïda a llenguatge humà         
  +====================+      pregunta.py : la trama és enviada al comptador, i aquest respon
    |               ^        
    |               |        
    v               |
  crea.py           |
    |               |
    |               |
    v               |
  TRAMA------->processa.py
    |               ^
    |               |
    v               |
  pregunta.py     TRAMA
    |               ^
    |               |
    v               |
  +====================+
  |     COMPTADOR      |
  +====================+

L'arxiu processa.py crea un xml que llavors es pot interpretar. 

Per indentar un arxiu xml de resultat:

```
  xmllint --format arxiu.xml
```

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

En un futur hi haurà TCP, 'script "server/tcp_serial_redirect.py" al raspberry:

```
python tcp_serial_redirect.py --parity E -P 3333 /dev/ttyUSB0 9600
```

En desenvolupament

Referències:

* https://github.com/Ebolon/iec104
* http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

