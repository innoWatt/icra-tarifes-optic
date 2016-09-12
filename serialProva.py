#FUNCIONA

import serial

#obre serial
ser=serial.Serial()
ser.port="/dev/ttyUSB0"
ser.baudrate=9600
ser.bytesize=8
ser.parity=serial.PARITY_EVEN
ser.stopbits=1
ser.xonxoff=False
ser.rtscts=False
ser.dsrdtr=False
ser.timeout=1
ser.open()
ser.flush()

#munta trama
trama=[0x10,0x49,0x01,0x00,0x4a,0x16]
print("enviant: "+str(trama))

#envia
ser.write(bytearray(trama))
ser.flush()

#resposta
print("resposta:")
resposta=ser.readlines()
print(resposta)
print(type(resposta))

#fi
ser.close()
