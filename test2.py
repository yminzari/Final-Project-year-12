import socket
import struct
import protocol
import PyQ5_windows
import sys
from PyQt5 import QtWidgets
import PyQt5


def ShowRegister(CurrentWindow):
    window = QtWidgets.QMainWindow()
    RegisterUi = PyQ5_windows.Ui_RegisterWindow()
    RegisterUi.setupUi(window, Enter, ShowLogIn)
    window.show()
    CurrentWindow.close()


def ShowLogIn(CurrentWindow):
    window = QtWidgets.QMainWindow()
    LogInUi = PyQ5_windows.Ui_LogInWindow()
    LogInUi.setupUi(window, Enter, ShowRegister)
    window.show()
    CurrentWindow.close()


# Use callback very smart
def Enter(Username:PyQt5.QtWidgets.QLineEdit, FirstName:PyQt5.QtWidgets.QLineEdit, LastName:PyQt5.QtWidgets.QLineEdit, Password_LineEdit:PyQt5.QtWidgets.QLineEdit, ConfirmPassword_LineEdit:PyQt5.QtWidgets.QLineEdit, ClassName):
    global RegisterOrLogIn
    global UserInformation
    if ClassName == "Register":
        if ConfirmPassword_LineEdit.text() != Password_LineEdit.text():
            return "Password and Confirm Password are different"
        else:
            RegisterOrLogIn = "1"
            UserInformation = {"Username": Username.text(), "Password": Password_LineEdit.text(), "FirstName": FirstName.text(), "LastName": LastName.text()}
            send_data(client_socket, RegisterOrLogIn, 1, "")
            data = UserInformation
            send_data(client_socket, data, 1, "")
            data_recv = recv_msg(client_socket)
            print(data_recv["msg"])
            return data_recv["msg"]
    elif ClassName == "LogIn":
        RegisterOrLogIn = "2"
        UserInformation = {"Username": Username.text(), "Password": Password_LineEdit.text()}
        send_data(client_socket, RegisterOrLogIn, 1, "")
        data = UserInformation
        send_data(client_socket, data, 1, "")
        data_recv = recv_msg(client_socket)
        print(data_recv["msg"])
        return data_recv["msg"]


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
        data = UserInformation


def recv_msg(conn):
    data_size = protocol.recvall(conn, 4)
    length = struct.unpack('>I', data_size)[0]
    data_recv = protocol.recvall(conn, length)
    data_recv = protocol.parse_header(data_recv)
    return data_recv


host = '127.0.0.1'
port = 12345
RegisterWindow = PyQ5_windows.Ui_RegisterWindow()
LogInWindow = PyQ5_windows.Ui_LogInWindow()
LogInOrRegister = PyQ5_windows.Ui_LogInOrRegister()
UserInformation = {}
RegisterOrLogIn = ""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))


def main():
    global LogInOrRegister
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    LogInOrRegisterui = LogInOrRegister
    LogInOrRegisterui.setupUi(MainWindow, ShowRegister, ShowLogIn)
    MainWindow.show()
    app.exec_()
    # data = input("pls enter 1 for register and 2 for log in: ")
    data = RegisterOrLogIn
    send_data(client_socket, data, 1, "")
    # data = input("pls enter username and password with | between and 6 or more characters with at least one number in the password: ")
    data = UserInformation
    # if "|" not in data:
    #    print("didn't put | in the username and password")
    #    quit()
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
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()
