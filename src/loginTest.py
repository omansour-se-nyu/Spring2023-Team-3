import unittest
import sys
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from src import login
from PyQt5.QtWidgets import QApplication
from src.postgres_connect import PostgresHandler


app = QApplication(sys.argv)
class MyTestCase(unittest.TestCase):
    def setUp(self):
        #Create the GUI
        postgresDB = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)',
                                     'MentCare')
        self.form = login.LoginPage(postgresDB)
    #login
    def test_something(self):
        self.form.lineEdit.setText("Doctor")
        self.form.lineEdit_2.setText("$2b$12$va3j1iJSyC10hj7J34.HMeb4bdjCqAiupAaHwYHA6hzN9c.tWZ6wi")

        #test_defaults
        self.assertEqual(self.form.label.text(), "Welcome to Mentcare!")
        self.assertEqual(self.form.lineEdit.text(), "Doctor")


        #click login button without click the role
        QTest.mouseClick(self.form.pushButton_2, Qt.LeftButton)
        self.assertEqual(self.form.login(),False)

        #Click the role
        QTest.mouseClick(self.form.radioButton, Qt.LeftButton)
        self.assertEqual(self.form.login(), True)

        #insert the wrong password
        self.form.lineEdit.setText("Doctor")
        self.form.lineEdit_2.setText("123")
        QTest.mouseClick(self.form.radioButton, Qt.LeftButton)
        self.assertEqual(self.form.login(), False)


        #choose admin
        self.assertEqual(self.form.roleSelection(), "Medical Staff")
        QTest.mouseClick(self.form.radioButton2, Qt.LeftButton)
        self.assertEqual(self.form.roleSelection(),"Admin")


        #test register not realized
        # self.form.lineEdit.setText("Doctor")
        # self.form.lineEdit_2.setText("123")
        # QTest.mouseClick(self.form.pushButton, Qt.LeftButton)
        # self.form.lineEdit.setText("Doctor")
        # self.form.lineEdit_2.setText("123")
        # QTest.mouseClick(self.form.radioButton, Qt.LeftButton)
        # self.assertEqual(self.form.login(), True)


if __name__ == '__main__':
    unittest.main()

