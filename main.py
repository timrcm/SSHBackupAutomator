# STOP! Fill out blankconfig.py and rename it to config.py before running.

import paramiko 
import time

import config

ssh = paramiko.SSHClient() 

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(config.host, username=config.user, password=config.pw)

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('''
ls -a
echo " "
uptime
echo " "
ls -a /var/www
''')

ssh_stdout = ssh_stdout.readlines()
time.sleep(1)
ssh.close()

for line in ssh_stdout:
    print(line, end='')
