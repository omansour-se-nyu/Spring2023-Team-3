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
from datetime import datetime


class DeletePatient(QMainWindow):
    def __init__(self, uid, current_user, role, record):
        super().__init__()
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.record = record
        self.patient_id = None
        var = os.path.dirname(os.path.abspath(__file__)) + "/delete_patient.ui"
        uic.loadUi(var, self)
        self.pushButton_3.clicked.connect(self.delete_patient)
        self.pushButton.clicked.connect(self.delete_record)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])
        # self.postgresDB = postgres_local.PostgresToolbox(config.remote_postgre["dbname"],
        #                                                  config.remote_postgre["user"],
        #                                                  config.remote_postgre["pwd"],
        #                                                  config.remote_postgre["host"],
        #                                                  config.remote_postgre["port"])

    def delete_patient(self): #delete patient from patients table and all records corresponding to patient id from records table
        self.patient_id = "'%s'" % self.lineEdit.text()
        exception2 = self.postgresDB.insertData('delete from mentcare.records where patient_id = ' + self.patient_id)
        exception1 = self.postgresDB.insertData('delete from mentcare.patients where id = ' + self.patient_id)
        # exception2 = self.postgresDB.executeSql('delete from mentcare.records where patient_id = ' + self.patient_id)
        # exception1 = self.postgresDB.executeSql('delete from mentcare.patients where id = ' + self.patient_id)
        global prompt2
        if exception1 == None and exception2 == None:
            prompt2 = prompt_dialog.Prompt("Patient Successfully Deleted")
            prompt2.show()
        else:
            prompt2 = prompt_dialog.Prompt("Patient Deletion Failed")
            prompt2.show()

    def delete_record(self):
        if isinstance(self.record, pd.core.series.Series):
            print("to frame:")
            self.record = self.record.to_frame()
        if self.lineEdit_3.text() != '':
            self.record_id = "'%s'" % self.lineEdit_3.text()
        else:
            rec_id = "'%s'" % self.record.iloc[2]
            self.record_id = "'%s'" % rec_id.split()[1]
            # print("id" + str(id))
            # self.record_id = self.record_id.split(" ")[1]
        # print(self.record, type(self.record))
        print("record_id" + str(self.record_id))
        exception = self.postgresDB.insertData('delete from mentcare.records where record_id = ' + self.record_id)
        # exception = self.postgresDB.executeSql('delete from mentcare.records where record_id = ' + self.record_id)
        global prompt2
        if exception == None:
            prompt2 = prompt_dialog.Prompt("Record Successfully Deleted")
            prompt2.show()
        else:
            prompt2 = prompt_dialog.Prompt("Record Deletion Failed")
            prompt2.show()

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.id, self.current_user, self.role)
        backToMenu.show()
        self.close()
