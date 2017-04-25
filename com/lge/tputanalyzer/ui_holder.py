# -*- coding: utf-8 -*-

import os, sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel

class UiHolder():
    def __init__(self):
        # Create an PyQT4 application object.
        self.myApp = QApplication(sys.argv)

        # Add menu bar, need to use QMainWindow().
        self.mWidget = QWidget()
        self.mWidget.setWindowTitle('TputAnalyzer !')
        self.mWidget.setAutoFillBackground(True)
        self.mWidget.setMinimumSize(200, 100)
        self.mWidget.setMaximumSize(300, 200)
        self.mWidget.resize(240, 150)

        # Add some requirement text
        self.mLabel1 = QLabel(self.mWidget)
        self.mLabel1.setText("CSV 파일만 지원합니다.")
        self.mLabel1.move(10, 10)

        # Add e-mail address
        self.mLabel2 = QLabel(self.mWidget)
        self.mLabel2.setText("dom-data@lge.com")
        self.mLabel2.move(10, 30)

        # Create a button in the window
        self.mFileButton = QPushButton('File Open', self.mWidget)
        self.mFileButton.move(140, 110)
        self.mFileButton.clicked.connect(self.filebutton_clicked)

    def filebutton_clicked(self):
        self.filename = QFileDialog.getOpenFileName(self.mWidget, 'File Open', '/')
        self.myApp.quit()
        self.mWidget.close()

    def startFileDialog(self):
        self.mWidget.show()
        self.myApp.exec_()

    def getFileName(self):
        return self.filename[0]