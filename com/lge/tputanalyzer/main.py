# -*- coding: utf-8 -*-

import file_parser
import graph_manager
import tput_manager
import os, sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

#Create window
myApp = QApplication(sys.argv) #Create an PyQT4 application object.
w = QWidget() #Add menubar, need to use QMainWindow().
w.setWindowTitle('Add FileDialog')
w.resize(300, 240)

#Create a button in the window
myButton1 = QPushButton('Open CSV File', w)
myButton1.move(20,80)

##Create file dialog
filename = QFileDialog.getOpenFileName(w, 'Open File', '/')
print(filename)

#Show the window and run the app
# w.show()
# myApp.exec_()

mFileParser = file_parser.FileParser()
mGraphManager = graph_manager.GraphManager()
mThroughputManager = tput_manager.TputManager()

# mRawData = mFileParser.getDataFrameFromFile('D:/Utils_for_adb/LG-F600L_V29d_20170424_032245_Asia_Seoul.csv')
mRawData = mFileParser.getDataFrameFromFile(filename[0])
mRawData.plot()
mMeasurementData = mThroughputManager.addThroughputColumn(mRawData)
mMeasurementData = mThroughputManager.addAvgCpuClockColumn(mMeasurementData)
mMeasurementData = mThroughputManager.addRealTimeColumn(mMeasurementData)

# print(mMeasurementData)
mGroupedDataList = mThroughputManager.groupMeasurementData(mMeasurementData)
mThroughputResult = mThroughputManager.makeThroughputResult(mGroupedDataList)

# print(mThroughputResult)

mGraphManager.create_bar_graph(mThroughputResult.Throughput, mThroughputResult.CallCount)
mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData.Temperature)
