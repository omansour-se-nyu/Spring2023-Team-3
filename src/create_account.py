import os
import sys
from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame
from PyQt5 import uic
import bcrypt
import login
from random import randint
import config

class CreateAccount(QDialog):
    def __init__(self):
        super().__init__()
        self.set_ui()
        var = os.path.dirname(os.path.abspath(__file__)) + "/create_account.ui"
        uic.loadUi(var, self)
        self.postgresDB = config.DBconnect
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton.clicked.connect(self.back_to_login)


    def set_ui(self):
        self.frame = QFrame(self)
        self.frame.resize(150,150)
        self.frame.move(160, -5)
        var = os.path.dirname(os.path.abspath(__file__)) + "/IMG/python-logo.png"
        self.frame.setStyleSheet(
            'background-image: url(' + var + '); background-repeat: no-repeat; text-align:center;')

    def register(self):
        n = 8
        id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while self.id_existed(id):
            id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])


        self.create_user = self.lineEdit.text()
        self.create_password = self.lineEdit_2.text()

        if self.comboBox.currentText() == "Medical Staff":
            self.isadmin = "'false'"
        else:
            self.isadmin = "'true'"

        if self.create_user == "" or self.create_password == "":
            self.label_6.setText("Please fill the correct Username or Password.")
            return False

        if self.is_taken_user():
            self.label_6.setText("This username has been taken, please choose another thanks.")
            return False
        self.hashed_passworf = self.hash(self.create_password)

        self.login_id = "'%s'" % id
        self.create_user = "'%s'" % self.create_user
        self.hashed_passworf = "'%s'" % self.hashed_passworf
        query = 'insert into ' + config.schema +'.login(id, isadmin, username, password) ' \
                'values(' + self.login_id + ","  + self.isadmin + ","  + self.create_user + "," + self.hashed_passworf + ")"
        print(query)
        #exception = self.postgresDB.insertData(query)
        exception = self.postgresDB.executeSql(query)
        if exception == None:
            self.back_to_login()
        else:
            self.label_6.setText("Error!")


    def id_existed(self, id):
        id = "'%s'" %id
        sql = 'select id from ' + config.schema +'.login where id =' + id
        if self.postgresDB.exists(sql):
            return True
        return False

    def is_taken_user(self):
        self.username = "'%s'" % self.create_user
        self.postgresDB.connect()
        self.account_df = self.postgresDB.getRow(
            'select id,  isadmin, username, password from ' + config.schema +'.login where username =  ' + self.username)
        # self.account_df = self.postgresDB.executeSql(
        #     'select id,  isadmin, username, password from ' + config.schema +'.login where username =  ' + self.username)
        if self.account_df is None:
            return False
        return True

    def hash(self, password):
        bytes = password.encode('utf-8')

        # gen salt
        salt = bcrypt.gensalt()

        # Hashing the password
        result = bcrypt.hashpw(bytes, salt)

        return result.decode("utf-8")

    def back_to_login(self):
        global back
        back = login.LoginPage()
        back.show()
        self.close()


