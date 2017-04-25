# -*- coding: utf-8 -*-

import os, sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

class UiHolder():
    def __init__(self):
        # Create an PyQT4 application object.
        self.myApp = QApplication(sys.argv)
        # Add menu bar, need to use QMainWindow().
        self.w = QWidget()
        self.w.setWindowTitle('TputAnalyzer !')
        self.w.setAutoFillBackground(True)
        self.w.setMinimumSize(200, 100)
        self.w.setMaximumSize(300, 200)
        self.w.resize(240, 150)

        # Create a button in the window
        self.mFileButton = QPushButton('File Open', self.w)
        self.mFileButton.move(140, 110)
        self.mFileButton.clicked.connect(self.filebutton_clicked)

    def filebutton_clicked(self):
        self.filename = QFileDialog.getOpenFileName(self.w, 'File Open', '/')
        self.myApp.quit()
        self.w.close()

    def startFileDialog(self):
        self.w.show()
        self.myApp.exec_()

    def getFileName(self):
        return self.filename[0]