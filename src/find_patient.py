from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

import menu

class FindPatient(QMainWindow):
    def __init__(self, current_user, role):
        super().__init__()
        self.current_user = current_user
        self.role = role
        uic.loadUi('find_patient.ui', self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.back_to_menu)

    def search(self):
        pass

    def back_to_menu(self):
        global backToMenu
        backToMenu = menu.MainMenu(self.current_user, self.role)
        backToMenu.show()
        self.close()
=======

class FindPatient(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('find_patient.ui', self)

