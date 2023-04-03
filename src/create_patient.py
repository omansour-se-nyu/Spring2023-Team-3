from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import menu
import postgres_connect
import config
from random import randint
import os
from datetime import datetime, timezone

class CreatePatient(QDialog):
    def __init__(self, current_user, role):
        super().__init__()
        self.current_user = current_user
        self.role = role
        var = os.path.dirname(os.path.abspath(__file__)) + "/create_patient.ui"
        uic.loadUi(var, self)
        self.label_9.setText("")
        self.label_12.setText("")
        self.label_10.setText("")

        self.pushButton_2.clicked.connect(self.register)
        self.pushButton.clicked.connect(self.back_to_menu)
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])


    # the button with Save
    def register(self):
        n = 8
        
        id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while self.id_existed(id):
            id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        self.patient_id = id

        self.patient_name = self.lineEdit.text()
        self.patient_email = self.lineEdit_3.text()
        self.patient_gender = self.comboBox.currentText()
        self.patient_phone = self.lineEdit_2.text()
        #self.patient_birth = self.calendarWidget.selectedDate() # PyQt5.QtCore.QDate(2023, 2, 12)
        self.patient_age = self.lineEdit_5.text()
        self.patient_ssn = self.lineEdit_4.text()
        self.patinet_address = self.lineEdit_6.text()

        if self.patient_name == "":
            self.label_9.setText("Empty")
            print(1)
            return False
        if self.patient_gender == "None":
            self.label_12.setText("Choose a gender")
            print(2)
            return False
        if self.patient_ssn == "":
            self.label_10.setText("Empty")
            print(3)
            return False

        self.patient_id = "'%s'" % self.patient_id
        self.patient_name = "'%s'" % self.patient_name
        self.patient_email = "'%s'" %self.patient_email
        self.patient_gender = "'%s'" %self.patient_gender
        self.patient_age = "'%s'" %self.patient_age
        self.patient_phone = "'%s'" %self.patient_phone
        self.patient_ssn = "'%s'" %self.patient_ssn
        self.patinet_address = "'%s'" %self.patinet_address

        # print(self.patient_id)
        # print(self.patient_name)
        # print(self.patient_email)
        # print(self.patient_gender)
        # print(self.patient_phone)
        # print(self.patient_ssn)

        tableName = '"public".patients'
        schema = 'id, name, gender, age, ssn, phone, email, address'
        data = self.patient_id + "," + self.patient_name + "," \
               + self.patient_gender + "," + self.patient_age + "," \
               + self.patient_ssn + "," + self.patient_phone + "," + self.patient_email + "," + self.patinet_address

        sql = "insert into " + tableName + " (" + schema + ") values (" + data + ")"
        self.postgresDB.insertData(sql)

        id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        while self.record_id_existed(id):
            id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        id = "'%s'" % id

        now = datetime.now() 
        date_time = now.strftime('%m-%d-%Y %H:%M:%S')
        date_time = "'%s'" % date_time

        tableName = '"public".records'
        schema = 'id, record_id, last_modified, content'
        default = 'none'
        default = "'%s'" % default
        data = self.patient_id + ',' + id + ',' + date_time + ',' + default

        sql = "insert into " + tableName + " (" + schema + ") values (" + data + ")"
        self.postgresDB.insertData(sql)


    def id_existed(self, id):
        id = "'%s'" %id
        sql = 'select id from "public".patients where id =' + id
        if self.postgresDB.exists(sql):
            return True
        return False
    
    def record_id_existed(self, id):
        id = "'%s'" %id
        sql = 'select record_id from "public".records where record_id =' + id
        if self.postgresDB.exists(sql):
            return True
        return False

    # the button with cancel
    def back_to_menu(self):
        global back
        back = menu.MainMenu(self.current_user, self.role)
        back.show()
        self.close()