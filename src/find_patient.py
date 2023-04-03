from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import menu
import postgres_connect
import config
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

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
    def __init__(self, current_user, role):
        super().__init__()
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
        backToMenu = menu.MainMenu(self.current_user, self.role)
        backToMenu.show()
        self.close()

    def search(self):
        self.patient = self.lineEdit.text()
        self.patientid = "'%s'" % self.patient
        cols = ['id', 'name', 'gender', 'age', 'ssn', 'phone', 'email', 'address']
        self.df = self.postgresDB.getRow('select * from public.patients where id = ' + self.patientid + ' or patients.name = ' + self.patientid, cols)

        for index, row in self.df.iterrows():
            self.patientid = "'%s'" % row['id']
            break

        cols = ['id', 'record_id', 'last_modified', 'content']
        record = self.postgresDB.getRow('select * from public.records where id = ' + self.patientid, cols)
        #comb = record.append(self.df, ignore_index=True)

        model = pandasModel(self.df)
        self.tableView.setModel(model)
        self.tableView.resize(200, 100)
        self.tableView.show()

        model = pandasModel(record)
        self.tableView_2.setModel(model)
        self.tableView_2.resize(200, 100)
        self.tableView_2.show()



