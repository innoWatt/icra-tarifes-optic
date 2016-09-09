
'''
        import comptador
        com = comptador.Comptador()
'''

import socket
import sys

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.103.63",3333))

#envia una trama i rep la resposta
trama=[16,73,1,0,74,22]

sock.send(str(trama))

chunks = []
bytes_recd = 0


while 1:
    chunk = sock.recv(1024)
    if chunk == '': break
    chunks.append(chunk)
    bytes_recd = bytes_recd + len(chunk)
    sys.stdout.write('.')

print(" Received "+str(bytes_recd)+" bytes")
print(chunks)
