from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt5 import uic
import menu
import view_record
import delete_patient
import postgres_connect
import postgres_local
import config
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal
import prompt_dialog
import numpy as np
from functools import partial
import delete_patient


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class ButtonWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, uid, current_user, role, record):
        super(ButtonWidget, self).__init__()
        self.button = QPushButton("View")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.record = record

        self.button.clicked.connect(self.view_record)
        # self.button.clicked.connect(self.clicked)

    def view_record(self):
        global viewRecord
        viewRecord = view_record.ViewRecord(self.id, self.current_user, self.role, self.record)
        viewRecord.show()
        # self.close()


class DeleteButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, uid, current_user, role, record):
        super(DeleteButton, self).__init__()
        self.button = QPushButton("Delete")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.record = record

        self.button.clicked.connect(self.delete_patient)

    def delete_patient(self):
        global deletePatient
        deletePatient = delete_patient.DeletePatient(self.id, self.current_user, self.role, self.record)
        deletePatient.delete_record()


    # def clicked(self):
    #     return True

class FindPatient(QMainWindow):
    def __init__(self, uid, current_user, role):
        super().__init__()
        self.id = uid
        self.current_user = current_user
        self.role = role
        var = os.path.dirname(os.path.abspath(__file__)) + "/find_patient.ui"
        uic.loadUi(var, self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])
        # self.postgresDB = postgres_local.PostgresToolbox(config.remote_postgre["dbname"],
        #                                                    config.remote_postgre["user"],
        #                                                    config.remote_postgre["pwd"],
        #                                                    config.remote_postgre["host"],
        #                                                    config.remote_postgre["port"])

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.id, self.current_user, self.role)
        backToMenu.show()
        self.close()

    def search(self):
        self.patient = self.lineEdit.text()
        self.patientid = "'%s'" % self.patient

        self.df = self.postgresDB.getRow('select * from "mentcare".patients where id = ' + self.patientid
                                         + ' or patients.name = ' + self.patientid)
        # self.df = self.postgresDB.executeSql('select * from "mentcare".patients where id = ' + self.patientid
        #                                  + ' or patients.name = ' + self.patientid)
        if self.df is None:
            global prompt
            prompt = prompt_dialog.Prompt("Can't find the patient")
            prompt.show()
            return False
        patients_cols = ['id', 'name', 'gender', 'ssn', 'phone', 'email', 'address', 'birth_date']
        patient_info = pd.DataFrame(list(self.df), patients_cols)
        print(patient_info.shape)

        patient_info['Columns'] = patients_cols
        patient_info = patient_info.iloc[:, :-1].assign(Columns=patient_info['Columns'])
        patient_info.iloc[:, [0, 1]] = patient_info.iloc[:, [1, 0]].values
        patient_info.columns.values[0] = 'Columns'
        patient_info.columns.values[1] = 'Values'

        self.patientid = "'%s'" % self.df[0]

        records_cols = ['patient_id', 'doctor_id', 'record_id', 'last_modified', 'content']
        record = self.postgresDB.getRowAll('select * from mentcare.records where patient_id = ' + self.patientid, records_cols)
        # record = self.postgresDB.executeSql('select * from mentcare.records where patient_id = ' + self.patientid,records_cols)
        #comb = record.append(self.df, ignore_index=True)

        model = pandasModel(patient_info)
        self.tableView.setModel(model)
        self.tableView.show()

        record['Full Record'] = ""
        record['Delete'] = ""

        if record is not None:
            model = pandasModel(record)

            self.tableView_2.setModel(model)
            #self.tableView_2.resize(200, 100)
            rowCount = model.rowCount()
            columnCount = model.columnCount()-1
            print(rowCount, columnCount)
            for i in range(rowCount):
                button_widget = ButtonWidget(self.id, self.current_user, self.role, record.loc[i])
                self.tableView_2.setIndexWidget(model.index(i, columnCount-1), button_widget)
            for i in range(rowCount):
                delete_button = DeleteButton(self.id, self.current_user, self.role, record.loc[i])
                self.tableView_2.setIndexWidget(model.index(i, columnCount), delete_button)
            self.tableView_2.show()






