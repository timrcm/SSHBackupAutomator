# STOP! Fill out blankconfig.py and rename it to config.py before running.
# Takes a list of tuples from config.py and converts them to the host, user, and pw 

import paramiko
import config

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# class ssh_start(object):
#     def __init__(self):
#         self.devices = []

#     def __call__(self, cmd): 
#         for X in self.devices:
#             ssh.connect(X[0], username=X[1], password=X[2])
            

# class cisco_backup(ssh_start):
#     def __init__(self):
#         self.devices = config.CISCO_DEVICES


def generic_command(cmd):
    for X in config.CISCO_DEVICES:
        ssh.connect(X[0], username=X[1], password=X[2])
        
        cmdtype = cmd.replace(' ', '.') # Unnecessary but I prefer this naming convention
        path = f'{X[0]}.{cmdtype}.txt'
        backup_file = open(path, 'w+', newline='\n')

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh_stdout = ssh_stdout.readlines()

        ssh.close()

        for line in ssh_stdout:
            backup_file.write(line)

        print(f"{path} created.")

def main():
    print("Starting backups...")
    generic_command('show run')
    generic_command('show ver')
    generic_command('show flash')
    print("All devices found in config completed.")
    exit(0)

if __name__ == '__main__':
    main()
