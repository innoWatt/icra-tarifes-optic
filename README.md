# icra-tarifes-optic

Comunicació amb comptadors elèctrics pel protocol IEC 60870-5-102

## Requeriments
- Python 2.7
- pyserial (can be installed using pip, 'pip install pyserial')

## Comptadors provats (veure carpeta /img)
- Actaris SL762B (port òptic) (icra) OK
- Actaris ACE6000 (port òptic) (edar quart) OK
- Landys Gyr (port òptic) (edar girona) OK
- Circutor Cirwatt (port òptic) (edar girona) <- no contesta bé

## Inici
bash inici.sh

## Manual en desenvolupament

Autors: Lluis Bosch (lbosch@icra.cat) & Felix Hill (fhill@icra.cat)

Aquest paquet inclou:

 * Intèrpret de trames del Protocol IEC 60870-5-102 (processa.py)
 * Un creador de trames de bytes (crea.py)
 * Una funció per enviar trames i llegir la resposta (pregunta.py)
 * Una funció per extreure corba horària de potència d'un ASDU 11 (processaA11.py)

Raspberry Pi connectada a un comptador Actaris SL762B, al sensor òptic (port serial, RS232)

https://www1.itron.com/local/Spain%20Product%20Portfolio/ACE%20SL7000%20tipo%20762-EL-ES-04.14.pdf

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
El primer que s'ha de fer és editar l'arxiu `config.py`, i després testejar si el Raspberry envia trames correctament:

```
	vim config.py
	python test.py
```
![](https://raw.githubusercontent.com/holalluis/icra-tarifes-optic/master/gif/test.gif)

Després, s'ha de crear un script com ara `usuari.py` per fer les peticions desitjades. Exemple

```python
	import crea     as C
	import pregunta as P

	#login
	P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183(1))) #request user data & send password=1
	P.pregunta(C.creaTramaFix(0b01011011)) #request class 2 data

	#prova asdu 190 amb registre 11 (Curva de carga) i direccio 9,10,11
	P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU190(11,10,C.creaTemps(16,7,21,0,0,1),C.creaTemps(16,7,22,16,0,0,1))))
	while 1:
		P.pregunta(C.creaTramaFix(0b01011011)) #request data
		P.pregunta(C.creaTramaFix(0b01111011)) #request data (flip FCB)
```

# Scripts a nivell usuari:
* usuari.py
* usuari_extreuPotencia.py

Exemple de resposta script usuari_extreuPotencia.py: 

	01/07/2016 01:00 114 kW
	01/07/2016 02:00 113 kW
	01/07/2016 03:00 108 kW
	01/07/2016 04:00 110 kW
	01/07/2016 05:00 107 kW
	[...]

Dades Rasbperry ICRA:

* ip local:   192.168.103.63
* ip externa: 84.89.61.64

Dades de la connexió serial --> `config.py`:

```python
	port = "/dev/ttyUSB0"
	baudrate=9600
	bytesize=8
	parity=serial.PARITY_EVEN
	stopbits=1
	xonxoff=False
	rtscts=False
	dsrdtr=False
	timeout=1 
```

## Exemple sessio
```
root@debian:/home/lbosch/icra-tarifes-optic/usr# python instantani.py 
RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  19 bytes: 68 d d 68 8 1 0 b7 1 7 1 0 0 1 0 0 0 ca 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	10 bytes: b7 1 7 1 0 0 1 0 0 0 
	<iud>
	  6 bytes: b7 1 7 1 0 0 
	  idt: 0xb7: [ASDU 183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x7: [T=False, PN=False, Causa de transmissió=7: CONFIRMACION DE ACTIVACION]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  4 bytes: 1 0 0 0 
	  <objecte>
		4 bytes:  1 0 0 0 
		Clau d'accés: 1
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  45 bytes: 68 27 27 68 8 1 0 a3 1 5 1 0 0 c0 30 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 24 90 bf 3 11 a1 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	36 bytes: a3 1 5 1 0 0 c0 30 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 24 90 bf 3 11 
	<iud>
	  6 bytes: a3 1 5 1 0 0 
	  idt: 0xa3: [ASDU 163: INSTANTANIS (RESPOSTA)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  30 bytes: c0 30 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 24 90 bf 3 11 
	  <objecte>
		30 bytes:  c0 30 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 24 90 bf 3 11 
		Direcció objecte: 192
		KWh Activa Importació: 8920624
		KWh Activa Exportació: 0
		KVArh Reactiva Q1: 566836
		KVArh Reactiva Q2: 0
		KVArh Reactiva Q3: 0
		KVArh Reactiva Q4: 1537379
		[ETIQUETA] tipus a (5 bytes): 24 90 bf 3 11 = Data: 31/03/2017 16:36
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

root@debian:/home/lbosch/icra-tarifes-optic/usr# python instantani.py 
RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  19 bytes: 68 d d 68 8 1 0 b7 1 7 1 0 0 1 0 0 0 ca 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	10 bytes: b7 1 7 1 0 0 1 0 0 0 
	<iud>
	  6 bytes: b7 1 7 1 0 0 
	  idt: 0xb7: [ASDU 183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x7: [T=False, PN=False, Causa de transmissió=7: CONFIRMACION DE ACTIVACION]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  4 bytes: 1 0 0 0 
	  <objecte>
		4 bytes:  1 0 0 0 
		Clau d'accés: 1
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  45 bytes: 68 27 27 68 8 1 0 a3 1 5 1 0 0 c0 31 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 25 90 bf 3 11 a3 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	36 bytes: a3 1 5 1 0 0 c0 31 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 25 90 bf 3 11 
	<iud>
	  6 bytes: a3 1 5 1 0 0 
	  idt: 0xa3: [ASDU 163: INSTANTANIS (RESPOSTA)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  30 bytes: c0 31 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 25 90 bf 3 11 
	  <objecte>
		30 bytes:  c0 31 1e 88 0 0 0 0 0 34 a6 8 0 0 0 0 0 0 0 0 0 63 75 17 0 25 90 bf 3 11 
		Direcció objecte: 192
		KWh Activa Importació: 8920625
		KWh Activa Exportació: 0
		KVArh Reactiva Q1: 566836
		KVArh Reactiva Q2: 0
		KVArh Reactiva Q3: 0
		KVArh Reactiva Q4: 1537379
		[ETIQUETA] tipus a (5 bytes): 25 90 bf 3 11 = Data: 31/03/2017 16:37
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

root@debian:/home/lbosch/icra-tarifes-optic/usr# python mes_actual.py 
Dia inici: [1, 3, 17]
Dia final: [32, 3, 17]
RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  19 bytes: 68 d d 68 8 1 0 b7 1 7 1 0 0 1 0 0 0 ca 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	10 bytes: b7 1 7 1 0 0 1 0 0 0 
	<iud>
	  6 bytes: b7 1 7 1 0 0 
	  idt: 0xb7: [ASDU 183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x7: [T=False, PN=False, Causa de transmissió=7: CONFIRMACION DE ACTIVACION]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  4 bytes: 1 0 0 0 
	  <objecte>
		4 bytes:  1 0 0 0 
		Clau d'accés: 1
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  27 bytes: 68 15 15 68 8 1 0 7b 1 12 1 0 b 1 1 0 0 1 3 11 0 0 20 3 11 ee 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	18 bytes: 7b 1 12 1 0 b 1 1 0 0 1 3 11 0 0 20 3 11 
	<iud>
	  6 bytes: 7b 1 12 1 0 b 
	  idt: 0x7b: [ASDU 123: LEER TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x12: [T=False, PN=False, Causa de transmissió=18: PERIODO DE INTEGRACION NO DISPONIBLE]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  12 bytes: 1 1 0 0 1 3 11 0 0 20 3 11 
	  <objecte>
		12 bytes:  1 1 0 0 1 3 11 0 0 20 3 11 
		Direcció inici: 1: Totales Integrados de Activa Entrante
		Direcció final: 1: Totales Integrados de Activa Entrante
		[ETIQUETA] tipus a (5 bytes): 0 0 1 3 11 = Data: 01/03/2017 00:00
		[ETIQUETA] tipus a (5 bytes): 0 0 20 3 11 = Data: 00/03/2017 00:00
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

Traceback (most recent call last):
  File "mes_actual.py", line 37, in <module>
	P.pregunta(C.creaTramaFix(0b01011011)) #request data
  File "../bin/pregunta.py", line 44, in pregunta
	Pro.processa(respostaTotal) #mostra la resposta (veure "processa.py")
  File "../bin/processa.py", line 71, in processa
	detectaError(buf)
  File "../bin/processa.py", line 868, in detectaError
	elif cdt==18: raise RuntimeError("PERIODO DE INTEGRACION NO DISPONIBLE")
RuntimeError: PERIODO DE INTEGRACION NO DISPONIBLE
root@debian:/home/lbosch/icra-tarifes-optic/usr# vi mes_actual.py 
root@debian:/home/lbosch/icra-tarifes-optic/usr# python dia.py 
Ús: python dia.py dd-mm-yy
root@debian:/home/lbosch/icra-tarifes-optic/usr# python dia.py 28-03-17
RESPOSTA
Traceback (most recent call last):
  File "dia.py", line 27, in <module>
	P.pregunta(C.creaTramaVar(0b01110011,C.creaASDU183())) #request data & send password
  File "../bin/pregunta.py", line 44, in pregunta
	Pro.processa(respostaTotal) #mostra la resposta (veure "processa.py")
  File "../bin/processa.py", line 54, in processa
	if n==0: raise RuntimeError("TRAMA BUIDA")
RuntimeError: TRAMA BUIDA
root@debian:/home/lbosch/icra-tarifes-optic/usr# python dia.py 28-03-17
RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  19 bytes: 68 d d 68 8 1 0 b7 1 7 1 0 0 1 0 0 0 ca 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	10 bytes: b7 1 7 1 0 0 1 0 0 0 
	<iud>
	  6 bytes: b7 1 7 1 0 0 
	  idt: 0xb7: [ASDU 183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x7: [T=False, PN=False, Causa de transmissió=7: CONFIRMACION DE ACTIVACION]
	  dco->registre: 0x0=0: Dirección de defecto
	</iud>
	<objectesInfo>
	  4 bytes: 1 0 0 0 
	  <objecte>
		4 bytes:  1 0 0 0 
		Clau d'accés: 1
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  6 bytes: 10 0 1 0 1 16 
  <control>
	Byte control: 0x0=0=0b0
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b0 [Funció 0] [Resposta: ACK]
  </control>
</missatge>

RESPOSTA
<missatge>
  27 bytes: 68 15 15 68 8 1 0 7b 1 7 1 0 b 1 1 0 0 1c 3 11 0 0 1d 3 11 fb 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	18 bytes: 7b 1 7 1 0 b 1 1 0 0 1c 3 11 0 0 1d 3 11 
	<iud>
	  6 bytes: 7b 1 7 1 0 b 
	  idt: 0x7b: [ASDU 123: LEER TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x7: [T=False, PN=False, Causa de transmissió=7: CONFIRMACION DE ACTIVACION]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  12 bytes: 1 1 0 0 1c 3 11 0 0 1d 3 11 
	  <objecte>
		12 bytes:  1 1 0 0 1c 3 11 0 0 1d 3 11 
		Direcció inici: 1: Totales Integrados de Activa Entrante
		Direcció final: 1: Totales Integrados de Activa Entrante
		[ETIQUETA] tipus a (5 bytes): 0 0 1c 3 11 = Data: 28/03/2017 00:00
		[ETIQUETA] tipus a (5 bytes): 0 0 1d 3 11 = Data: 29/03/2017 00:00
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 6c 0 0 0 0 0 81 5c 3 11 84 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 6c 0 0 0 0 0 81 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 6c 0 0 0 0 0 81 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 6c 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 108 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 81 5c 3 11 = Data: 28/03/2017 01:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 70 0 0 0 0 0 82 5c 3 11 89 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 70 0 0 0 0 0 82 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 70 0 0 0 0 0 82 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 70 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 112 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 82 5c 3 11 = Data: 28/03/2017 02:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 70 0 0 0 0 0 83 5c 3 11 8a 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 70 0 0 0 0 0 83 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 70 0 0 0 0 0 83 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 70 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 112 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 83 5c 3 11 = Data: 28/03/2017 03:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 73 0 0 0 0 0 84 5c 3 11 8e 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 73 0 0 0 0 0 84 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 73 0 0 0 0 0 84 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 73 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 115 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 84 5c 3 11 = Data: 28/03/2017 04:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 6b 0 0 0 0 0 85 5c 3 11 87 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 6b 0 0 0 0 0 85 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 6b 0 0 0 0 0 85 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 6b 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 107 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 85 5c 3 11 = Data: 28/03/2017 05:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 77 0 0 0 0 0 86 5c 3 11 94 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 77 0 0 0 0 0 86 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 77 0 0 0 0 0 86 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 77 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 119 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 86 5c 3 11 = Data: 28/03/2017 06:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 77 0 0 0 0 0 87 5c 3 11 95 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 77 0 0 0 0 0 87 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 77 0 0 0 0 0 87 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 77 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 119 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 87 5c 3 11 = Data: 28/03/2017 07:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 79 0 0 0 0 0 88 5c 3 11 98 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 79 0 0 0 0 0 88 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 79 0 0 0 0 0 88 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 79 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 121 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 88 5c 3 11 = Data: 28/03/2017 08:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 93 0 0 0 0 0 89 5c 3 11 b3 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 93 0 0 0 0 0 89 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 93 0 0 0 0 0 89 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 93 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 147 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 89 5c 3 11 = Data: 28/03/2017 09:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 a7 0 0 0 0 0 8a 5c 3 11 c8 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 a7 0 0 0 0 0 8a 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 a7 0 0 0 0 0 8a 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 a7 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 167 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8a 5c 3 11 = Data: 28/03/2017 10:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 a0 0 0 0 0 0 8b 5c 3 11 c2 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 a0 0 0 0 0 0 8b 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 a0 0 0 0 0 0 8b 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 a0 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 160 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8b 5c 3 11 = Data: 28/03/2017 11:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 9c 0 0 0 0 0 8c 5c 3 11 bf 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 9c 0 0 0 0 0 8c 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 9c 0 0 0 0 0 8c 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 9c 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 156 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8c 5c 3 11 = Data: 28/03/2017 12:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 94 0 0 0 0 0 8d 5c 3 11 b8 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 94 0 0 0 0 0 8d 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 94 0 0 0 0 0 8d 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 94 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 148 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8d 5c 3 11 = Data: 28/03/2017 13:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 94 0 0 0 0 0 8e 5c 3 11 b9 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 94 0 0 0 0 0 8e 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 94 0 0 0 0 0 8e 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 94 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 148 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8e 5c 3 11 = Data: 28/03/2017 14:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 8f 0 0 0 0 0 8f 5c 3 11 b5 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 8f 0 0 0 0 0 8f 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 8f 0 0 0 0 0 8f 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 8f 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 143 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 8f 5c 3 11 = Data: 28/03/2017 15:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 93 0 0 0 0 0 90 5c 3 11 ba 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 93 0 0 0 0 0 90 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 93 0 0 0 0 0 90 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 93 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 147 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 90 5c 3 11 = Data: 28/03/2017 16:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 8f 0 0 0 0 0 91 5c 3 11 b7 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 8f 0 0 0 0 0 91 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 8f 0 0 0 0 0 91 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 8f 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 143 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 91 5c 3 11 = Data: 28/03/2017 17:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 c4 0 0 0 0 0 92 5c 3 11 ed 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 c4 0 0 0 0 0 92 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 c4 0 0 0 0 0 92 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 c4 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 196 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 92 5c 3 11 = Data: 28/03/2017 18:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 9b 0 0 0 0 0 93 5c 3 11 c5 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 9b 0 0 0 0 0 93 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 9b 0 0 0 0 0 93 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 9b 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 155 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 93 5c 3 11 = Data: 28/03/2017 19:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 95 0 0 0 0 0 94 5c 3 11 c0 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 95 0 0 0 0 0 94 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 95 0 0 0 0 0 94 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 95 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 149 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 94 5c 3 11 = Data: 28/03/2017 20:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 7c 0 0 0 0 0 95 5c 3 11 a8 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 7c 0 0 0 0 0 95 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 7c 0 0 0 0 0 95 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 7c 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 124 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 95 5c 3 11 = Data: 28/03/2017 21:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 7b 0 0 0 0 0 96 5c 3 11 a8 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 7b 0 0 0 0 0 96 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 7b 0 0 0 0 0 96 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 7b 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 123 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 96 5c 3 11 = Data: 28/03/2017 22:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 7c 0 0 0 0 0 97 5c 3 11 aa 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 7c 0 0 0 0 0 97 5c 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 7c 0 0 0 0 0 97 5c 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 7c 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 124 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 97 5c 3 11 = Data: 28/03/2017 23:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  26 bytes: 68 14 14 68 8 1 0 b 1 5 1 0 b 1 7a 0 0 0 0 0 80 7d 3 11 b2 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	17 bytes: b 1 5 1 0 b 1 7a 0 0 0 0 0 80 7d 3 11 
	<iud>
	  6 bytes: b 1 5 1 0 b 
	  idt: 0xb: [ASDU 11: TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE, 4 OCTETOS (INCREMENTOS DE ENERGÍA, EN KWH O KVARH)]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0x5: [T=False, PN=False, Causa de transmissió=5: PETICION O SOLICITADA (REQUEST OR REQUESTED)]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  11 bytes: 1 7a 0 0 0 0 0 80 7d 3 11 
	  Amb Etiqueta comuna de temps tipus a (5 bytes)
	  <objecte>
		6 bytes:  1 7a 0 0 0 0 
		Registre 0x1=1: Totales Integrados de Activa Entrante
		Energia (kWh): 122 (kWh o kVARh)
		byte Cualificador: 0x0: [iv,ca,cy,vh,mp,in,al,res]
	  </objecte>
		[ETIQUETA] tipus a (5 bytes): 0 80 7d 3 11 = Data: 29/03/2017 00:00
	</objectesInfo>
  </asdu>
</missatge>

RESPOSTA
<missatge>
  27 bytes: 68 15 15 68 8 1 0 7b 1 a 1 0 b 1 1 0 0 1c 3 11 0 0 1d 3 11 fe 16 
  <control>
	Byte control: 0x8=8=0b1000
	bit PRM=0: Aquest missatge es una RESPOSTA
	FUN: 0b1000 [Funció 8] [Resposta: DADES DE L'USUARI]
  </control>
  <asdu>
	18 bytes: 7b 1 a 1 0 b 1 1 0 0 1c 3 11 0 0 1d 3 11 
	<iud>
	  6 bytes: 7b 1 a 1 0 b 
	  idt: 0x7b: [ASDU 123: LEER TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES]
	  qev: 0x1=0b1: [SQ=False, N=1 objectes d'informació]
	  cdt: 0xa: [T=False, PN=False, Causa de transmissió=10: FINALIZACION DE LA ACTIVACION]
	  dco->registre: 0xb=11: Totales integrados con período de integración 1 (curva de carga)
	</iud>
	<objectesInfo>
	  12 bytes: 1 1 0 0 1c 3 11 0 0 1d 3 11 
	  <objecte>
		12 bytes:  1 1 0 0 1c 3 11 0 0 1d 3 11 
		Direcció inici: 1: Totales Integrados de Activa Entrante
		Direcció final: 1: Totales Integrados de Activa Entrante
		[ETIQUETA] tipus a (5 bytes): 0 0 1c 3 11 = Data: 28/03/2017 00:00
		[ETIQUETA] tipus a (5 bytes): 0 0 1d 3 11 = Data: 29/03/2017 00:00
	  </objecte>
	</objectesInfo>
  </asdu>
</missatge>

CORBA POTÈNCIA
==============
28/03/2017 01:00 108 kW
28/03/2017 02:00 112 kW
28/03/2017 03:00 112 kW
28/03/2017 04:00 115 kW
28/03/2017 05:00 107 kW
28/03/2017 06:00 119 kW
28/03/2017 07:00 119 kW
28/03/2017 08:00 121 kW
28/03/2017 09:00 147 kW
28/03/2017 10:00 167 kW
28/03/2017 11:00 160 kW
28/03/2017 12:00 156 kW
28/03/2017 13:00 148 kW
28/03/2017 14:00 148 kW
28/03/2017 15:00 143 kW
28/03/2017 16:00 147 kW
28/03/2017 17:00 143 kW
28/03/2017 18:00 196 kW
28/03/2017 19:00 155 kW
28/03/2017 20:00 149 kW
28/03/2017 21:00 124 kW
28/03/2017 22:00 123 kW
28/03/2017 23:00 124 kW
29/03/2017 00:00 122 kW
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

