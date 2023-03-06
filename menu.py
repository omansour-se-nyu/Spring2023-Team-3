
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import find_patient
import create_patient
import login
import postgres_connect
import config


class MainMenu(QMainWindow):
    def __init__(self, current_user, role):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.current_user = current_user
        self.role = role
        self.label_2.setText("Logged in as: " + self.current_user)
        self.label_3.setText("Role: " + self.role)
        self.pushButton.clicked.connect(self.find_patient)
        self.pushButton_3.clicked.connect(self.create_patient)
        self.pushButton_7.clicked.connect(self.back_to_login)

    def find_patient(self):
        global findPatient
        findPatient = find_patient.FindPatient(self.current_user, self.role)
        QApplication.processEvents()
        findPatient.show()
        self.close()

    def create_patient(self):
        global createPatient
        createPatient = create_patient.CreatePatient(self.current_user, self.role)
        QApplication.processEvents()
        createPatient.show()
        self.close()

    def back_to_login(self):
        global backToLogin
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])
        backToLogin = login.LoginPage(self.postgresDB)
        backToLogin.show()
        self.close()



=======
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)

