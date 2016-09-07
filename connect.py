import mysocket

'''
import socket
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser.connect(("192.168.103.63",3333))
'''

#new socket
sock=mysocket.mysocket()
sock.connect('192.168.103.63',3333)
sock.mysend('hola')

print sock.myreceive()
