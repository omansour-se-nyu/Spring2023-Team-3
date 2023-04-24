from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QFont
import postgres_connect
import postgres_local
import config
import os
import pandas as pd
import menu
import prompt_dialog

class EditPatient(QMainWindow):
    def __init__(self, uid, current_user, role):
        super().__init__()
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.patientid = None
        var = os.path.dirname(os.path.abspath(__file__)) + "/edit_patient.ui"
        uic.loadUi(var, self)
        self.pushButton.clicked.connect(self.check_record)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        self.pushButton_3.clicked.connect(self.edit_patient)
        self.pushButton_4.clicked.connect(self.edit_medication)
        self.postgresDB = config.DBconnect
        # self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
        #                                                    config.remote_postgre["port"],
        #                                                    config.remote_postgre["username"],
        #                                                    config.remote_postgre["passwd"],
        #                                                    config.remote_postgre["database"])
        # self.postgresDB = postgres_local.PostgresToolbox(config.remote_postgre["dbname"],
        #                                                  config.remote_postgre["user"],
        #                                                  config.remote_postgre["pwd"],
        #                                                  config.remote_postgre["host"],
        #                                                  config.remote_postgre["port"])

    def edit_patient(self):
        option = self.comboBox.currentText()
        content = "'%s'" % self.lineEdit_2.text()
        #exception = self.postgresDB.insertData('update mentcare.patients set ' + option + ' = ' + content + ' where id = ' + self.patientid)
        exception = self.postgresDB.executeSql('update ' + config.schema +'.patients set ' + option + ' = ' + content + ' where id = ' + self.patientid)
        global prompt2
        if exception == None:
            prompt2 = prompt_dialog.Prompt("Patient Successfully Edited")
            prompt2.show()
        else:
            prompt2 = prompt_dialog.Prompt("Patient Edit Failed")
            prompt2.show()


    def edit_medication(self):
        pass
        # content = "'%s'" % self.lineEdit_3.text()
        # self.df = self.postgresDB.insertData('update mentcare.records set content = ' + content + ' where patient_id = ' + self.patientid)

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.id, self.current_user, self.role)
        backToMenu.show()
        self.close()

    def check_record(self):
        self.userinput = self.lineEdit.text()
        self.patientid = "'%s'" % self.userinput
        self.df = self.postgresDB.getRow('select id, name from ' + config.schema +'.patients where id = ' + self.patientid)
        #self.df = self.postgresDB.executeSql('select id, name from mentcare.patients where id = ' + self.patientid)
        global prompt
        if self.df is None:
            prompt = prompt_dialog.Prompt("Can't find the patient")
            prompt.show()
            return False

        self.patientid = "'%s'" % self.df[0]
        patient_name  = self.df[1]
        prompt = prompt_dialog.Prompt('Now you are editing \ninformation of ' + patient_name)
        #prompt.label.setFont(QFont("Arial" ,18))
        prompt.show()

        return True
        


