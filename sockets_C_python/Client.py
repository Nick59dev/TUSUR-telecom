import socket

client_socket = socket.socket()

client_socket.connect(("127.0.0.1", 5000))

while True:
	message = input(">> ")
	client_socket.send(message.encode("utf-8"))
	
	data = client_socket.recv(65)
	
	if not data:
		break
	
	print("SERVER>>", str(data))
	
print('bye')

client_socket.close()

