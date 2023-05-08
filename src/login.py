import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QFrame
import menu
import postgres_connect
import postgres_local
import create_account
import bcrypt

class LoginPage(QDialog):
    def __init__(self, postgresDB):
        super().__init__()
        self.set_ui()
        var = os.path.dirname(os.path.abspath(__file__)) + "/login.ui"
        uic.loadUi(var, self)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.create_account)
        self.current_user = None
        self.postgresDB = postgresDB


    def set_ui(self):
        self.frame = QFrame(self)
        self.frame.resize(150,150)
        self.frame.move(160, -5)
        var = os.path.dirname(os.path.abspath(__file__)) + "/IMG/python-logo.png"
        self.frame.setStyleSheet(
            'background-image: url(' + var + '); background-repeat: no-repeat; text-align:center;')

    def login(self):
        self.current_user = self.lineEdit.text()
        self.current_password = self.lineEdit_2.text()
        self.hashed_current_password = self.hash(self.current_password)
        self.role = self.roleSelection()
        # if self.radioButton.isChecked():
        #     self.role = "Medical Staff"
        # if self.radioButton2.isChecked():
        #     self.role = "Admin"
        if self.role == None:
            self.label_6.setText("Please select a role.")
            return False

        if not self.is_valid_user():
            print("Not a registered account")
            self.label_6.setText("User not registered - please sign up or try again.")
            return False
        else:
            global Menu
            Menu = menu.MainMenu(self.account_df[0],self.current_user, self.role)
            QApplication.processEvents()
            #menu.label_2.setText("Logged in as: " + self.current_user)
            #menu.label_3.setText("Role: " + self.role)
            Menu.show()
            #menu.pushButton.clicked.connect(self.find_patient)
            self.close()
            return True

    def roleSelection(self):
        if self.radioButton.isChecked():
            return False
        elif self.radioButton2.isChecked():
            return True

    # def medical_selected(self):
    #     if self.radioButton.isChecked():
    #         self.role = "Medical Staff"
    #         print("Medical Staff")
    #         return "Medical Staff"
    #
    # def admin_selected(self):
    #     if self.radioButton2.isChecked():
    #         self.role = "Admin"
    #         print("Admin")
    #         return

    def create_account(self): #still need to implement create account logic (connection being lost)
        global new_account
        new_account = create_account.CreateAccount(self.postgresDB)
        #create_account.pushButton_2.clicked.connect(create_account.register)
        #create_account.pushButton.clicked.connect(self.back_to_login)
        new_account.show()
        self.close()

    # def back_to_login(self):
    #     login_page.show()
    #     create_account.close()

    # def register(self):
    #     create_user = create_account.lineEdit.text()
    #     create_password = create_account.lineEdit_2.text()
    #     create_user = "'%s'" % create_user
    #     create_password = "'%s'" % create_password
    #     query = 'insert into "Security".login(username,password) values(' + create_user + "," + create_password + ")"
    #     print(query)
    #     # self.postgresDB.insertData(query)
    #     create_account.postgresDB.insertData(query)



    def is_valid_user(self):
        self.username  = "'%s'" % self.current_user
        #cols = ['id', 'isadmin','username', 'password']
        # self.account_df = self.postgresDB.getRow('select id, isadmin, username, password '
        #                                          'from "mentcare".login where username =  ' + self.username)
        self.account_df = self.postgresDB.executeSql('select id, isadmin, username, password '
                                                 'from "mentcare".login where username =  ' + self.username, False).iloc[0]

        if self.account_df is None:
            return False
        
        if bcrypt.hashpw(self.current_password.encode('utf-8'), self.account_df[3].encode('utf-8')).decode('UTF-8') \
                == self.account_df[3] and self.role==self.account_df[1]:
            print("Registered account")
            return True
        # for index, row in self.account_df.iterrows():
        #     #test whether the sign in password is same with the hashed password stored in database
        #     if bcrypt.hashpw(self.current_password.encode('utf-8'),row['password'].encode('utf-8')).decode('UTF-8') == row['password']:
        #         print("Registered account")
        #         return True

        return False

    # def find_patient(self):
    #     global findPatient
    #     findPatient = FindPatient()
    #     QApplication.processEvents()
    #     findPatient.show()
    #     findPatient.pushButton.clicked.connect(self.search)
    #     menu.close()

    # def search(self):
    #     patient = findPatient.lineEdit.text()
    #     print(patient)

    def hash(self, password):
        bytes = password.encode('utf-8')

        # gen salt
        salt = bcrypt.gensalt()

        # Hashing the password
        result = bcrypt.hashpw(bytes, salt)

        return result.decode("utf-8")


    def unhash(self, hashed_password): #implement unhashing
        pass

if __name__ == '__main__':
    # postgresDB = postgres_connect.PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    postgresDB = postgres_local.PostgresToolBox()
    app = QApplication(sys.argv)
    global login_page
    login_page = LoginPage(postgresDB)
    login_page.show()
    sys.exit(app.exec_())


# 69824438
