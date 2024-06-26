import socket
import struct
import protocol
import PyQ5_windows
import sys
from PyQt5 import QtWidgets
import PyQt5


# Use callback very smart
def Enter(Username:PyQt5.QtWidgets.QLineEdit, FirstName:PyQt5.QtWidgets.QLineEdit, LastName:PyQt5.QtWidgets.QLineEdit, Password_LineEdit:PyQt5.QtWidgets.QLineEdit, ConfirmPassword_LineEdit:PyQt5.QtWidgets.QLineEdit, ClassName):
    print(f"{Username.text()} {FirstName.text()} {LastName.text()} {Password_LineEdit.text()} {ConfirmPassword_LineEdit.text()}")
    if ClassName == "Register":
        # handle register
        # return "connection succeed"
        return "foasnfioasdnaofnasoif"
        pass
    elif ClassName == "LogIn":
        # handle LogIn
        return "connection succeed"
        pass


def send_data(conn, data, operation, file_to_send):
    if operation == 1:
        data = protocol.create_string_header(data)
        length = len(data)
        packed_length = struct.pack('>I', length)
        # Send the packed length over the socket
        conn.sendall(packed_length)
        conn.sendall(data)
    elif operation == 2:
        data = protocol.create_file_header(data, file_to_send)
        length = len(data)
        packed_length = struct.pack('>I', length)
        # Send the packed length over the socket
        conn.sendall(packed_length)
        conn.sendall(data)


def recv_msg(conn):
    data_size = protocol.recvall(conn, 4)
    length = struct.unpack('>I', data_size)[0]
    data_recv = protocol.recvall(conn, length)
    data_recv = protocol.parse_header(data_recv)
    return data_recv


host = '127.0.0.1'
port = 12345


def main():
    while True:
        jorge = PyQ5_windows.Ui_LogInOrRegister(Enter)
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = jorge
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    data = input("pls enter 1 for register and 2 for log in: ")
    send_data(client_socket, data, 1, "")
    data = input("pls enter username and password with | between and 6 or more characters with at least one number in the password: ")
    if "|" not in data:
        print("didn't put | in the username and password")
        quit()
    send_data(client_socket, data, 1, "")
    data_recv = recv_msg(client_socket)
    print(data_recv["msg"])
    if data_recv["msg"] != "connection succeed":
        quit()
    file_to_send = "C:\\Users\\yminz\\Downloads\\shared_moment.gif"
    req = ""
    while req.upper() != "EXIT":
        req = input("pls enter file for sending a file, pls enter req for sending a request, pls enter exit to exit: ")
        if req.upper() == "FILE":
            with open(file_to_send, 'rb') as file:
                filedata = file.read()
                send_data(client_socket, filedata, 2, file_to_send)
        elif req.upper() == "REQ":
            data = input("pls enter the request: ")
            send_data(client_socket, data, 1, "")
            data_recv = recv_msg(client_socket)
            print(data_recv["msg"])
    data = "exit"
    send_data(client_socket, data, 1, "")
    client_socket.close()


if __name__ == "__main__":
    main()
