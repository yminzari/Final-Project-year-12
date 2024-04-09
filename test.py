import os
import socket
import struct
import protocol
import PyQ5_windows
from PyQt5 import QtWidgets
import sys


host = '127.0.0.1'
port = 12345
FileWindow = PyQ5_windows.Ui_file_window()


def main():
    # os.mkdir(f"D:\\Yonatan\\INPUT_FILES_FOR_PROCESS\\test")
    app = QtWidgets.QApplication(sys.argv)
    file_window = QtWidgets.QMainWindow()
    FileWindow_ui = PyQ5_windows.Ui_file_window_ver2()
    FileWindow_ui.setupUi_file_window(file_window)
    PyQ5_windows.Ui_file_window_ver2.add_file_to_list(FileWindow_ui, ["test.txt", "4/9/2024", "yminzari"])
    file_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
