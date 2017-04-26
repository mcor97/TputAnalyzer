# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("Dialog_TputAnalyzer.ui")[0]

class UiHolder(QMainWindow, form_class):
    def __init__(self, mQApplication):
        super().__init__()
        self.setupUi(self)
        self.myApp = mQApplication
        self.selectFileButton.clicked.connect(self.__selectedBtn_clicked__)

    def __selectedBtn_clicked__(self):
        self.selectedFileName = QFileDialog.getOpenFileName(self)
        self.__close_myApp__()

    def __close_myApp__(self):
        self.myApp.quit()
        self.close()

    def getSeldectedFileName(self):
        return self.selectedFileName[0]