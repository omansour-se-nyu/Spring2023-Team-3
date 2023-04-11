import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import find_patient
import create_patient
import edit_patient
import login
import postgres_connect
import config

class MainMenu(QMainWindow):
    def __init__(self, uid, current_user, role):
        super().__init__()
        var = os.path.dirname(os.path.abspath(__file__)) + "/menu.ui"
        uic.loadUi(var, self)
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.label_2.setText("Logged in as: " + self.current_user)
        if self.role:
            self.label_3.setText("Role: Admin" )
        else:
            self.label_3.setText("Role: Medical Staff")
        self.pushButton_2.clicked.connect(self.edit_patient)
        self.pushButton.clicked.connect(self.find_patient)
        self.pushButton_3.clicked.connect(self.create_patient)
        self.pushButton_7.clicked.connect(self.back_to_login)

    def edit_patient(self):
        global findPatient
        findPatient = edit_patient.EditPatient(self.id, self.current_user, self.role)
        QApplication.processEvents()
        findPatient.show()
        self.close()

    def find_patient(self):
        global findPatient
        findPatient = find_patient.FindPatient(self.id, self.current_user, self.role)
        QApplication.processEvents()
        findPatient.show()
        self.close()

    def create_patient(self):
        global createPatient
        createPatient = create_patient.CreatePatient(self.id, self.current_user, self.role)
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



