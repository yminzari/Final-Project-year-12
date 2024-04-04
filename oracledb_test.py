import oracledb
import socket
import os
#DATA SOURCE=XEPDB1;TNS_ADMIN=C:\app\yminz\product\21c\homes\OraDB21Home1\network\admin;USER ID=INFO_MANAGE
def receive_file(connection, save_as_filename, save_directory):
    file_path = os.path.join(save_directory, save_as_filename)
    with open(file_path, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            file.write(data)


def main():
    connectiondb = oracledb.connect(user="INFO_MANAGE", password="Henry123", host="localhost", port=1521,
                            service_name="xepdb1")
    cursor = connectiondb.cursor()
    cursor.execute('select 1 from dual')
    for row in cursor:
        print(row)
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

# Specify the target directory to save files
    save_directory = "D:\\Yonatan\\INPUT_FILES_FOR_PROCESS"

    while not os.path.exists(save_directory):
        print(f"The directory '{save_directory}' does not exist.")
        save_directory = input("Enter a valid target directory to save files: ")

    print(f"Files will be saved in: {save_directory}")

    while True:
        connection, address = server_socket.accept()
        print(f"Accepted connection from {address}")

        try:
            # Receive filenames from the client
            original_filename = connection.recv(1024).decode()
            save_as_filename = connection.recv(1024).decode() #error here

            print(f"Receiving file with original filename: {original_filename}")

            # Receive file content and save with the desired filename in the specified directory
            receive_file(connection, save_as_filename, save_directory)

            print(f"File received successfully and saved as: {os.path.join(save_directory, save_as_filename)}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            connection.close()
            cursor.close()
            connectiondb.close()


if __name__ == "__main__":
    main()
