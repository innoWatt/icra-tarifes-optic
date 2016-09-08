

'''

        import comptador
        com = comptador.Comptador()

        import mysocket
	#new socket
	sock=mysocket.mysocket()
	sock.connect('192.168.103.63',3333)
	sock.mysend('hola')
	print sock.myreceive()


'''
import socket
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.103.63",3333))

#6.1.1 direccion control
# start - longi - longi - start - control - direccion - 2 octetos - asdu - checksum - end
# 1B      1B     1B     1B      1B        1B          2B          var.   1B         1B 
start     = 0x68
longi     = 1+1+0 # 1 + num bytes direccion + num bytes asdu
control   = 0b01111001
direccion = 0x1
octetos   = 0
asdu      = 0
checksum  = start+longi+longi+start+control+direccion+octetos+asdu
end       = 0x16
trama=[start,longi,longi,start,control,direccion,octetos,asdu,checksum,end]

#ENVIA
for i in trama: sock.send(bytes(i))

msg=""
while 1:
    print('pre')
    chunk = sock.recv(1024)
    print 'post'
    if not chunk: 
        break
    msg = msg + chunk
    msg = str(msg, 'UTF-8')

print('Received:', unpack(msg))
