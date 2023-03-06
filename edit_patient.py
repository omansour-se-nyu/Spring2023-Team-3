from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class EditPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('edit_patient.ui', self)