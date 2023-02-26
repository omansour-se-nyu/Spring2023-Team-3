from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class FindPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('find_patient.ui', self)