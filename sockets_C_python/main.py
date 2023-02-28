import socket

server_socket = socket.socket()

server_socket.bind(("127.0.0.1", 5000))
server_socket.listen(2)

connect, addr = server_socket.accept()

print("connected on:", addr)

while True:
	data = connect.recv(65)
	if not data:
		break
	
	data = data.decode("utf-8")
	
	connect.send(data.upper().encode("utf-8"))
	print(data)
	
connect.close()

