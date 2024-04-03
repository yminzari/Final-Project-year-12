import socket
import struct
import threading
import protocol
from threading import *
import oracledb


# need to deal with log in and register
# need to fix send_data right now I can add a user to the database
def handle_client(conn, client_address):
    connectiondb = oracledb.connect(user="INFO_MANAGE", password="Henry123", host="localhost", port=1521,
                                    service_name="xepdb1")
    cursor = connectiondb.cursor()
    error_msg = ""
    cursor.execute('select 1 from dual')
    data = recv_msg(conn)
    print(data["msg"])
    if data["msg"] == "error":
        return
    is_ok = False
    if "1" in data["msg"]:
        is_ok, error_msg = handle_register(conn, cursor, connectiondb)
    elif "2" in data["msg"]:
        is_ok, error_msg = handle_login(conn, cursor, connectiondb)
    else:
        send_data(conn, "didn't enter log in or register", 1, "")
    if is_ok is False:
        cursor.close()
        connectiondb.close()
        send_data(conn, error_msg, 1, "")
        return
    else:
        send_data(conn, "connection succeed", 1, "")
    while True:
        data = recv_msg(conn)
        if data["msg"] == "error" or data["msg"] == "exit":
            cursor.close()
            connectiondb.close()
            return
        # saves the file to dir written need to add the db
        elif data["operation"] == "2":
            print("eeeee")
            file_path_dict = data["file_path"].split("\\")
            with open(save_dirct + "\\" + file_path_dict[-1], 'wb') as file:
                file.write(data["msg"])
        # need to add dealing with the different req
        elif data["operation"] == "1":
            send_data(conn, data["msg"], 1, "")


def recv_msg(conn):
    try:
        data_size = protocol.recvall(conn, 4)
        length = struct.unpack('>I', data_size)[0]
        data_recv = protocol.recvall(conn, length)
        #   lengthdict = len(protocol.parse_header(data_recv))
        data_recv = protocol.parse_header(data_recv)
        return data_recv
    except Exception as e:
        print("client connection was forcibly closed")
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
def handle_register(conn, cursor, connectiondb):
    username_and_password = recv_msg(conn)["msg"]
    username_and_password = username_and_password.split("|")
    username = username_and_password[0]
    print("username: " + username)
    password = username_and_password[1]
    if is_valid_password(password):
        return False, "Invalid password"
    cursor.execute("SELECT COUNT(*) FROM USERS_TBL WHERE USER_NAME = :username", (username, ))
    result = cursor.fetchone()[0]
    print("result: " + str(result))
    if result > 0:
        return False, "username already exists in the system"
    try:
        cursor.execute(f"""INSERT INTO USERS_TBL(USER_NAME,PASSWORD,UPDATE_BY,COMMENTS,USER_STATUS,IS_ADMIN)
        VALUES(:username,:password,:username,'Standard user','OPEN',0)""", (username, password, username))
        connectiondb.commit()
        return True, ""
    except oracledb.Error as error:
        print(error)
        return False, error


# need to check if client is in the db
def handle_login(conn, cursor, connectiondb):
    username_and_password = recv_msg(conn)["msg"]
    username_and_password = username_and_password.split("|")
    username = username_and_password[0]
    password = username_and_password[1]
    cursor.execute("SELECT COUNT(*) FROM USERS_TBL WHERE USER_NAME = :username AND PASSWORD = :password", (username, password))
    result = cursor.fetchone()[0]
    if result == 0:
        return False, "user does not exist in the system"
    else:
        return True, ""


# def recv_file(data_recv):
#    return data_recv["msg"], data_recv["operation"], data_recv["file_path"]


# def recv_req(data_recv):
#    return data_recv["msg"], data_recv["operation"]


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


def is_valid_password(password):
    # Check if password has at least 6 characters and a number
    if len(password) < 6:
        return False
    has_number = any(char.isdigit() for char in password)
    return has_number


save_dirct = "D:\\Yonatan\\INPUT_FILES_FOR_PROCESS"


def main():
    host = '127.0.0.1'
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
