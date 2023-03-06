from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class RegisterPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('register_patient.ui', self)