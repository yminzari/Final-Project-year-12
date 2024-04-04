# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Register.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
# import Icon_resorce_rc


class Ui_RegisterWindow(object):
    def BackToLogInOrRegister(self, MainWindow, LogInOrRegister):
        LogInOrRegister.show()
        MainWindow.hide()

    def setupUi(self, MainWindow, LogInOrRegister):
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
        self.Enter = QtWidgets.QPushButton(self.centralwidget)
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
        self.SwitchToLogin = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.BackToLogInOrRegister(MainWindow, LogInOrRegister))
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
        self.label_4 = QtWidgets.QLabel(self.Password_box)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.ConfirmPassword_LineEdit = QtWidgets.QLineEdit(self.Password_box)
        self.ConfirmPassword_LineEdit.setGeometry(QtCore.QRect(10, 140, 241, 31))
        self.ConfirmPassword_LineEdit.setObjectName("ConfirmPassword_LineEdit")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(700, 440, 61, 41))
        self.label_7.setMaximumSize(QtCore.QSize(71, 16777215))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../../../Downloads/icons8-question-30.png"))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(700, 160, 61, 41))
        self.label_8.setMaximumSize(QtCore.QSize(71, 16777215))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("../../../Downloads/icons8-question-30.png"))
        self.label_8.setObjectName("label_8")
        # Add toolTips to the labels
        QtWidgets.QToolTip.setFont(QFont('Arial', 8))
        self.label_7.setToolTip('Password must be at least 6 characters and must include a number and a special character')
        self.label_7.resize(self.label_7.sizeHint())
        self.label_7.move(700, 440)
        self.label_8.setToolTip('Username must be longer then 5 characters')
        self.label_8.resize(self.label_8.sizeHint())
        self.label_8.move(700, 160)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_RegisterWindow()
    ui.setupUi(MainWindow, "")
    MainWindow.show()
    sys.exit(app.exec_())
