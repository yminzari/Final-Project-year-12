import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QFileDialog, QLabel, QCalendarWidget, QTableWidgetItem, \
    QMenu, QAction
from PyQt5.QtCore import QDate

# need in the file window deal with all the sorts obviously deal with the listing of the files as well
class Ui_LogInOrRegister(object):

    def OpenLogInWindow(self, MainWindow, CallBackShowLogIn):
        CallBackShowLogIn(MainWindow)

    def OpenRegistrtWindow(self, MainWindow, CallBackShowRegister):
        CallBackShowRegister(MainWindow)

    def setupUi(self, MainWindow, CallBackShowRegister, CallBackShowLogIn):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 609)
        MainWindow.setStyleSheet("background-color: rgb(236, 243, 244);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogInButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.OpenLogInWindow(MainWindow, CallBackShowLogIn))
        self.LogInButton.setGeometry(QtCore.QRect(280, 300, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LogInButton.setFont(font)
        self.LogInButton.setStyleSheet("QPushButton{\n"
"background-color: #43BEF7;\n"
"border-radius: 15px;\n"
"border-bottom: 2px solid;\n"
"border-right: 2px solid;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #4385F7;\n"
"}")
        self.LogInButton.setObjectName("pushButton_2")
        self.RegisterButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.OpenRegistrtWindow(MainWindow, CallBackShowRegister))
        self.RegisterButton.setGeometry(QtCore.QRect(280, 180, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RegisterButton.setFont(font)
        self.RegisterButton.setStyleSheet("QPushButton{\n"
"background-color: #43BEF7;\n"
"border-radius: 15px;\n"
"border-bottom: 2px solid;\n"
"border-right: 2px solid;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #4385F7;\n"
"}")
        self.RegisterButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 80, 571, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "logInOrRegister"))
        self.LogInButton.setText(_translate("MainWindow", "Log In"))
        self.RegisterButton.setText(_translate("MainWindow", "Register"))
        self.label.setText(_translate("MainWindow", "Välkommen till python-projekt"))


class Ui_LogInWindow(object):
    def call_Enter(self, EnterCallBack, CallBackFileWindow, MainWindow):
        self.result, files = EnterCallBack(self.Username, "", "", self.Password_LineEdit, "", "LogIn")
        if self.result != "connection succeed":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Bomboclat")
            msg_box.setText(self.result)
            msg_box.exec_()
        else:
            CallBackFileWindow(MainWindow, files)

    def OpenRegistrtWindow(self, MainWindow, CallBackShowRegister):
        CallBackShowRegister(MainWindow)

    def setupUi(self, MainWindow, EnterCallBack, CallBackShowRegister, CallBackFileWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 90, 371, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.result = ""
        self.Enter = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.call_Enter(EnterCallBack, CallBackFileWindow, MainWindow))
        self.Enter.setGeometry(QtCore.QRect(260, 430, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Enter.setFont(font)
        self.Enter.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(85, 85, 255);\n"
"}")
        self.Enter.setObjectName("pushButton")
        # Currently takes you back to the window when you pick either LogIn or Register
        self.SwitchToRegister = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.OpenRegistrtWindow(MainWindow, CallBackShowRegister))
        self.SwitchToRegister.setGeometry(QtCore.QRect(260, 490, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SwitchToRegister.setFont(font)
        self.SwitchToRegister.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(85, 85, 255);\n"
"}")
        self.SwitchToRegister.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(200, 180, 331, 251))
        self.groupBox.setObjectName("groupBox")
        self.Password_LineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.Password_LineEdit.setGeometry(QtCore.QRect(20, 160, 261, 31))
        self.Password_LineEdit.setObjectName("lineEdit_2")
        self.Password_LineEdit.setEchoMode(QLineEdit.Password)
        self.toggle_button = QPushButton(self.groupBox, clicked= lambda: self.toggle_visibility())
        self.toggle_button.setGeometry(QtCore.QRect(20, 200, 100, 31))
        self.toggle_button.setText("Show Password")
        self.toggle_button.setStyleSheet("QPushButton{\n"
                                            "    background-color: rgb(85, 170, 255);\n"
                                            "}\n"
                                            "QPushButton:hover{\n"
                                            "    background-color: rgb(85, 85, 255);\n"
                                            "}")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Username = QtWidgets.QLineEdit(self.groupBox)
        self.Username.setGeometry(QtCore.QRect(20, 70, 261, 31))
        self.Username.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 711, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def toggle_visibility(self):
        if self.Password_LineEdit.echoMode() == QLineEdit.Password:
            self.Password_LineEdit.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setText("Hide Password")
        else:
            self.Password_LineEdit.setEchoMode(QLineEdit.Password)
            self.toggle_button.setText("Show Password")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LogIn"))
        self.label.setText(_translate("MainWindow", "Login"))
        self.Enter.setText(_translate("MainWindow", "Enter"))
        self.SwitchToRegister.setText(_translate("MainWindow", "Switch To Register"))
        self.groupBox.setTitle(_translate("MainWindow", "User Inforamtion"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.label_2.setText(_translate("MainWindow", "Username:"))


class Ui_RegisterWindow(object):
    def call_Enter(self, EnterCallBack, CallBackFileWindow, MainWindow):
        self.result = EnterCallBack(self.Username, self.FirstName, self.LastName, self.Password_LineEdit, self.ConfirmPassword_LineEdit, "Register")
        if self.result != "connection succeed":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Bomboclat")
            msg_box.setText(self.result)
            msg_box.exec_()
        else:
            CallBackFileWindow(MainWindow, [])

    def OpenLogInWindow(self, MainWindow, CallBackShowLogIn):
        CallBackShowLogIn(MainWindow)

    def setupUi(self, MainWindow, EnterCallBack, CallBackShowLogIn, CallBackFileWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1099, 845)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 30, 411, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.result = ""
        self.Enter = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.call_Enter(EnterCallBack, CallBackFileWindow, MainWindow))
        self.Enter.setGeometry(QtCore.QRect(470, 660, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Enter.setFont(font)
        self.Enter.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(85, 85, 255);\n"
"}")
        self.Enter.setObjectName("Enter")
        # Currently takes you back to the window when you pick either LogIn or Register
        self.SwitchToLogin = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.OpenLogInWindow(MainWindow, CallBackShowLogIn))
        self.SwitchToLogin.setGeometry(QtCore.QRect(470, 720, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SwitchToLogin.setFont(font)
        self.SwitchToLogin.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(85, 85, 255);\n"
"}")
        self.SwitchToLogin.setObjectName("SwitchToLogin")
        self.PersonalInformation = QtWidgets.QGroupBox(self.centralwidget)
        self.PersonalInformation.setGeometry(QtCore.QRect(440, 120, 271, 271))
        self.PersonalInformation.setObjectName("PersonalInformation")
        self.LastName = QtWidgets.QLineEdit(self.PersonalInformation)
        self.LastName.setGeometry(QtCore.QRect(10, 210, 241, 31))
        self.LastName.setObjectName("LastName")
        self.label_6 = QtWidgets.QLabel(self.PersonalInformation)
        self.label_6.setGeometry(QtCore.QRect(10, 190, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.FirstName = QtWidgets.QLineEdit(self.PersonalInformation)
        self.FirstName.setGeometry(QtCore.QRect(10, 130, 241, 31))
        self.FirstName.setObjectName("FirstName")
        self.label_5 = QtWidgets.QLabel(self.PersonalInformation)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.Username = QtWidgets.QLineEdit(self.PersonalInformation)
        self.Username.setGeometry(QtCore.QRect(10, 50, 241, 31))
        self.Username.setObjectName("Username")
        self.label_2 = QtWidgets.QLabel(self.PersonalInformation)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.Password_box = QtWidgets.QGroupBox(self.centralwidget)
        self.Password_box.setGeometry(QtCore.QRect(440, 400, 271, 231))
        self.Password_box.setObjectName("Password_box")
        self.label_3 = QtWidgets.QLabel(self.Password_box)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Password_LineEdit = QtWidgets.QLineEdit(self.Password_box)
        self.Password_LineEdit.setGeometry(QtCore.QRect(10, 50, 241, 31))
        self.Password_LineEdit.setObjectName("Password_LineEdit")
        self.Password_LineEdit.setEchoMode(QLineEdit.Password)
        self.label_4 = QtWidgets.QLabel(self.Password_box)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.ConfirmPassword_LineEdit = QtWidgets.QLineEdit(self.Password_box)
        self.ConfirmPassword_LineEdit.setGeometry(QtCore.QRect(10, 140, 241, 31))
        self.ConfirmPassword_LineEdit.setObjectName("ConfirmPassword_LineEdit")
        self.ConfirmPassword_LineEdit.setEchoMode(QLineEdit.Password)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(700, 440, 61, 41))
        self.label_7.setMaximumSize(QtCore.QSize(71, 16777215))
        self.label_7.setText("")
        # need to fix later
        self.label_7.setPixmap(QtGui.QPixmap("C:\\Users\\yminz\\Downloads\\icons8-question-30.png"))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(700, 160, 61, 41))
        self.label_8.setMaximumSize(QtCore.QSize(71, 16777215))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("C:\\Users\\yminz\\Downloads\\icons8-question-30.png"))
        self.label_8.setObjectName("label_8")
        # Add toolTips to the labels
        QtWidgets.QToolTip.setFont(QFont('Arial', 8))
        self.label_7.setToolTip('Password must be at least 6 characters and must include a number and a special character')
        self.label_7.resize(self.label_7.sizeHint())
        self.label_7.move(700, 440)
        self.label_8.setToolTip('Username must be longer then 5 characters')
        self.label_8.resize(self.label_8.sizeHint())
        self.label_8.move(700, 160)
        self.toggle_button = QPushButton(self.Password_box, clicked= lambda: self.toggle_visibility())
        self.toggle_button.setGeometry(QtCore.QRect(10, 180, 100, 31))
        self.toggle_button.setText("Show Password")
        self.toggle_button.setStyleSheet("QPushButton{\n"
                                         "    background-color: rgb(85, 170, 255);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "    background-color: rgb(85, 85, 255);\n"
                                         "}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/fugue-icons-3.5.6/icons/question-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon)
        self.actionHelp.setObjectName("actionHelp")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def toggle_visibility(self):
        if self.ConfirmPassword_LineEdit.echoMode() == QLineEdit.Password:
            self.ConfirmPassword_LineEdit.setEchoMode(QLineEdit.Normal)
            self.Password_LineEdit.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setText("Hide Password")
        else:
            self.ConfirmPassword_LineEdit.setEchoMode(QLineEdit.Password)
            self.Password_LineEdit.setEchoMode(QLineEdit.Password)
            self.toggle_button.setText("Show Password")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Register"))
        self.Enter.setText(_translate("MainWindow", "Enter"))
        self.SwitchToLogin.setText(_translate("MainWindow", "Switch To Login"))
        self.PersonalInformation.setTitle(_translate("MainWindow", "Personal Information"))
        self.label_6.setText(_translate("MainWindow", "Last Name:"))
        self.label_5.setText(_translate("MainWindow", "First Name:"))
        self.label_2.setText(_translate("MainWindow", "Username:"))
        self.Password_box.setTitle(_translate("MainWindow", "Password"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.label_4.setText(_translate("MainWindow", "Confirm Password:"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))


class Ui_file_window(object):
    def setupUi_file_window(self, MainWindow, add_file_call_back):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1124, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(10, 150, 1111, 701))
        self.file_list.setObjectName("file_list")
        self.search_file_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_file_line_edit.setGeometry(QtCore.QRect(140, 30, 981, 31))
        self.search_file_line_edit.setObjectName("search_file_line_edit")
        self.search_file_lable = QtWidgets.QLabel(self.centralwidget)
        self.search_file_lable.setGeometry(QtCore.QRect(140, 10, 371, 21))
        self.search_file_lable.setText("Search A File: ")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 10, 371, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.add_file_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_file(add_file_call_back))
        self.add_file_pushButton.setGeometry(QtCore.QRect(0, 30, 131, 31))
        # self.add_file_pushButton.clicked.connect(self.add_file)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/icons8-file-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_file_pushButton.setIcon(icon)
        self.add_file_pushButton.setIconSize(QtCore.QSize(24, 24))
        self.add_file_pushButton.setObjectName("add_file_pushButton")
        self.search_keyword_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_keyword_lineEdit.setGeometry(QtCore.QRect(140, 90, 181, 31))
        self.search_keyword_lineEdit.setObjectName("search_keyword_lineEdit")
        self.search_keyword_lable = QtWidgets.QLabel(self.centralwidget)
        self.search_keyword_lable.setGeometry(QtCore.QRect(140, 70, 371, 21))
        self.search_keyword_lable.setText("Enter Keyword to search: ")
        self.search_keyword_lable.setObjectName("search_keyword_lable")
        self.edited_date_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.edited_date_comboBox.setGeometry(QtCore.QRect(340, 90, 181, 31))
        self.edited_date_comboBox.setCurrentText("")
        self.edited_date_comboBox.setObjectName("edited_date_comboBox")
        self.edited_date_comboBox.addItem("All")
        self.edited_date_comboBox.addItems(["today", "the last seven days", "the last thirty days", "this year", "custom date range"])
        self.file_type_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.file_type_comboBox.setGeometry(QtCore.QRect(540, 90, 191, 31))
        self.file_type_comboBox.setObjectName("file_type_comboBox")
        self.file_type_comboBox.addItem("All")
        self.file_type_comboBox.addItems(["txt", "docx"])
        self.owner_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.owner_comboBox.setGeometry(QtCore.QRect(750, 90, 191, 31))
        self.owner_comboBox.setObjectName("owner_comboBox")
        self.owner_comboBox.addItem("All")
        self.edit_date_label = QtWidgets.QLabel(self.centralwidget)
        self.edit_date_label.setGeometry(QtCore.QRect(340, 70, 171, 16))
        self.edit_date_label.setObjectName("edit_date_label")
        self.file_type_label = QtWidgets.QLabel(self.centralwidget)
        self.file_type_label.setGeometry(QtCore.QRect(540, 70, 171, 16))
        self.file_type_label.setObjectName("file_type_label")
        self.owner_label = QtWidgets.QLabel(self.centralwidget)
        self.owner_label.setGeometry(QtCore.QRect(750, 70, 171, 16))
        self.owner_label.setObjectName("owner_label")
        self.edited_date_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.edited_date_comboBox.setGeometry(QtCore.QRect(340, 90, 181, 31))
        self.edited_date_comboBox.setCurrentText("")
        self.edited_date_comboBox.setObjectName("edited_date_comboBox")
        self.edited_date_comboBox.addItem("All")
        self.edited_date_comboBox.addItems(
            ["today", "the last seven days", "the last thirty days", "this year", "custom date range"])
        self.edited_date_comboBox.currentIndexChanged.connect(self.handle_date_range_selection)
        self.custom_date_range_widget = None  # Initialize the custom date range widget
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def handle_date_range_selection(self, index):
        if self.edited_date_comboBox.currentText() == "custom date range":
            if self.custom_date_range_widget is None:
                self.custom_date_range_widget = self.create_custom_date_range_widget()
            self.custom_date_range_widget.show()
        else:
            if self.custom_date_range_widget is not None:
                self.custom_date_range_widget.hide()

    def create_custom_date_range_widget(self):
        # Create a new widget for the custom date range selection
        custom_date_range_widget = QtWidgets.QWidget(self.centralwidget)
        custom_date_range_widget.setGeometry(QtCore.QRect(340, 150, 400, 200))
        custom_date_range_widget.setWindowTitle("Select Custom Date Range")

        # Create a layout for the custom date range widget
        layout = QtWidgets.QVBoxLayout(custom_date_range_widget)

        # Create a layout for the start and end date selection
        date_range_layout = QtWidgets.QHBoxLayout()

        # Create the start date selection
        start_date_label = QtWidgets.QLabel("Start Date:")
        self.start_date_edit = QtWidgets.QDateEdit(custom_date_range_widget)
        self.start_date_edit.setCalendarPopup(True)
        date_range_layout.addWidget(start_date_label)
        date_range_layout.addWidget(self.start_date_edit)

        # Create the end date selection
        end_date_label = QtWidgets.QLabel("End Date:")
        self.end_date_edit = QtWidgets.QDateEdit(custom_date_range_widget)
        self.end_date_edit.setCalendarPopup(True)
        date_range_layout.addWidget(end_date_label)
        date_range_layout.addWidget(self.end_date_edit)

        layout.addLayout(date_range_layout)

        # Create buttons to confirm and cancel the selection
        button_layout = QtWidgets.QHBoxLayout()
        confirm_button = QtWidgets.QPushButton("Confirm")
        cancel_button = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Connect the confirm and cancel buttons to appropriate functions
        confirm_button.clicked.connect(lambda: self.handle_custom_date_range_confirmation(self.start_date_edit, self.end_date_edit))
        cancel_button.clicked.connect(custom_date_range_widget.hide)

        return custom_date_range_widget

    def handle_custom_date_range_confirmation(self, start_date_edit, end_date_edit):
        # Get the selected start and end dates from the date edit widgets
        start_date = start_date_edit.date()
        end_date = end_date_edit.date()

        # Do something with the selected date range, e.g., update the UI or perform a search
        print(f"Selected date range: {start_date.toString()} - {end_date.toString()}")

        # Hide the custom date range widget
        self.custom_date_range_widget.hide()

    def add_file(self, add_file_call_back):
        self.file_name, answer = add_file_call_back()
        if answer != "Saved File":
            return
        self.add_file_to_list(self.file_name)

    def add_file_to_list(self, file):
        self.file_list.addItem(file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "file_window"))
        self.search_file_line_edit.setText(_translate("MainWindow", ""))
        self.add_file_pushButton.setText(_translate("MainWindow", "Add File"))
        self.search_keyword_lineEdit.setText(_translate("MainWindow", ""))
        self.edit_date_label.setText(_translate("MainWindow", "Edited Date:"))
        self.file_type_label.setText(_translate("MainWindow", "File Type:"))
        self.owner_label.setText(_translate("MainWindow", "Owner:"))
class Ui_file_window_ver2(object):
    def setupUi_file_window(self, MainWindow, add_file_call_back, search_by_criteria, download_file, update_file_call_back):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1124, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_tabel = QtWidgets.QTableWidget(self.centralwidget)
        self.file_tabel.setGeometry(QtCore.QRect(10, 150, 1111, 701))
        self.file_tabel.setObjectName("file_table")
        self.file_tabel.setRowCount(0)
        self.file_tabel.setColumnCount(3)
        self.file_tabel.setColumnWidth(0, 700)
        self.file_tabel.setColumnWidth(1, 200)
        self.file_tabel.setColumnWidth(2, 200)
        self.file_tabel.setHorizontalHeaderLabels(["File Name", "Date Created", "File Owner"])
        self.file_tabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tabel.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, download_file))
        self.search_file_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_file_line_edit.setGeometry(QtCore.QRect(140, 30, 981, 31))
        self.search_file_line_edit.setObjectName("search_file_line_edit")
        self.search_file_lable = QtWidgets.QLabel(self.centralwidget)
        self.search_file_lable.setGeometry(QtCore.QRect(140, 10, 371, 21))
        self.search_file_lable.setText("Search A File: ")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 10, 371, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.add_file_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_file(add_file_call_back, update_file_call_back))
        self.add_file_pushButton.setGeometry(QtCore.QRect(0, 30, 131, 31))
        # self.add_file_pushButton.clicked.connect(self.add_file)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/icons8-file-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_file_pushButton.setIcon(icon)
        self.add_file_pushButton.setIconSize(QtCore.QSize(24, 24))
        self.add_file_pushButton.setObjectName("add_file_pushButton")
        self.search_file_button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.search(search_by_criteria))
        self.search_file_button.setGeometry(QtCore.QRect(0, 90, 131, 31))
        self.search_file_button.setObjectName("search_file_pushButton")
        #self.download_file_button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.download(download_file))
        #self.download_file_button.setGeometry(QtCore.QRect(0, 102, 131, 31))
        #self.download_file_button.setObjectName("download_file_button")
        self.download_dir = os.path.expanduser("~/Downloads")
        self.download_dir_label = QtWidgets.QLabel(self.centralwidget)
        self.download_dir_label.setGeometry(QtCore.QRect(500, 0, 400, 31))
        self.download_dir_label.setObjectName("download_file_label")
        # self.choose_download_dir_button = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.choose_download_dir())
        # self.choose_download_dir_button.setGeometry(960, 90, 150, 31)
        # self.choose_download_dir_button.setObjectName("choose_download_dir_button")
        self.search_keyword_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_keyword_lineEdit.setGeometry(QtCore.QRect(140, 90, 181, 31))
        self.search_keyword_lineEdit.setObjectName("search_keyword_lineEdit")
        self.search_keyword_lable = QtWidgets.QLabel(self.centralwidget)
        self.search_keyword_lable.setGeometry(QtCore.QRect(140, 70, 371, 21))
        self.search_keyword_lable.setText("Enter Keyword to search: ")
        self.search_keyword_lable.setObjectName("search_keyword_lable")
        self.edited_date_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.edited_date_comboBox.setGeometry(QtCore.QRect(340, 90, 181, 31))
        self.edited_date_comboBox.setCurrentText("")
        self.edited_date_comboBox.setObjectName("edited_date_comboBox")
        self.edited_date_comboBox.addItem("All")
        self.edited_date_comboBox.addItems(["today", "the last seven days", "the last thirty days", "this year", "custom date range"])
        self.file_type_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.file_type_comboBox.setGeometry(QtCore.QRect(540, 90, 191, 31))
        self.file_type_comboBox.setObjectName("file_type_comboBox")
        self.file_type_comboBox.addItem("All")
        self.file_type_comboBox.addItems(["txt", "docx", "pdf", "xlsx"])
        self.owner_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.owner_comboBox.setGeometry(QtCore.QRect(750, 90, 191, 31))
        self.owner_comboBox.setObjectName("owner_comboBox")
        self.owner_comboBox.addItem("All")
        self.edit_date_label = QtWidgets.QLabel(self.centralwidget)
        self.edit_date_label.setGeometry(QtCore.QRect(340, 70, 171, 16))
        self.edit_date_label.setObjectName("edit_date_label")
        self.file_type_label = QtWidgets.QLabel(self.centralwidget)
        self.file_type_label.setGeometry(QtCore.QRect(540, 70, 171, 16))
        self.file_type_label.setObjectName("file_type_label")
        self.owner_label = QtWidgets.QLabel(self.centralwidget)
        self.owner_label.setGeometry(QtCore.QRect(750, 70, 171, 16))
        self.owner_label.setObjectName("owner_label")
        self.edited_date_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.edited_date_comboBox.setGeometry(QtCore.QRect(340, 90, 181, 31))
        self.edited_date_comboBox.setCurrentText("")
        self.edited_date_comboBox.setObjectName("edited_date_comboBox")
        self.edited_date_comboBox.addItem("All")
        self.edited_date_comboBox.addItems(
            ["today", "the last seven days", "the last thirty days", "this year", "custom date range"])
        self.edited_date_comboBox.activated.connect(self.handle_date_range_selection)
        self.custom_date_range_widget = None  # Initialize the custom date range widget
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def show_context_menu(self, pos, download_file_func):
        # Create a QMenu instance
        menu = QMenu(self.file_tabel)

        # Create a QAction for the "Download File" option
        download_action = QAction("Download File", self.file_tabel)
        download_action.triggered.connect(lambda: self.download_selected_file(download_file_func))

        # Add the action to the menu
        menu.addAction(download_action)

        # Show the context menu at the specified position
        menu.exec_(self.file_tabel.mapToGlobal(pos))

    def download_selected_file(self, download_file_func):
        selected_items = self.file_tabel.selectedItems()
        if selected_items:
            print("hej 2")
            selected_item = selected_items[0]
            row = selected_item.row()
            file_name = self.file_tabel.item(row, 0).text()
            answer = download_file_func(file_name, self.download_dir)
            if answer == "file is being used":
                msg_box = QMessageBox()
                msg_box.setWindowTitle("error")
                msg_box.setText("File is being used. To download close it and retry")
                msg_box.exec_()
                return
            os.startfile(self.download_dir)

    def download(self, download_file):
        selected_items = self.file_tabel.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
            row = selected_item.row()
            column = selected_item.column()

            if column == 0:  # Check if selected item is from the correct column
                item_text = selected_item.text()
                download_file(item_text, self.download_dir)
            else:
                print("Selected item is not from the correct column.")

    def choose_download_dir(self):
        print(self.download_dir)
        self.download_dir = QFileDialog.getExistingDirectory(None, "pick a folder", os.path.expanduser("~"))
        self.download_dir_label.setText(f"downloading to: {self.download_dir}")
        print(self.download_dir)


    def search(self, search_by_criteria):
        search = self.search_file_line_edit.text()
        file_type = self.file_type_comboBox.currentText()
        date = self.edited_date_comboBox.currentText()
        if date == "custom date range":
            start_date = self.start_date_edit.text()
            end_date = self.end_date_edit.text()
        else:
            start_date = ""
            end_date = ""
        files = search_by_criteria(search, file_type, date, start_date, end_date)
        self.file_tabel.clearContents()
        self.file_tabel.setRowCount(0)
        for item in files:
            self.add_file_to_list(item)

    def handle_date_range_selection(self, index):
        if index == self.edited_date_comboBox.count() - 1:  # Check if the "custom date range" option is selected
            if self.custom_date_range_widget is None or not self.custom_date_range_widget.isVisible():
                self.show_custom_date_range_dialog()
            else:
                self.hide_custom_date_range_dialog()
        else:
            self.hide_custom_date_range_dialog()
            self.selected_start_date = None
            self.selected_end_date = None

    def show_custom_date_range_dialog(self):
        self.custom_date_range_dialog = QtWidgets.QDialog(self.centralwidget)
        self.custom_date_range_dialog.setWindowTitle("Select Custom Date Range")
        self.custom_date_range_dialog.setModal(True)

        layout = QtWidgets.QVBoxLayout(self.custom_date_range_dialog)

        date_range_layout = QtWidgets.QHBoxLayout()

        start_date_label = QtWidgets.QLabel("Start Date:")
        self.start_date_edit = QtWidgets.QDateEdit(self.custom_date_range_dialog)
        self.start_date_edit.setCalendarPopup(True)
        date_range_layout.addWidget(start_date_label)
        date_range_layout.addWidget(self.start_date_edit)

        end_date_label = QtWidgets.QLabel("End Date:")
        self.end_date_edit = QtWidgets.QDateEdit(self.custom_date_range_dialog)
        self.end_date_edit.setCalendarPopup(True)
        date_range_layout.addWidget(end_date_label)
        date_range_layout.addWidget(self.end_date_edit)

        layout.addLayout(date_range_layout)

        button_layout = QtWidgets.QHBoxLayout()
        confirm_button = QtWidgets.QPushButton("Confirm")
        cancel_button = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        confirm_button.clicked.connect(
            lambda: self.handle_custom_date_range_confirmation(self.start_date_edit, self.end_date_edit))
        cancel_button.clicked.connect(self.hide_custom_date_range_dialog)

        self.custom_date_range_dialog.exec_()

    def hide_custom_date_range_dialog(self):
        self.custom_date_range_dialog.hide()

    def handle_custom_date_range_confirmation(self, start_date_edit, end_date_edit):
        start_date = start_date_edit.date()
        end_date = end_date_edit.date()
        if start_date > end_date:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("date error")
            msg_box.setText("Invalid date range")
            msg_box.exec_()
            return
        self.selected_start_date = start_date
        self.selected_end_date = end_date

        # Update the edited_date_comboBox to display the selected date range
        date_range_text = f"{start_date.toString('MMM d, yyyy')} - {end_date.toString('MMM d, yyyy')}"
        self.edited_date_comboBox.setItemText(self.edited_date_comboBox.count() - 1, date_range_text)

        print(f"Selected date range: {start_date.toString()} - {end_date.toString()}")

        self.hide_custom_date_range_dialog()

    def add_file(self, add_file_call_back, update_file_call_back):
        self.file_name, answer, file_path = add_file_call_back()
        if answer != "Saved File" and answer != "file already exists":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Bomboclat")
            msg_box.setText(answer)
            msg_box.exec_()
            return
        elif answer == "file already exists":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Update or not")
            msg_box.setText("file already exist would you like to update")
            msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

            button = msg_box.exec_()
            if button == QMessageBox.Yes:
                answer, self.file_name = update_file_call_back(file_path)
                if answer != "Updated":
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Bomboclat")
                    msg_box.setText(answer)
                    msg_box.exec_()
                    return

            else:
                return
        self.file_tabel.clearContents()
        self.file_tabel.setRowCount(0)
        for item in self.file_name:
            self.add_file_to_list(item)


    def add_file_to_list(self, file):
        print(file)
        self.file_tabel.setRowCount(self.file_tabel.rowCount() + 1)
        column = 0
        row = self.file_tabel.rowCount() - 1
        print(row)
        for item in file:
            self.file_tabel.setItem(row, column, QTableWidgetItem(item))
            column += 1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "file_window"))
        self.search_file_line_edit.setText(_translate("MainWindow", ""))
        self.add_file_pushButton.setText(_translate("MainWindow", "Add File"))
        self.search_keyword_lineEdit.setText(_translate("MainWindow", ""))
        self.edit_date_label.setText(_translate("MainWindow", "Edited Date:"))
        self.file_type_label.setText(_translate("MainWindow", "File Type:"))
        self.owner_label.setText(_translate("MainWindow", "Owner:"))
        self.search_file_button.setText(_translate("MainWindow", "Search"))
        # self.download_file_button.setText(_translate("MainWindow", "download file"))
        self.download_dir_label.setText(_translate("MainWindow", f"downloading to: {self.download_dir}"))
        # self.choose_download_dir_button.setText(_translate("MainWindow", "choose download directory"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LogInOrRegister()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
