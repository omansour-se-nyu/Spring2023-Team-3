import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from src.menu import MainMenu
from src.find_patient import FindPatient
from src.postgres_connect import PostgresHandler
from src.create_account import CreateAccount

from src.login import LoginPage

def test_LoginPage():
    postgresDB = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    login_page = LoginPage(postgresDB)
    assert login_page.is_valid_user()==True

