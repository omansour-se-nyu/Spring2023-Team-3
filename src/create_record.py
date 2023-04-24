from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore
import menu
import postgres_connect
import postgres_local
import config
from random import randint
import os
import prompt_dialog
from datetime import datetime


class CreateRecord(QDialog):
    def __init__(self, uid, current_user, role):
        super().__init__()
        self.userId = uid
        self.doctor_id = "'%s'" % uid
        self.current_user = current_user
        self.role = role
        var = os.path.dirname(os.path.abspath(__file__)) + "/create_record.ui"
        uic.loadUi(var, self)

        self.pushButton.clicked.connect(self.create)
        self.pushButton_2.clicked.connect(self.back_to_menu)
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

    def create(self):
        self.patient_id = self.lineEdit.text()
        self.record = self.lineEdit_2.text()
        self.last_modified = datetime.now()

        n = 8
        id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while self.id_existed(id):
            id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        self.record_id = id

        if self.patient_id == "":
            # self.label_9.setText("Empty")
            print(1)
            return False
        if self.record == "":
            # self.label_9.setText("Empty")
            print(2)
            return False

        self.patient_id = "'%s'" % self.patient_id
        self.record_id = "'%s'" % self.record_id
        self.last_modified = "'%s'" % self.last_modified
        self.record = "'%s'" % self.record

        tableName = config.schema +'.records'
        schema = 'patient_id, doctor_id, record_id, last_modified, content'
        data = self.patient_id + "," + self.doctor_id + "," \
               + self.record_id + "," + self.last_modified + "," \
               + self.record

        sql = "insert into " + tableName + " (" + schema + ") values (" + data + ")"
        #exception = self.postgresDB.insertData(sql)
        exception = self.postgresDB.executeSql(sql)
        global prompt
        if exception == None:
            prompt = prompt_dialog.Prompt("Creation Success")
            prompt.show()
        else:
            prompt = prompt_dialog.Prompt("Creation Failed")
            prompt.show()

    def id_existed(self, id):
        id = "'%s'" % id
        sql = 'select id from ' + config.schema +'.patients where id =' + id
        if self.postgresDB.exists(sql):
            return True
        return False
    #
    # def record_id_existed(self, id):
    #     id = "'%s'" % id
    #     sql = 'select record_id from "public".records where record_id =' + id
    #     if self.postgresDB.exists(sql):
    #         return True
    #     return False

    # the button with cancel
    def back_to_menu(self):
        global back
        back = menu.MainMenu(self.userId, self.current_user, self.role)
        back.show()
        self.close()