import socket
import struct
from PyQt5.QtWidgets import QFileDialog
from PyQ5_windows import Ui_file_window
import protocol
import PyQ5_windows
import sys
from PyQt5 import QtWidgets
import PyQt5
import os


def update_file(file_path):
    print(file_path)
    req_dir = {"req": "update", "file_path": file_path}
    send_data(client_socket, req_dir, 1, "")
    with open(file_path, "rb") as data:
        print(data)
        file = data.read()
    send_data(client_socket, file, 2, file_path)
    answer = recv_msg(client_socket)["msg"]
    file_name = recv_msg(client_socket)["msg"]
    return answer, file_name


def download_file(file_path, download_path):
    req_dir = {"req": "download", "file_path": file_path}
    send_data(client_socket, req_dir, 1, "")
    file_msg = recv_msg(client_socket)
    file_path_dict = file_msg.get("file_path").split("/")
    print(download_path + "/" + file_path_dict[-1])
    if os.path.exists(download_path + "/" + file_path_dict[-1]):
        try:
            os.rename(download_path + "/" + file_path_dict[-1], download_path + "/" + file_path_dict[-1])
            print("ok")
        except OSError as e:
            print("file is being used. to download close the file and retry")
            return "file is being used"
    with open(download_path + "/" + file_path_dict[-1], 'wb') as file:
        print("hej")
        file.write(file_msg.get("msg"))
    return ""


# need to send added files to the server and deal with responses appropriately
def ShowFileWindow(CurrentWindow, files):
    global file_window
    print(files)
    file_window = QtWidgets.QMainWindow()
    FileWindow_ui = PyQ5_windows.Ui_file_window_ver2()
    FileWindow_ui.setupUi_file_window(file_window, add_file, search_by_criteria, download_file, update_file)
    try:
        if len(files) > 0:
            for file in files:
                PyQ5_windows.Ui_file_window_ver2.add_file_to_list(FileWindow_ui, file)
        file_window.show()
        CurrentWindow.close()
    except Exception as e:
        print(e)


def add_file():
    file_path = QFileDialog.getOpenFileName(None, "upload a file", os.path.expanduser("~"), "All (*.txt *.docx *.pdf *.xlsx) ;;Docx (*.docx);; text (*.txt);; PDF (*.pdf);; Excel (*.xlsx);")
    if file_path[0] == "":
        return "", "no file was selected"
    print(file_path[0])
    with open(file_path[0], "rb") as data:
        print(data)
        file = data.read()
    file_name = file_path[0].split("/")[-1]
    send_data(client_socket, file, 2, file_path[0])
    answer = recv_msg(client_socket)["msg"]
    file_name = recv_msg(client_socket)["msg"]
    print(answer)
    return file_name, answer, file_path[0]
    # file_list.addItem(file_name)


def search_by_criteria(search, file_type, date, start_date, end_date):
    ext_query = ""
    if search != "":
        ext_query = f"and (file_path like '%{search}%')"
    if file_type != "All":
        ext_query += f" and (file_type ='{file_type}')"
    if date != "ALL":
        if date == "today":
            ext_query += " and (date_create > trunc(sysdate))"
        if date == "last 7 days":
            ext_query += " and (date_create > sysdate-7)"
        if date == "last 30 days":
            ext_query += " and (date_create > sysdate-30)"
        if date == "this year":
            ext_query += " and (to_char(date_create,'yyyy') =  to_char(sysdate,'yyyy'))"
        if date == "custom date range":
            if start_date != "" and end_date != "":
                ext_query += f" and (date_create between to_date('{start_date}','mm/dd/yyyy') and to_date('{end_date}','mm/dd/yyyy'))"
    req_dir = {"req": "ext_query", "ext_query": ext_query}
    send_data(client_socket, req_dir, 1, "")
    files = recv_msg(client_socket)
    return files["msg"]


def ShowRegister(CurrentWindow):
    window = QtWidgets.QMainWindow()
    RegisterUi = PyQ5_windows.Ui_RegisterWindow()
    RegisterUi.setupUi(window, Enter, ShowLogIn, ShowFileWindow)
    window.show()
    CurrentWindow.close()


def ShowLogIn(CurrentWindow):
    window = QtWidgets.QMainWindow()
    LogInUi = PyQ5_windows.Ui_LogInWindow()
    LogInUi.setupUi(window, Enter, ShowRegister, ShowFileWindow)
    window.show()
    CurrentWindow.close()


# Use callback very smart
def Enter(Username:PyQt5.QtWidgets.QLineEdit, FirstName:PyQt5.QtWidgets.QLineEdit, LastName:PyQt5.QtWidgets.QLineEdit, Password_LineEdit:PyQt5.QtWidgets.QLineEdit, ConfirmPassword_LineEdit:PyQt5.QtWidgets.QLineEdit, ClassName):
    global RegisterOrLogIn
    global UserInformation
    if ClassName == "Register":
        if ConfirmPassword_LineEdit.text() != Password_LineEdit.text():
            return "The password and the password conformation do not match"
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
        files = recv_msg(client_socket)["msg"]
        print(data_recv["msg"])
        return data_recv["msg"], files


def send_data(conn, data, operation, file_to_send):
    if operation == 1:
        data = protocol.create_string_header(data)
        length = len(data)
        packed_length = struct.pack('>I', length)
        # Send the packed length over the socket
        conn.sendall(packed_length)
        conn.sendall(data)
    elif operation == 2:
        # print(os.path.getsize(file_to_send))
        data = protocol.create_file_header(data, file_to_send)
        # print(data)
        length = len(data)
        # print(length)
        packed_length = struct.pack('>I', length)
        # Send the packed length over the socket
        # print(packed_length)
        conn.sendall(packed_length)
        conn.sendall(data)
        # data = UserInformation


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
FileWindow = PyQ5_windows.Ui_file_window()
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
