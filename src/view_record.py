from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import menu
import postgres_connect
import postgres_local
import config
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
import prompt_dialog
import numpy as np
import find_patient


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


class ViewRecord(QMainWindow):
    def __init__(self, uid, current_user, role, record):
        super().__init__()
        self.id = uid
        self.current_user = current_user
        self.role = role
        self.record = record
        var = os.path.dirname(os.path.abspath(__file__)) + "/view_record.ui"
        uic.loadUi(var, self)
        self.display()
        self.pushButton.clicked.connect(self.back_to_find_patient)
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

    def back_to_find_patient(self):
        # global backToFindPatient
        # backToFindPatient = find_patient.FindPatient(self.id, self.current_user, self.role)
        # backToFindPatient.show()
        self.close()

    def display(self):
        print(self.id, self.current_user, self.role)
        print(self.record, type(self.record))
        self.record = self.record.iloc[:-2]
        record_cols = ['patient_id', 'doctor_id', 'record_id', 'last_modified', 'content']
        df = self.record.to_frame()
        df['Columns'] = record_cols
        df = df.iloc[:, :-1].assign(Columns=df['Columns'])
        df.iloc[:, [0, 1]] = df.iloc[:, [1, 0]].values
        df.columns.values[0] = 'Columns'
        df.columns.values[1] = 'Values'
        model = pandasModel(df)
        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.show()


# 69824438

