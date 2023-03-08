import ssl
import socket
import base64


mailpop3 = "pop.mail.ru" # FIX IT
mailsmtp = "smtp.mail.ru" # FIX IT TOO


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


srv.bind(('127.0.0.1', 1114))
srv.listen(1)


temp_socket, address = srv.accept()


buff = 512


def sending_msg_smtp():
  global srv
  global buff
  global mailsmtp
  global temp_socket
  global address
  login = temp_socket.recv(buff).decode('utf-8')
  passwrd = temp_socket.recv(buff).decode('utf-8')
  login2 = login
  passwrd2 = passwrd
  subj = temp_socket.recv(buff).decode('utf-8')
  main = temp_socket.recv(buff).decode('utf-8')


  print("login: ", login)
  print("passwrd: ", passwrd)
  print("subj: ", subj)
  print("main: ", main)
  
  srv.close()
  
  # creating a connection ################
  
  sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sc.connect((mailsmtp, 465))
  safeSocket = ssl.wrap_socket(sc)
  
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  safeSocket.send("EHLO smtp.mail.ru\r\n".encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  # authorization ###############
  
  safeSocket.send("AUTH LOGIN\r\n".encode('utf-8'))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  login = base64.b64encode(login.encode("utf-8")) + b"\r\n"
  # safeSocket.send((login + "\r\n").encode('utf-8'))
  safeSocket.send(login)
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  passwrd = base64.b64encode(passwrd.encode("utf-8")) + b"\r\n"
  # safeSocket.send((passwrd + "\r\n").encode('utf-8'))
  safeSocket.send(passwrd)
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  # sending our message ################


  text = "MAIL FROM:" + login2 + "\r\n"
  
  safeSocket.send(text.encode('utf-8'))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  safeSocket.send(("RCPT TO:" + login2 + "\r\n").encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  safeSocket.send("DATA\r\n".encode('utf-8'))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  # IF ANY PROBLEM IS OCCURED IT IS BECAUSE OF THIS TEXT VATIABLE (FIX IT ('\n\n.\r\n'))
  
  text = "From:" + login2 + "\nTo:" + login2 + '\nSubject:' + subj + "\n" + main + "\r\n.\r\n"
  
  safeSocket.send(text.encode('utf-8'))
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  # QUITTING FROM THIS SESSION ###########
  
  safeSocket.send("QUIT\r\n".encode("utf-8")) # HERE MAY BE AN ERROR AS WELL ("QUIT \r\n")
  rc = safeSocket.recv(buff)
  print("SMTP >> ", rc.decode('utf-8'))
  
  safeSocket.close()
  sc.close()




def deleting_msg_pop3():
  global srv
  global buff
  global mailpop3
  global temp_socket
  global address
  login = temp_socket.recv(buff).decode('utf-8')
  passwrd = temp_socket.recv(buff).decode('utf-8')
  login2 = login
  passwrd2 = passwrd
  subj = temp_socket.recv(buff).decode('utf-8')
  main = temp_socket.recv(buff).decode('utf-8')
  
  srv.close()
  
  # creating a connection ################
  
  sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sc.connect((mailpop3, 995))
  safeSocket = ssl.wrap_socket(sc)
  
  rc = safeSocket.recv(buff)
  print("POP3 >> ", rc.decode('utf-8'))
  
  # authorization ################
  
  safeSocket.send(("USER " + login2 + "\r\n").encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("POP3 >> ", rc.decode('utf-8'))
  
  safeSocket.send(("PASS " + passwrd2 + "\r\n").encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("POP3 >> ", rc.decode('utf-8'))
  
  # deleting the first message ################
  
  safeSocket.send(("DELE 1" + "\r\n").encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("POP3 >> ", rc.decode('utf-8'))
  
  # quitting from our pop3 app ############
  
  safeSocket.send("QUIT\r\n".encode("utf-8"))
  rc = safeSocket.recv(buff)
  print("POP3 >> ", rc.decode('utf-8'))
  
  safeSocket.close()
  sc.close()




FL = temp_socket.recv(buff).decode("utf-8")


if FL == "SEND":
  sending_msg_smtp()
elf FL == "DEL":
  deleting_msg_pop3()
