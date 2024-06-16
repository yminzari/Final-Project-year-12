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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


def send_exit(exit_msg, aes_cipher):
    """
    sends the exit message to the server
    :param exit_msg: the exit message for the server
    :param aes_cipher: the cypher key
    :return:
    """
    send_data_encrypt(client_socket, exit_msg, 1, "", aes_cipher)
    sys.exit()


def update_file(file_path, aes_cipher):
    """
    send the update request to server with the file to update
    :param file_path: the path of the file to update
    :param aes_cipher: the cypher key
    :return: the answer of the server the name of the file updated
    """
    print(file_path)
    req_dir = {"req": "update", "file_path": file_path}
    send_data_encrypt(client_socket, req_dir, 1, "", aes_cipher)
    with open(file_path, "rb") as data:
        print(data)
        file = data.read()
    send_data_encrypt(client_socket, file, 2, file_path, aes_cipher)
    answer = recv_msg_encrypt(client_socket, aes_cipher)["msg"]
    file_name = recv_msg_encrypt(client_socket, aes_cipher)["msg"]
    return answer, file_name


def download_file(file_path, download_path, aes_cipher):
    """
    sends download request to the server with the name of the file and then writes it to the path Downloads/info_manage
    :param file_path: the file you want to download
    :param download_path: the place you want to download it to
    :param aes_cipher: the cypher key
    :return:
    """
    req_dir = {"req": "download", "file_path": file_path}
    if os.path.exists(download_path):
        print("folder exist")
    else:
        os.mkdir(download_path)
    send_data_encrypt(client_socket, req_dir, 1, "", aes_cipher)
    file_msg = recv_msg_encrypt(client_socket, aes_cipher)
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
def ShowFileWindow(CurrentWindow, files, aes_cipher):
    """
    shows the Main file window
    :param CurrentWindow: the current window that is open
    :param files: list of all the files of the user
    :param aes_cipher: the cypher key
    :return:
    """
    global file_window
    print(files)
    file_window = QtWidgets.QMainWindow()
    FileWindow_ui = PyQ5_windows.Ui_file_window_ver2()
    FileWindow_ui.setupUi_file_window(file_window, add_file, search_by_criteria, download_file, update_file, send_exit, aes_cipher)
    try:
        if len(files) > 0:
            for file in files:
                PyQ5_windows.Ui_file_window_ver2.add_file_to_list(FileWindow_ui, file)
        file_window.show()
        CurrentWindow.close()
    except Exception as e:
        print(e)


def add_file(aes_cipher):
    """
    sends the file the client wants to add to the server
    :param aes_cipher: the cypher key
    :return: updated list of files, the answer of the server, and the path of the file selected
    """
    file_path = QFileDialog.getOpenFileName(None, "upload a file", os.path.expanduser("~"), "All (*.txt *.docx *.pdf *.xlsx) ;;Docx (*.docx);; text (*.txt);; PDF (*.pdf);; Excel (*.xlsx);")
    print(file_path)
    if file_path[0] == "":
        return "", "no file was selected", file_path[0]
    print(file_path[0])
    with open(file_path[0], "rb") as data:
        print(data)
        file = data.read()
    file_name = file_path[0].split("/")[-1]
    send_data_encrypt(client_socket, file, 2, file_path[0], aes_cipher)
    answer = recv_msg_encrypt(client_socket, aes_cipher)["msg"]
    file_name = recv_msg_encrypt(client_socket, aes_cipher)["msg"]
    print(answer)
    return file_name, answer, file_path[0]
    # file_list.addItem(file_name)


def search_by_criteria(search, file_type, date, start_date, end_date,  exact_word, wildcard_word, and_words, or_words, aes_cipher):
    """
    sends to the server list of criteria to search files by
    :param search: file name
    :param file_type: type of the file
    :param date: dates
    :param start_date: if custom date was picked the start date picked
    :param end_date: if custom date was picked the end date picked
    :param exact_word: exact word to search
    :param wildcard_word: wildcard word to search
    :param and_words: list of words to search with and
    :param or_words: list of words to search with or
    :param aes_cipher: the cypher key
    :return: the list of files that answer the criteria
    """
    ext_query = ""
    and_quary = ""
    or_quary = ""
    if exact_word != "":
        exact_word = exact_word.replace("-", "%")
        ext_query += f"and contains(file_text,'{exact_word}') > 0"
    if wildcard_word != "":
        wildcard_word = wildcard_word.replace("-", "%")
        # wildcard_word.replace(" ", "%")
        ext_query += f"and contains(file_text,'%{wildcard_word}%') > 0"
    for word in and_words:
        word = word.replace("-", "%")
        if word != "" and and_quary == "":
            and_quary += f"and contains(file_text,'%{word}%"
        elif word != "" and and_quary != "":
            and_quary += f" and %{word}%"
    if and_quary != "":
        and_quary += "') > 0"
    ext_query += and_quary
    for word in or_words:
        word.replace("-", "%")
        if word != "" and or_quary == "":
            or_quary += f"and contains(file_text,'%{word}%"
        elif word != "" and or_quary != "":
            or_quary += f" or %{word}%"
    if or_quary != "":
        or_quary += "') > 0"
    ext_query += or_quary
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
    send_data_encrypt(client_socket, req_dir, 1, "", aes_cipher)
    files = recv_msg_encrypt(client_socket, aes_cipher)
    return files["msg"]


def ShowRegister(CurrentWindow, aes_cipher):
    """
    shows the register window
    :param CurrentWindow: the window currently open
    :param aes_cipher: the cypher key
    :return:
    """
    window = QtWidgets.QMainWindow()
    RegisterUi = PyQ5_windows.Ui_RegisterWindow()
    RegisterUi.setupUi(window, Enter, ShowLogIn, ShowFileWindow, send_exit, aes_cipher)
    window.show()
    CurrentWindow.close()


def ShowLogIn(CurrentWindow, aes_cipher):
    """
    shows the login window
    :param CurrentWindow: the window currently open
    :param aes_cipher: the cypher key
    :return:
    """
    window = QtWidgets.QMainWindow()
    LogInUi = PyQ5_windows.Ui_LogInWindow()
    LogInUi.setupUi(window, Enter, ShowRegister, ShowFileWindow, send_exit, aes_cipher)
    window.show()
    CurrentWindow.close()


# Use callback very smart
def Enter(Username:PyQt5.QtWidgets.QLineEdit, FirstName:PyQt5.QtWidgets.QLineEdit, LastName:PyQt5.QtWidgets.QLineEdit, Password_LineEdit:PyQt5.QtWidgets.QLineEdit, ConfirmPassword_LineEdit:PyQt5.QtWidgets.QLineEdit, ClassName, aes_cipher):
    """
    sends to the server the information inputted by the client and if he tries to login sign up
    :param Username: username
    :param FirstName: first name
    :param LastName: last name
    :param Password_LineEdit: password
    :param ConfirmPassword_LineEdit: confirmation of the password
    :param ClassName: the name of the class that called it
    :param aes_cipher: the cypher key
    :return: the answer of the server to the connect attempt
    """
    global RegisterOrLogIn
    global UserInformation
    if ClassName == "Register":
        if ConfirmPassword_LineEdit.text() != Password_LineEdit.text():
            return "The password and the password conformation do not match"
        else:
            RegisterOrLogIn = "1"
            UserInformation = {"Username": Username.text(), "Password": Password_LineEdit.text(), "FirstName": FirstName.text(), "LastName": LastName.text()}
            send_data_encrypt(client_socket, RegisterOrLogIn, 1, "", aes_cipher)
            data = UserInformation
            send_data_encrypt(client_socket, data, 1, "", aes_cipher)
            data_recv = recv_msg_encrypt(client_socket, aes_cipher)
            print(data_recv["msg"])
            return data_recv["msg"]
    elif ClassName == "LogIn":
        RegisterOrLogIn = "2"
        UserInformation = {"Username": Username.text(), "Password": Password_LineEdit.text()}
        # send_data_encrypt(client_socket, "hello world", 1, "", aes_cipher)
        send_data_encrypt(client_socket, RegisterOrLogIn, 1, "", aes_cipher)
        data = UserInformation
        send_data_encrypt(client_socket, data, 1, "", aes_cipher)
        # data_recv = recv_msg(client_socket)
        data_recv = recv_msg_encrypt(client_socket, aes_cipher)
        print("hej 4")
        files = recv_msg_encrypt(client_socket, aes_cipher)["msg"]
        print("hej 5")
        print(data_recv["msg"])
        return data_recv["msg"], files


def send_data(conn, data, operation, file_to_send):
    """
    sends the data
    :param conn: client socket
    :param data: the data to send
    :param operation: the type of operation(file or string)
    :param file_to_send: file path
    :return:
    """
    if operation == 1:
        print(data)
        data = protocol.create_string_header(data)
        length = len(data)
        print(length)
        print(data)
        packed_length = struct.pack('>I', length)
        print(packed_length)
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


def send_data_encrypt(conn, data, operation, file_to_send, aes_cipher):
    """
    sends the data to the server but encrypted
    :param conn: client socket
    :param data: the data
    :param operation: the type of operation(file or string)
    :param file_to_send: file path
    :param aes_cipher: the cypher key
    :return:
    """
    try:
        if operation == 1:
            data = protocol.create_string_header(data)
            print(data)
            data = aes_cipher.encrypt(data)
            length = len(data)
            print(length)
            packed_length = struct.pack('>I', length)
            print(packed_length)

            # Send the packed length over the socket
            conn.sendall(packed_length)
            conn.sendall(data)
        elif operation == 2:
            # print(os.path.getsize(file_to_send))
            data = protocol.create_file_header(data, file_to_send)
            # print(data)
            data = aes_cipher.encrypt(data)
            length = len(data)
            # print(length)
            packed_length = struct.pack('>I', length)
            # Send the packed length over the socket
            # print(packed_length)
            conn.sendall(packed_length)
            conn.sendall(data)
            # data = UserInformation
    except Exception as e:
        print(e)


def recv_msg(conn):
    """
    receives data
    :param conn: client socket
    :return: the data
    """
    data_size = protocol.recvall(conn, 4)
    length = struct.unpack('>I', data_size)[0]
    data_recv = protocol.recvall(conn, length)
    data_recv = protocol.parse_header(data_recv)
    return data_recv


def recv_msg_encrypt(conn, aes_cipher):
    """
    receives encrypted data and decrypts it
    :param conn: client socket
    :param aes_cipher: the cypher key
    :return: the data
    """
    try:
        data_size = protocol.recvall(conn, 4)
        length = struct.unpack('>I', data_size)[0]
        print(length)
        data_recv = protocol.recvall(conn, length)
        data_recv = aes_cipher.decrypt(data_recv)
        print(data_recv)
        #   lengthdict = len(protocol.parse_header(data_recv))
        data_recv = protocol.parse_header(data_recv)
        print(data_recv)
        return data_recv
    except Exception as e:
        print(e)


def first_connection():
    """
    receives the public key from the server and creates and sends the iv and aes key
    :return: the cypher key
    """
    encryption_key = get_random_bytes(32)
    iv = get_random_bytes(16)

    aes_cipher = protocol.AESCipher(encryption_key, iv)
    print(f"Decrypted aes key: {encryption_key}")
    print(f"Decrypted iv: {iv}")
    keys_dict = recv_msg(client_socket)
    public_key = keys_dict["msg"]["key"]
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))

    encrypted_aes_key = cipher.encrypt(encryption_key)
    encrypted_iv = cipher.encrypt(iv)

    keys_response_dict = {"aes_key": encrypted_aes_key, "iv": encrypted_iv}
    send_data(client_socket, keys_response_dict, 1, "")
    return aes_cipher


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
    """
    starts the first window
    :return:
    """
    global LogInOrRegister
    aes_cipher = first_connection()
    print(aes_cipher.iv)
    print(aes_cipher.key)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    LogInOrRegisterui = LogInOrRegister
    LogInOrRegisterui.setupUi(MainWindow, ShowRegister, ShowLogIn, send_exit, aes_cipher)
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
