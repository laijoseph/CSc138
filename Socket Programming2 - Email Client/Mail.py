from socket import *
import ssl
import base64

mailServer = 'smtp.office365.com'
serverPort = 587

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

heloCommand = 'Helo Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'

clientSocket.send('starttls\r\n')
recv1 = clientSocket.recv(1024)
print recv1

secureConnect = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
secureConnect.send(heloCommand)
secureConnect.send('auth login\r\n')
recv1 = secureConnect.recv(1024)

print recv1

user = 'jl3986@csus.edu'
pw = [REDACTED]

target = 'js2000honda@gmail.com'
subject = '138 test'
body = 'hi'

secureConnect.send(base64.b64encode(user)+'\r\n')
secureConnect.send(base64.b64encode(pw)+'\r\n')

print secureConnect.recv(1024)
print secureConnect.recv(1024)

def sendmail (sender, receiver, subj, msg):
    secureConnect.send('mail from: ' + sender + '\r\n')
    print secureConnect.recv(1024)
    secureConnect.send('rcpt to: ' + receiver + '\r\n')
    print secureConnect.recv(1024)
    secureConnect.send('data\r\n')
    print secureConnect.recv(1024)
    secureConnect.send('To: ' + receiver + '\r\nSubject: ' + subj +
    ('\r\n' + msg + '.'))
    print secureConnect.recv(1024)

sendmail(('<' + user + '>'), ('<' + target + '>'), subject, body)

secureConnect.close()
clientSocket.close()