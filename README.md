# icra-tarifes-optic

DOCUMENTACIÓ ICRA – TARIFES – OPTIC

Tenim una Raspberry Pi connectada a un comptador Actaris SL761 amb un sensor òptic (port serial)

El protocol implementat es el "iec 870-5-102"

http://www.aperca.org/temppdf/Articulo%20Contadores.pdf

https://github.com/Ebolon/iec104

* Per indentar un arxiu xml de resultat:

```
  xmllint --format arxiu.xml
```

Dades Rasbperry: pi icrahopetayea 

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

