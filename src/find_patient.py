from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import menu
import postgres_connect
import config
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import prompt_dialog

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
        if self.df is None:
            global prompt
            prompt = prompt_dialog.Prompt("Can't find the patient")
            prompt.show()
            return False
        patients_cols = ['id', 'name', 'gender', 'ssn', 'phone', 'email', 'address', 'birth_date']
        patient_info = pd.DataFrame(list(self.df), patients_cols)
        print(patient_info.shape)
        self.patientid = "'%s'" % self.df[0]

        records_cols = ['patient_id', 'doctor_id', 'record_id', 'last_modified', 'content']
        record = self.postgresDB.getRowAll('select * from mentcare.records where patient_id = ' + self.patientid, records_cols)
        #comb = record.append(self.df, ignore_index=True)

        model = pandasModel(patient_info)
        self.tableView.setModel(model)
        #self.tableView.resize(200, 100)
        self.tableView.show()

        if record is not None:
            model = pandasModel(record)
            self.tableView_2.setModel(model)
            #self.tableView_2.resize(200, 100)
            self.tableView_2.show()





