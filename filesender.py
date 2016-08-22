import socket
from urllib2 import urlopen
def writeFile(filename, lines):
    fw = open(filename,'w')
    for line in lines:
        fw.write(line)
    fw.flush()
    fw.close()
def readFile(filename):
    fr = open(filename,'r')
    lines = fr.read().splitlines()
    return lines

def create_conn(port):
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen(1)
    hostname = socket.gethostbyname(socket.gethostname())
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print 'listening on {}: {} - lan'.format(hostname, port)
    print 'listening on {}: {} - public'.format(my_ip, port)
    (clientsocket, address) = serversocket.accept()
    clientsocket.send('connection made\n')
    done = 0
    writingfile = 0
    lines = []
    fn = ''
    fw = ''
    while done == 0:
        if writingfile == 0:
            cmd = clientsocket.recv(1024)
            if "writeFile:" in cmd:
                fnwithline = cmd[10:]
                l = len(fnwithline) - 1
                fn = fnwithline[:l]
                writingfile = 1
                lines = []
                clientsocket.send('Starting to write to {}\n'.format(fn))
            elif cmd=="quit":
                done = 1
            else:
                clientsocket.send('Fail. Not a valid command.\n')
        else:
            line = clientsocket.recv(1024)
            if "{{stopWritingFile}}" in line:
                writeFile(fn,lines)
                writingfile = 0
                clientsocket.send('done.\n')
            else:
                lines.append(line)
                clientsocket.send('recieved.\n')
def connect(ip,port):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    print s.recv(1024)
    run = 1
    while run:
        command=raw_input('Fsend>>>')
        if command == 'help':
            print 'help - help menu'
            print 'send <filename> - to send a file'
            print 'quit to quit'
        elif 'send ' in command:
            fn = command[5:]
            lines = readFile(fn)
            s.send('writeFile:{}\n'.format(fn))
            print s.recv(1024)
            for l in lines:
                s.send('{}\n'.format(l))
                r = s.recv(1024)
            s.send('{{stopWritingFile}}\n')
            print s.recv(1024)
        elif 'quit' in command:
            run = 0
            s.send('quit\n')
        else:
            print 'invalid command.'
opt = raw_input('Connect or recieve connection? (c/r): ')
if opt=='c':
    ip=raw_input('ip: ')
    port=raw_input('port: ')
    connect(ip,int(port))
elif opt=='r':
    port = int(raw_input('port: '))
    create_conn(port)
else:
    print 'invalid option.'
