import os
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5 import uic
import bcrypt
import login

class CreateAccount(QDialog):
    def __init__(self, postgresDB):
        super().__init__()
        var = os.path.dirname(os.path.abspath(__file__)) + "/create_account.ui"
        uic.loadUi(var, self)
        self.postgresDB = postgresDB
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton.clicked.connect(self.back_to_login)

    def register(self):
        self.create_user = self.lineEdit.text()
        self.create_password = self.lineEdit_2.text()
        if self.create_user == "" or self.create_password == "":
            self.label_6.setText("Please fill the correct Username or Password.")
            return False
        self.hashed_passworf = self.hash(self.create_password)

        self.create_user = "'%s'" % self.create_user
        self.hashed_passworf = "'%s'" % self.hashed_passworf
        query = 'insert into "Security".login(username,password) values(' + self.create_user + "," + self.hashed_passworf + ")"
        print(query)
        # self.postgresDB.insertData(query)
        exception = self.postgresDB.insertData(query)
        if exception == None:
            self.back_to_login()
        else:
            self.label_6.setText(exception)



    def hash(self, password):
        bytes = password.encode('utf-8')

        # gen salt
        salt = bcrypt.gensalt()

        # Hashing the password
        result = bcrypt.hashpw(bytes, salt)

        return result.decode("utf-8")

    def back_to_login(self):
        global back
        back = login.LoginPage(self.postgresDB)
        back.show()
        self.close()


