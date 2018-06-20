# STOP! Fill out blankconfig.py and rename it to config.py before running.

from time import sleep
import paramiko
import wget

import config

# Instantiate paramiko  
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def ssh_connect(X):
    '''Takes a list of tuples from config.py as an argument and converts
        them to the host, username, and password for paramiko to connect'''
    try:
        ssh.connect(X[0], username=X[1], password=X[2])
    except paramiko.AuthenticationException:
        print(f"Failed to authenticate to {X[0]}")
    except:
        print(f"Unknown failure when connecting to {X[0]}")


def cisco_backup(cmd):
    '''Takes the command to run as an argument, and then spits the output to a .txt'''
    for X in config.CISCO_DEVICES:
        ssh_connect(X)

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


def apache_backup():
    '''Zips up the apache directory and transfers it
        This is done via wget until I can figure out how
        to make paramiko's sftp transport work correctly'''
    for X in config.APACHE_SERVERS:

        # Connect via SSH and zip the file
        ssh_connect(X)
        ssh.exec_command(f'tar -zcvf ~/{X[0]}.tar.gz {config.APACHE_DIRECTORY}')
        sleep(30) # Paramiko doesn't give the server enough time to finish zipping larger directories

        # Download the new zipped directory & delete it when done
        ssh.exec_command(f'mv ~/{X[0]}.tar.gz {config.APACHE_DIRECTORY}/{config.APACHE_HTML_ROOT_DIR}/{X[0]}.tar.gz')
        sleep(5)
        wget.download(f'http://{X[0]}/{X[0]}.tar.gz')
        ssh.exec_command(f'rm {config.APACHE_DIRECTORY}/{config.APACHE_HTML_ROOT_DIR}/{X[0]}.tar.gz')
        ssh.close()


        # transport = paramiko.Transport({X[0]}, 22)

        # try:
        #     transport.connect(username = {X[1]}, password = {X[2]})
        # except TimeoutError:
        #     print("Timeout error")

        # sftp = paramiko.SFTPClient.from_transport(transport)
        # sftp.get(f'~/{X[0]}.tar.gz', '{X[0]}.tar.gz')


def main():
    print("Starting backups...")
    cisco_backup('show run')
    cisco_backup('show ver')
    cisco_backup('show flash')
    apache_backup()
    print("\n Done.")
    exit(0)


if __name__ == '__main__':
    main()
