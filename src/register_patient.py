import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class RegisterPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        var = os.path.dirname(os.path.abspath(__file__)) + "/register_patient.ui"
        uic.loadUi(var, self)