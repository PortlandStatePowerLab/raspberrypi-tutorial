#! /usr/bin/python3
import os
import time
import paramiko

print('Hey, welcome!')# Welcome message. Not important. I was bored.
os.system('sudo hostname -I >> ip.log') # os command to get ip address
os.system('sudo hostname >> ip.log') # os command to get the hostname
ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('**.***.***.**', username='*****', password='***') # fill in credentials for the remote host. Ask Midrar if you don't have a host credentials.
sftp = ssh.open_sftp()
local_file = 'ip.log' # name of the file you want to send over to the remote host.
remote_host = '/home/deras/Desktop/store_ip.log' #Directory is not enough. Need to specify a file name!
sftp.put(local_file, remote_host)
sftp.close()
ssh.close()
os.system('sudo rm ip.log')
