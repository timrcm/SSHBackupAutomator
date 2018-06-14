# STOP! Fill out blankconfig.py and rename it to config.py before running.

import paramiko 
from time import sleep

import config

ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def cisco_backup(cmd): 
    for X in config.CISCO_DEVICES:
        ssh.connect(X[0], username=X[1], password=X[2])
        cmdtype = cmd.replace(' ', '.')
        path = f'{X[0]}.{cmdtype}.txt'
        backup_file = open(path, 'w+', newline='\n')

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh_stdout = ssh_stdout.readlines()

        sleep(1)
        ssh.close()

        for line in ssh_stdout:
            backup_file.write(line)

        print(f"{path} created.")

def main():
    print("Starting backups...")
    cisco_backup('show run')
    cisco_backup('show ver')
    cisco_backup('show flash')
    print("All devices found in config completed.")
    exit(0)

main()