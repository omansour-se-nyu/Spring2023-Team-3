from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class CreateAccount(QMainWindow):
    def __init__(self, postgresDB):
        super().__init__()
        uic.loadUi('create_account.ui', self)
        self.postgresDB = postgresDB
