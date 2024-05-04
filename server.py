import socket
import struct
import threading
import docx
import protocol
from threading import *
import oracledb
import hashlib
import os
import fitz
import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


socket_to_username = {}
socket_to_user_id = {}

# If download path does not exist in the clint create the folder and download there Done
# on Login screen display the right error. For example is password is wrong. Display "Wrong password" Done
# NICE TO HAVE: The option of reset password
# when wanting to save a file use f"{save_dirct}\\{username}" as it is the folder for each user
# Deal with keyword search Done
# Deal with owner sort
# Check the option of another owner with his own files
# Create the admin screens
# Fix the custom date range to display the dates and to allow redefine of it Done
# Create a function for error massages Done
# Add pdf and excel files Done
# Add rsa and aes to the server and client


def handle_client(conn, client_address):
    global function_name
    function_name = "handle_client"
    connectiondb = oracledb.connect(user="INFO_MANAGE", password="Henry123", host="localhost", port=1521,
                                    service_name="xepdb1")
    cursor = connectiondb.cursor()
    aes_cipher = first_connection(conn)
    error_msg = ""
    cursor.execute('select 1 from dual')
    is_ok = False
    while is_ok is False:
        data = recv_msg(conn)
        print(data.get("msg"))
        if data.get("msg") == "error" or data.get("msg") == "exit":
            print("exiting")
            return
        if "1" in data.get("msg"):
            is_ok, error_msgs = handle_register(conn, cursor, connectiondb, aes_cipher)
            if is_ok:
                send_data(conn, "connection succeed", 1, "")
            else:
                send_data(conn, error_msg, 1, "")
        elif "2" in data.get("msg"):
            is_ok, error_msg, files = handle_login(conn, cursor, connectiondb, aes_cipher)
            if is_ok:
                send_data(conn, "connection succeed", 1, "")
                send_data(conn, files, 1, "")
            else:
                send_data(conn, error_msg, 1, "")
                send_data(conn, files, 1, "")
        else:
            send_data(conn, "didn't enter log in or register", 1, "")
    while True:
        print(socket_to_username)
        data = recv_msg(conn)
        print(data.get("msg"))
        if data.get("msg") == "error" or data.get("msg") == "exit":
            try:
                socket_to_username.pop(conn)
                socket_to_user_id.pop(conn)
            except Exception as e:
                print(e)
            cursor.close()
            connectiondb.close()
            return
        # saves the file to dir written need to add the db
        elif data.get("operation") == "2":
            handle_files(conn, data, cursor, connectiondb, aes_cipher)
        # need to add dealing with the different req
        elif data.get("operation") == "1":
            try:
                if data["msg"]["req"] == "download":
                    file_path = data["msg"]["file_path"]
                    with open(file_path, "rb") as data:
                        print(data)
                        file = data.read()
                    send_data(conn, file, 2, file_path)
                elif data["msg"]["req"] == "update":
                    print(data["msg"]["req"])
                    update_file(conn, cursor, connectiondb, aes_cipher)
                elif data["msg"]["req"] == "ext_query":
                    send_files_by_criteria(data["msg"]["ext_query"], cursor, conn, aes_cipher)
            except Exception as e:
                e = str(e)
                print(e)
                send_data(conn, e, 1, "")


def first_connection(client_socket):
    key = RSA.generate(2048)
    public_key = key.public_key().export_key()
    private_key = key.export_key()

    keys_dict = {"key": public_key}
    send_data(client_socket, keys_dict, 1, "")
    keys_response_dict = recv_msg(client_socket)["msg"]
    encrypted_aes_key = keys_response_dict.get("aes_key")
    encrypted_iv = keys_response_dict.get("iv")

    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    aes_key = cipher.decrypt(encrypted_aes_key)
    iv = cipher.decrypt(encrypted_iv)

    print(f"Decrypted aes key: {aes_key}")
    print(f"Decrypted iv: {iv}")
    aes_cipher = protocol.AESCipher(aes_key, iv)
    return aes_cipher


def update_file(conn, cursor, connectiondb, aes_cipher):
    file_msg = recv_msg(conn)
    print(file_msg["file_path"])
    try:
        file_path_dict = file_msg.get("file_path").split("/")
        with open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1], 'wb') as file:
            content = ""
            file.write(file_msg.get("msg"))
        if file_path_dict[-1].split(".")[-1] == "txt":
            with open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1], encoding='UTF-8') as file_ext:
                if os.path.exists(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1]):
                    content = file_ext.read()
                    print("File exists!")
                else:
                    print("File does not exist.")
        elif file_path_dict[-1].split(".")[-1] == "docx":
            content = getText(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1])
        elif file_path_dict[-1].split(".")[-1] == "pdf":
            doc = fitz.open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1])
            for page in doc:
                content += page.get_text()
            doc.close()
        print(content)
        cursor.execute("""UPDATE FILE_LIST_TBL
                        SET FILE_TEXT = :content
                        ,DATE_UPDATE = SYSDATE
                        ,UPDATE_BY = :update_by
                        WHERE FILE_PATH = :file_path """, content=content, file_path=(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1]), update_by=socket_to_user_id.get(conn))
        connectiondb.commit()
        cursor.execute("""SELECT FL.FILE_PATH,to_char(FL.DATE_CREATE,'dd/mm/yyyy hh24:mi'),UT.USER_NAME from info_manage.file_list_tbl fl,
                                                    info_manage.USERS_TBL UT
                                                    where fl.create_by = ut.user_id AND FL.CREATE_BY = :user_id""",
                       (socket_to_user_id.get(conn),))
        files = cursor.fetchall()
        send_data(conn, "Updated", 1, "")
        send_data(conn, files, 1, "")

    except Exception as e:
        print(e)
        send_data(conn, str(e), 1, "")
        send_data(conn, str(e), 1, "")


def handle_files(conn, data, cursor, connectiondb, aes_cipher):
    try:
        file_path_dict = data.get("file_path").split("/")
        print(file_path_dict[-1])
        cursor.execute("SELECT COUNT(*) FROM FILE_LIST_TBL WHERE FILE_PATH = :file_path", (save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1],))
        result = cursor.fetchone()[0]
        print("result: " + str(result))
        if result > 0:
            send_data(conn, "file already exists", 1, "")
            send_data(conn, "", 1, "")
            return
        with open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1], 'wb') as file:
            content = ""
            file.write(data.get("msg"))
            # need to fix, so it sends a response that it recived it
            cursor.execute(f"""INSERT INTO FILE_LIST_TBL(FILE_PATH,FILE_TYPE,CREATE_BY,UPDATE_BY)
                            VALUES(:file_path,:file_type,:create_by,:update_by)"""
                           , ((save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1]), file_path_dict[-1].split(".")[-1], socket_to_user_id.get(conn), socket_to_user_id.get(conn)))
            connectiondb.commit()
            cursor.execute("""SELECT FL.FILE_PATH,to_char(FL.DATE_CREATE,'dd/mm/yyyy hh24:mi'),UT.USER_NAME from info_manage.file_list_tbl fl,
                                            info_manage.USERS_TBL UT
                                            where fl.create_by = ut.user_id AND FL.CREATE_BY = :user_id""", (socket_to_user_id.get(conn),))
            files = cursor.fetchall()
        if file_path_dict[-1].split(".")[-1] == "txt":
            with open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1], encoding='UTF-8') as file_ext:
                if os.path.exists(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1]):
                    content = file_ext.read()
                    print("File exists!")
                else:
                    print("File does not exist.")
        elif file_path_dict[-1].split(".")[-1] == "docx":
            content = getText(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1])
        elif file_path_dict[-1].split(".")[-1] == "pdf":
            doc = fitz.open(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1])

            for page in doc:
                content += page.get_text()
            doc.close()
        elif file_path_dict[-1].split(".")[-1] == "xlsx":
            content = getExcelText(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1])
        print(content)
        # sql error
        cursor.execute(""" UPDATE FILE_LIST_TBL
                        SET FILE_TEXT = :content
                        WHERE FILE_PATH = :file_path """, content=content, file_path=(save_dirct + "/" + socket_to_username.get(conn) + "/" + file_path_dict[-1]))
        connectiondb.commit()
        send_data(conn, "Saved File", 1, "")
        send_data(conn, files, 1, "")
    except Exception as e:
        send_data(conn, str(e), 1, "")
        send_data(conn, str(e), 1, "")
        print(e)


def send_files_by_criteria(criteria, cursor, conn, aes_cipher):
    try:
        query = f"""SELECT FL.FILE_PATH,to_char(FL.DATE_CREATE,'dd/mm/yyyy hh24:mi'),UT.USER_NAME from info_manage.file_list_tbl fl,
                                                info_manage.USERS_TBL UT
                                                where fl.create_by = ut.user_id AND FL.CREATE_BY = :user_id
                                                {criteria}"""
        print(query)
        cursor.execute(query, (socket_to_user_id.get(conn),))
        files = cursor.fetchall()
        print(files)
        send_data(conn, files, 1, "")
    except Exception as e:
        print(e)




def recv_msg_encrypt(conn, aes_cipher):
    global function_name
    function_name = "recv_msg_encrypt"
    try:
        data_size = protocol.recvall(conn, 4)
        data_size = aes_cipher.decrypt(data_size)
        print(data_size)
        length = struct.unpack('>I', data_size)[0]
        data_recv = protocol.recvall(conn, length)
        print(data_recv)
        data_recv = aes_cipher.decrypt(data_recv)
        #   lengthdict = len(protocol.parse_header(data_recv))
        data_recv = protocol.parse_header(data_recv)
        return data_recv
    except Exception as e:
        print(f"failed at {function_name} {e}")
        return {"msg": "error"}



def recv_msg(conn):
    global function_name
    function_name = "recv_msg"
    try:
        data_size = protocol.recvall(conn, 4)
        print(data_size)
        length = struct.unpack('>I', data_size)[0]
        data_recv = protocol.recvall(conn, length)
        print(data_recv)
        #   lengthdict = len(protocol.parse_header(data_recv))
        data_recv = protocol.parse_header(data_recv)
        return data_recv
    except Exception as e:
        print(f"failed at {function_name} {e}")
        return {"msg": "error"}
#    match data_recv["operation"]:
#        case 2:
#            return recv_file(data_recv)
#        case 1:
#            return recv_req(data_recv)
#        case _:
#            pass

    # need to add the recv


# need to check if client does not already exist and username and password are ok if everything is good then return username True
def handle_register(conn, cursor, connectiondb, aes_cipher):
    global function_name
    global socket_to_username
    global socket_to_user_id
    function_name = "handle_register"
    UserInformation = recv_msg(conn).get("msg")
    username = UserInformation.get("Username")
    print("username: " + username)
    password = UserInformation.get("Password")
    salt = os.urandom(32)
    hashed_pass = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    print(password)
    print(hashed_pass)
    firstName = UserInformation.get("FirstName")
    lastName = UserInformation.get("LastName")
    if not is_valid_username(username):
        if not is_valid_password(password):
            return False, "Invalid password and username"
        return False, "Invalid username"
    if not is_valid_password(password):
        return False, "Invalid password"
    cursor.execute("SELECT COUNT(*) FROM USERS_TBL WHERE USER_NAME = :username", (username, ))
    result = cursor.fetchone()[0]
    print("result: " + str(result))
    if result > 0:
        return False, "username already exists in the system"
    try:
        user_id = ""
        cursor.execute(f"""INSERT INTO USERS_TBL(USER_NAME,PASSWORD,UPDATE_BY,COMMENTS,USER_STATUS,IS_ADMIN,PASSWORD_EXT,FIRST_NAME,LAST_NAME)
        VALUES(:username,:password,:username,'Standard user','OPEN',0,:password_ext,:first_name,:last_name)""", (username, hashed_pass, username, salt, firstName, lastName))
        connectiondb.commit()
        cursor.execute(f"""SELECT USER_ID FROM USERS_TBL WHERE USER_NAME = :username""", (username, ))
        user_id = cursor.fetchone()[0]
        print(user_id)
        if os.path.exists(f"{save_dirct}\\{username}"):
            print("folder already exist")
        else:
            os.mkdir(f"{save_dirct}\\{username}")
        socket_to_username[conn] = username
        socket_to_user_id[conn] = user_id
        return True, ""
    except oracledb.Error as error:
        print(f"failed at {function_name} {error}")
        return False, error


# need to check if client is in the db
def handle_login(conn, cursor, connectiondb, aes_cipher):
    global function_name
    global socket_to_username
    global socket_to_user_id
    function_name = "handle_login"
    username_and_password = recv_msg(conn).get("msg")
    print(username_and_password)
    username = username_and_password.get("Username")
    password = username_and_password.get("Password")
    # select password,nvl(to_char(password_ext),'EMPTY') salt, user_id , 1 as is_exists
    # from info_manage.users_tbl where user_name = 'test'
    cursor.execute("""select password,password_ext salt, user_id , 1 as is_exists
from info_manage.users_tbl where user_name = :username""", (username, ))
    user_info = cursor.fetchone()
    print(user_info)
    print(type(user_info))
    # -- If user does not exist
    if user_info is None:
        return False, "user does not exist in the system", []
    # cursor.execute("SELECT PASSWORD_EXT FROM USERS_TBL WHERE USER_NAME = :username", (username, ))
    # salt_result = cursor.fetchone()
    # -- If salt does not exist
    if user_info[1] is None:
        try:
            # cursor.execute("SELECT COUNT(*) FROM USERS_TBL WHERE USER_NAME = :username AND PASSWORD = :password",
            #               (username, password))
            # result = cursor.fetchone()[0]
            # cursor.execute(f"SELECT USER_ID FROM USERS_TBL WHERE USER_NAME = :username", (username,))
            # user_id = cursor.fetchone()[0]
            # if result == 0:
            #    return False, "Inputted incorrect password", []
            # -- If password does not match the username
            if user_info[0] != password:
                return False, "Invalid password", []
            else:
                socket_to_username[conn] = username
                socket_to_user_id[conn] = user_info[2]
                cursor.execute("""SELECT FL.FILE_PATH,to_char(FL.DATE_CREATE,'dd/mm/yyyy hh24:mi'),UT.USER_NAME from info_manage.file_list_tbl fl,
                                                info_manage.USERS_TBL UT
                                                where fl.create_by = ut.user_id AND FL.CREATE_BY = :user_id""",
                               (user_info[2],))
                files = cursor.fetchall()
                print(cursor.fetchall())
                return True, "", files
        except oracledb.Error as error:
            error = str(error)
            print(f"failed at {function_name} {error}")
            return False, error, []
    # -- If salt does exist
    else:
        try:
            salt = user_info[1].read()
            print(salt)
            hashed_pass = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            print(hashed_pass.hex())
            # cursor.execute("SELECT COUNT(*) FROM USERS_TBL WHERE USER_NAME = :username AND PASSWORD = :password",
            #                (username, hashed_pass))
            # result = cursor.fetchone()[0]
            # cursor.execute(f"SELECT USER_ID FROM USERS_TBL WHERE USER_NAME = :username", (username,))
            # user_id = cursor.fetchone()[0]
            # if result == 0:
            #     return False, "user does not exist in the system", []
            if hashed_pass.hex().upper() != user_info[0]:
                return False, "Invalid password", []
            else:
                socket_to_username[conn] = username
                socket_to_user_id[conn] = user_info[2]
                cursor.execute("""SELECT FL.FILE_PATH,to_char(FL.DATE_CREATE,'dd/mm/yyyy hh24:mi'),UT.USER_NAME from info_manage.file_list_tbl fl,
                                                info_manage.USERS_TBL UT
                                                where fl.create_by = ut.user_id AND FL.CREATE_BY = :user_id""",
                               (user_info[2],))
                files = cursor.fetchall()
                print(cursor.fetchall())
                print("hej")
                return True, "", files
        except oracledb.Error as error:
            error = str(error)
            print(f"failed at {function_name} {error}")
            return False, error, []



# def recv_file(data_recv):
#    return data_recv["msg"], data_recv["operation"], data_recv["file_path"]


# def recv_req(data_recv):
#    return data_recv["msg"], data_recv["operation"]


def send_data(conn, data, operation, file_to_send):
    global function_name
    function_name = "send_data"
    try:
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
    except Exception as e:
        print(f"failed at {function_name} {e}")


def send_data_encrypt(conn, data, operation, file_to_send, aes_cipher):
    global function_name
    function_name = "send_data"
    try:
        if operation == 1:
            data = protocol.create_string_header(data)
            length = len(data)
            packed_length = struct.pack('>I', length)
            packed_length = aes_cipher.encrypt(packed_length)
            data = aes_cipher.encrypt(data)
            # Send the packed length over the socket
            conn.sendall(packed_length)
            conn.sendall(data)
        elif operation == 2:
            data = protocol.create_file_header(data, file_to_send)
            length = len(data)
            packed_length = struct.pack('>I', length)
            packed_length = aes_cipher.encrypt(packed_length)
            data = aes_cipher.encrypt(data)
            # Send the packed length over the socket
            conn.sendall(packed_length)
            conn.sendall(data)
    except Exception as e:
        print(f"failed at {function_name} {e}")


def is_valid_password(password):
    # Check if password has at least 6 characters and a number
    global function_name
    function_name = "is_valid_password"
    try:
        if len(password) < 6:
            return False
        has_number = any(char.isdigit() for char in password)
        has_special_char = any(not c.isalnum() for c in password)
        return has_number and has_special_char
    except Exception as e:
        print(f"failed at: {function_name} {e}")
        return False


def is_valid_username(username):
    # Check if password has at least 6 characters and a number
    global function_name
    function_name = "is_valid_username"
    try:
        if len(username) < 5:
            return False
        return True
    except Exception as e:
        print(f"failed at: {function_name} {e}")
        return False


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def getExcelText(filename):
    # Read the Excel file into a DataFrame
    excel_file = filename # Replace with your Excel file path
    df = pd.read_excel(excel_file)

    # Initialize an empty list to store text
    all_text = []

    # Iterate through each cell in the DataFrame
    for column in df.columns:
        for cell in df[column]:
            # Check if the cell contains text
            if isinstance(cell, str):
                all_text.append(cell)

    # Join all the extracted text into a single string
    all_text_combined = '\n'.join(all_text)
    return all_text_combined


save_dirct = "D:/Yonatan/INPUT_FILES_FOR_PROCESS"
function_name = ""


def main():
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        conn, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, client_address))
        thread.start()


if __name__ == "__main__":
    main()