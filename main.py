# SSHBackupAutomator
# Python 3.7
# Fill out blankconfig.py and rename it to config.py before running.

import asyncio
from time import sleep

import paramiko
import wget

import config

# Instantiate paramiko  
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class start(object):

    def __init__(self, devices, devicetype):
        self.devices = devices
        self.devicetype = devicetype

        if self.devicetype == "cisco":
            self.cisco_backup('show run')
            self.cisco_backup('show ver')
            self.cisco_backup('show flash')
        elif self.devicetype == "apache":
            self.apache_backup()
        else:
            print("Unknown backup selection")
            exit(1)


    def __call__(self):
        pass


    def ssh_conn(self, X):
        if X[2] == 'ASK':
            X = (X[0]), (X[1]), (input(f"Enter the password for {X[0]}: "))

        try: 
            ssh.connect(X[0], username=X[1], password=X[2])
        except paramiko.AuthenticationException:
            print(f"Failed to authenticate to {X[0]}")
        except:
            print(f"Unknown failure when connecting to {X[0]}")


    def cisco_backup(self, cmd):
        for X in self.devices:
            self.ssh_conn(X)

            cmdtype = cmd.replace(' ', '.') # Unnecessary but I prefer this naming convention
            path = f'{X[0]}.{cmdtype}.txt'
            backup_file = open(path, 'w+', newline='\n')

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
            sleep(5) # Give the device enough time to respond 
            ssh_stdout = ssh_stdout.readlines()
            ssh.close()

            for line in ssh_stdout:
                backup_file.write(line)
            print(f"{path} created.")


    def apache_backup(self):
        '''Zips up the apache directory and transfers it
            This is done via wget until I can figure out how
            to make paramiko's sftp transport work correctly'''
        for X in self.devices:
            # Connect via SSH and zip the file
            self.ssh_conn(X)
            ssh.exec_command(f'tar -zcvf ~/{X[0]}.tar.gz {config.APACHE_DIRECTORY}')
            sleep(30) # Paramiko doesn't give the server enough time to finish zipping larger directories

            # Download the new zipped directory & delete it when done
            ssh.exec_command(f'mv ~/{X[0]}.tar.gz {config.APACHE_DIRECTORY}/{config.APACHE_HTML_ROOT_DIR}/{X[0]}.tar.gz')
            sleep(5)
            wget.download(f'http://{X[0]}/{X[0]}.tar.gz')
            ssh.exec_command(f'rm {config.APACHE_DIRECTORY}/{config.APACHE_HTML_ROOT_DIR}/{X[0]}.tar.gz')
            ssh.close()


def main():
    print("Starting backups...")
    start(config.CISCO_DEVICES, 'cisco')
    start(config.APACHE_SERVERS, 'apache')
    print("\n Done.")
    exit(0)


if __name__ == '__main__':
    main()
