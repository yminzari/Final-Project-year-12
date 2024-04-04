import socket
import os


def send_file(filename, save_as_filename):
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        # Send original filename and desired filename to the server
        client_socket.send(filename.encode())
        client_socket.send(save_as_filename.encode())

        # Send file content
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        print(f"File sent successfully to the server with desired filename: {save_as_filename}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    file_to_send = "C:\\Users\\yminz\\Downloads\\test_scan1.jpg"

    # Specify the desired filename for saving on the server
    save_as_filename = input("Enter the desired filename to save on the server: ")

    send_file(file_to_send, save_as_filename)
