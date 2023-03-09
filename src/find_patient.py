from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import menu
import postgres_connect
import config

class FindPatient(QMainWindow):
    def __init__(self, current_user, role):
        super().__init__()
        self.current_user = current_user
        self.role = role
        uic.loadUi('find_patient.ui', self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.back_to_menu)
        self.postgresDB = postgres_connect.PostgresHandler(config.remote_postgre["url"],
                                                           config.remote_postgre["port"],
                                                           config.remote_postgre["username"],
                                                           config.remote_postgre["passwd"],
                                                           config.remote_postgre["database"])

    def search(self):
        pass

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.current_user, self.role)
        backToMenu.show()
        self.close()

    def search(self):
        patient = self.lineEdit.text()
        df = None
        if patient.isnumeric():
            df = self.postgresDB.getQuery('select * from patients where id==' + patient)
        else:
            df = self.postgresDB.getQuery('select * from patients where name==' + patient)
        print(df)


