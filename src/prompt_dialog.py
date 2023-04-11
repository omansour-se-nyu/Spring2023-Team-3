from PyQt5.QtWidgets import QDialog, QApplication
import os
from PyQt5 import uic


class Prompt(QDialog):
    def __init__(self, text):
        super().__init__()
        var = os.path.dirname(os.path.abspath(__file__)) + "/prompt_dialog.ui"
        uic.loadUi(var, self)
        self.text = text
        self.label.setText(self.text)
        self.pushButton.clicked.connect(self.creat_patient_success)

    def creat_patient_success(self):
        self.close()


