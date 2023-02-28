import socket
import webbrowser
from bs4 import BeautifulSoup

def get_content(html):
	s = BeautifulSoup("<!doctype html>" + html, "html.parser")
	refs = s.find_all('a', class_ = "gbzt")
	return refs

site = "www.google.com"

socketA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketA.connect((site, 80))
buff = 512

# print(socketA.recv(buff).decode("utf-8"))

socketA.send(("GET / HTTP/1.1\r\nHost: " + site + "\r\n\r\n").encode("utf-8"))

msg = ''

while "</html>" not in msg:
	msg += socketA.recv(buff).decode("utf-8")

msg = msg.split("<!doctype html>")[1]

ref = get_content(msg)[1]

# print(str(ref))
ref2 = str(ref).split('\"')
print(msg)

webbrowser.open(ref2[3], new = 2)

socketA.close()

