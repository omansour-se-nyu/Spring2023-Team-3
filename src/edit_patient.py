from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import postgres_connect
import config
import os
import pandas as pd
import menu

class EditPatient(QMainWindow):
    def __init__(self, current_user, role):
        super().__init__()
        self.current_user = current_user
        self.role = role
        self.patientid = None
        var = os.path.dirname(os.path.abspath(__file__)) + "/edit_patient.ui"
        uic.loadUi(var, self)
        self.pushButton.clicked.connect(self.check_record)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        self.pushButton_3.clicked.connect(self.edit_patient)
        self.pushButton_4.clicked.connect(self.edit_medication)
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])

    def edit_patient(self):
        option = self.comboBox.currentText()
        content = "'%s'" % self.lineEdit_2.text()
        self.df = self.postgresDB.insertData('update public.patients set ' + option + ' = ' + content + ' where id = ' + self.patientid)

    def edit_medication(self):
        content = "'%s'" % self.lineEdit_3.text()
        self.df = self.postgresDB.insertData('update public.records set content = ' + content + ' where id = ' + self.patientid)

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.current_user, self.role)
        backToMenu.show()
        self.close()

    def check_record(self):
        self.userinput = self.lineEdit.text()
        self.patientid = "'%s'" % self.userinput
        cols = ['id']
        self.df = self.postgresDB.getRow('select id from public.patients where id = ' + self.patientid + ' or name = ' + self.patientid, cols)
        if not self.df.empty:
            for index, row in self.df.iterrows():
                self.patientid = "'%s'" % row['id']
                return True
        else:
            return False
        


