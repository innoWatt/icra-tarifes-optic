# icra-tarifes-optic

DOCUMENTACIÓ PROGRAMA ICRA – TARIFES – OPTIC

Tenim una Raspberry Pi connectada a un comptador Actaris SL761 amb un sensor òptic. 

El protocol implementat es el "IEC870-5"
descripció: http://www.edpenergia.es/recursosedp/doc/distribucion-gas/20130814/telemedida/definicion-protocolo.pdf

PROVAR!: https://github.com/Ebolon/iec104

Cal executar l'script "server/tcp_serial_redirect.py" al raspberry

rasbperry: 
	- ip local:   192.168.103.63
	- ip externa: 84.89.61.64
	- pi icrahopetayea 

	ser.port = "/dev/ttyUSB0"
	ser.baudrate=9600
	ser.bytesize=8
	ser.parity=serial.PARITY_EVEN
	ser.stopbits=1
	ser.xonxoff=False
	ser.rtscts=False
	ser.dsrdtr=False
	ser.timeout=1 

	port serial redirigit al port 3333
