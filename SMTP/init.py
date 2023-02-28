import socket


# reading login and password from the file


f = open("acc.txt", 'r')


login = f.readline()
passwrd = f.readline()


login = login.replace('\n', "")


f.close()


print(login, passwrd, sep = '\n')


# initializing our app
# creating the socket and sending our data


cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


cl.connect(("127.0.0.1", 1114))


cl.send(input("Enter <SEND> for sending a template message\nEnter <DEL> for deleting the first message: ").encode("utf-8"))


subj = input("Subject: ")
main = input("Main: ")


cl.send(login.encode("utf-8"))
cl.send(passwrd.encode("utf-8"))
cl.send(subj.encode('utf-8'))
cl.send(main.encode('utf-8'))


cl.close()

