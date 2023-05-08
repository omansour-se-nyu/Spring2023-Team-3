from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QFont
import postgres_connect
from postgres_local import PostgresToolBox
import config
import os
import pandas as pd
import menu
import prompt_dialog
from datetime import datetime


class EditRecord(QMainWindow):
    def __init__(self, uid, current_user, role):
        super().__init__()
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.patient_id = None
        var = os.path.dirname(os.path.abspath(__file__)) + "/edit_record.ui"
        uic.loadUi(var, self)
        self.pushButton_3.clicked.connect(self.check_record)
        self.pushButton.clicked.connect(self.edit_record)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        # self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
        #                                                            config.remote_postgre["port"],
        #                                                            config.remote_postgre["username"],
        #                                                            config.remote_postgre["passwd"],
        #                                                            config.remote_postgre["database"])
        self.postgresDB = PostgresToolBox()

    def edit_record(self):
        self.content = "'%s'" % self.lineEdit_2.text()
        self.last_modified = "'%s'" % datetime.now()
        # exception = self.postgresDB.insertData('update mentcare.records set last_modified = ' + self.last_modified + ' ,content = ' + self.content + ' where patient_id = ' + self.patient_id + 'and record_id = ' + self.record_id)
        exception = self.postgresDB.executeSql('update mentcare.records set last_modified = ' + self.last_modified + ' ,content = ' + self.content + ' where patient_id = ' + self.patient_id + 'and record_id = ' + self.record_id)
        print(exception)
        global prompt2
        if exception == None:
            prompt2 = prompt_dialog.Prompt("Record Successfully Edited")
            prompt2.show()
        else:
            prompt2 = prompt_dialog.Prompt("Record Edit Failed")
            prompt2.show()

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.id, self.current_user, self.role)
        backToMenu.show()
        self.close()

    def check_record(self):
        self.patient_id = self.lineEdit.text()
        self.patient_id = "'%s'" % self.patient_id

        self.record_id = self.lineEdit_3.text()
        self.record_id = "'%s'" % self.record_id

        # self.df = self.postgresDB.getRow('select content from mentcare.records where patient_id = ' + self.patient_id + 'and record_id = ' + self.record_id)
        self.df = self.postgresDB.executeSql('select content from mentcare.records where patient_id = ' + self.patient_id + 'and record_id = ' + self.record_id, False)
        global prompt
        if self.df is None:
            self.patient_check = self.postgresDB.executeSql('select patient_id from mentcare.records where patient_id = ' + self.patient_id, False)
            self.record_check = self.postgresDB.executeSql('select record_id from mentcare.records where record_id = ' + self.record_id, False)
            # self.patient_check = self.postgresDB.executeSql(
            #     'select patient_id from mentcare.records where patient_id = ' + self.patient_id)
            # self.record_check = self.postgresDB.executeSql(
            #     'select record_id from mentcare.records where record_id = ' + self.record_id)
            if self.patient_check == None and self.record_check == None:
                prompt = prompt_dialog.Prompt("Can't find the patient or record.")
                prompt.show()
            elif self.patient_check == None:
                prompt = prompt_dialog.Prompt("Can't find the patient.")
                prompt.show()
            elif self.record_check == None:
                prompt = prompt_dialog.Prompt("Can't find the record.")
                prompt.show()
            return False

        # self.df2 = self.postgresDB.getwRow('select name from mentcare.patients where id = ' + self.patient_id)
        self.df2 = self.postgresDB.executeSql('select name from mentcare.patients where id = ' + self.patient_id, False).iloc[0]
        patient_name = self.df2[0]
        prompt = prompt_dialog.Prompt('Now you are editing \nthe records of ' + patient_name + '.')
        prompt.label.setFont(QFont("Arial", 18))
        prompt.show()

        return True