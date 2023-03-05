import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from src.menu import MainMenu
from src.find_patient import FindPatient
from src.postgres_connect import PostgresHandler
from src.create_account import CreateAccount

class LoginPage(QDialog):
    def __init__(self, postgresDB):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.create_account)
        self.current_user = None
        self.postgresDB = postgresDB

    def login(self):
        self.current_user = self.lineEdit.text()
        self.current_password = self.lineEdit_2.text()
        self.role = ""
        if self.radioButton.isChecked():
            self.role = "Medical Staff"
        if self.radioButton2.isChecked():
            self.role = "Admin"
        if not self.is_valid_user():
            print("Not a registered account")
            self.label_6.setText("User not registered - please sign up or try again.")
        else:
            global menu
            menu = MainMenu()
            QApplication.processEvents()
            menu.label_2.setText("Logged in as: " + self.current_user)
            menu.label_3.setText("Role: " + self.role)
            menu.show()
            menu.pushButton.clicked.connect(self.find_patient)
            self.close()

    def medical_selected(self):
        if self.radioButton.isChecked():
            self.role = "Medical Staff"
            print("Medical Staff")

    def admin_selected(self):
        if self.radioButton2.isChecked():
            self.role = "Admin"
            print("Admin")

    def create_account(self): #still need to implement create account logic (connection being lost)
        global create_account
        create_account = CreateAccount(self.postgresDB)
        create_account.pushButton_2.clicked.connect(self.register)
        create_account.pushButton.clicked.connect(self.back_to_login)
        create_account.show()
        self.close()

    def back_to_login(self):
        login_page.show()
        create_account.close()

    def register(self):
        create_user = create_account.lineEdit.text()
        create_password = create_account.lineEdit_2.text()
        create_user = "'%s'" % create_user
        create_password = "'%s'" % create_password
        query = 'insert into "Security".login(username,password) values(' + create_user + "," + create_password + ")"
        print(query)
        # self.postgresDB.insertData(query)
        create_account.postgresDB.insertData(query)

    def is_valid_user(self):
        account_df = self.postgresDB.getQuery('select * from "Security".login')
        print(account_df)
        rslt_df = account_df[account_df[0] == self.current_user]
        print(rslt_df.at[0, 1])
        hashed_password = rslt_df.at[0, 1]
        # unhashed_password = self.unhash(rslt_df.at[0, 1])
        if self.current_password == hashed_password:
            print("Registered account")
            return True
        return False

    def find_patient(self):
        global findPatient
        findPatient = FindPatient()
        QApplication.processEvents()
        findPatient.show()
        findPatient.pushButton.clicked.connect(self.search)
        menu.close()

    def search(self):
        patient = findPatient.lineEdit.text()
        df=None
        if patient.isnumeric():
            df=self.postgresDB.getQuery('select * from patients where id=='+patient)
        else:
            df=self.postgresDB.getQuery('select * from patients where name=='+patient)
        print(df)

    def unhash(self, hashed_password): #implement unhashing
        pass

if __name__ == '__main__':
    postgresDB = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    app = QApplication(sys.argv)
    global login_page
    login_page = LoginPage(postgresDB)
    login_page.show()
    sys.exit(app.exec_())