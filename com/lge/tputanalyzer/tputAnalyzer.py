#-*- encoding: utf-8 -*-
import file_parser
import graph_manager
import tput_manager
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import sys
import pandas as pd
import numpy
import time

form_class = uic.loadUiType("Dialog_TputAnalyzer.ui")[0]

DBG = False
#DBG = True

class TputAnalyzer(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.myApp = mQApplication

        self.mFileParser = file_parser.FileParser()
        self.mGraphManager = graph_manager.GraphManager()
        self.mThroughputManager = tput_manager.TputManager()
        self.fileOpenBtn.clicked.connect(self.__fileOpenBtn_clicked__)
        self.summaryGraphBtn.clicked.connect(self.__summaryGraphBtn_clicked__)
        self.cpuTempUsageGraphBtn.clicked.connect(self.__cpuTempUsageGraphBtn_clicked__)
        self.cpuClockGraphBtn.clicked.connect(self.__cpuClockGraphBtn_clicked__)
        self.resultListView = QListWidget(self)
        self.resultListView.setGeometry(30, 60, 980, 220)
        self.resultListView.itemClicked.connect(self.resultListOneClickedItem)
        self.detailedListView = QListWidget(self)
        self.detailedListView.setGeometry(30, 320, 750, 600)
        self.detailedListView.itemClicked.connect(self.detailedListOneClickedItem)

        self.fileOpened = False
        self.viewIndex = -1

    def pushButtonClicked(self):
        print(self.lineEdit.text())

    def getDataFrameFromFile(self, file_path):
        self.data_frame = pd.read_csv(file_path)
        if(DBG):
            print(self.data_frame)
        return self.data_frame

    def makeData(self, rawData):
        self.mMeasurementData = self.mThroughputManager.convertFrequencyColumn(rawData)
        self.mMeasurementData = self.mThroughputManager.addThroughputColumn(rawData, rawData.Direction[0])
        #self.mMeasurementData = self.mThroughputManager.convertToKorTime(self.mMeasurementData)
        self.mMeasurementData = self.mThroughputManager.addRealTimeColumn(self.mMeasurementData)

        if (DBG):
            print(self.mMeasurementData)

        self.mGroupedDataList = self.mThroughputManager.groupMeasurementData(self.mMeasurementData)
        self.mThroughputResult = self.mThroughputManager.makeThroughputResult(self.mGroupedDataList, rawData.Direction[0])
        if (DBG):
            print(self.mThroughputResult)

    def printResult(self):
        self.resultListView.clear()
        self.detailedListView.clear()
        if (self.mMeasurementData.Direction[0] == 'UL'):
            self.resultListView.addItem("< Uplink Throughput Result >")
        else :
            self.resultListView.addItem("< Downlink Throughput Result >")

        testAppName = self.mMeasurementData.PackageName[0]
        if (testAppName.find("xcal.mobile") != -1):
            testAppName = "SAT (" + self.mMeasurementData.PackageName[0] + ")"
        elif (testAppName.find("benchbee") != -1):
            testAppName = "BenchBee (" + self.mMeasurementData.PackageName[0] + ")"
        elif (testAppName.find("nia") != -1):
            testAppName = "NIA (" + self.mMeasurementData.PackageName[0] + ")"
        elif (testAppName.find("ftpcafe") != -1):
            testAppName = "FTP Cafe (" + self.mMeasurementData.PackageName[0] + ")"

        self.resultListView.addItem("   - 측정 앱 : " + testAppName)
        self.resultListView.addItem("   - 결과 파일 : " + self.selectedFileName[0])

        self.resultListView.addItem("< 측정 시간 >")
        self.resultListView.addItem("   - 시작 : " + self.mThroughputResult.iloc[0].StartTime)
        self.resultListView.addItem("   - 종료 : " + self.mThroughputResult.iloc[-1].EndTime)

        self.resultListView.addItem("< 측정 결과 >")

        # 평균
        meanThroughput = numpy.round(self.mThroughputResult.Throughput.mean(), 1)
        # 최대
        maxThroughput = numpy.round(self.mThroughputResult.Throughput.max(), 1)
        # 최소
        minThroughput = numpy.round(self.mThroughputResult.Throughput.min(), 1)
        # 표준편차
        stdThroughput = numpy.round(self.mThroughputResult.Throughput.std(), 1)
        # 분산
        varThroughput = numpy.round(self.mThroughputResult.Throughput.var(), 1)

        meanTemperature = numpy.round(self.mThroughputResult.AvgTemperature.mean(), 1)

        cpuCount = 0
        for s in list(self.mMeasurementData):
            if "CPU_CUR_Freq" in s:
                cpuCount += 1

        self.resultListView.addItem("   - T-put :\t평균 : " + str(meanThroughput) + " Mbps\t최대 : " + str(maxThroughput) + " Mbps\t최소 : " + str(minThroughput) + " Mbps\t표준편차 : " + str(stdThroughput))
        startItemString = "   - CPU Clock (시작) : "
        endItemString = "   - CPU Clock (종료)  :"

        for j in range(1, cpuCount + 1):
            maxCpu = 'CPU_MAX_Freq' + str(j - 1)
            startItemString += "CPU" + str(j - 1) + "_Freq : " + str(numpy.round(self.mMeasurementData.head(1)[maxCpu].values, 0)) + "MHz\t"
            endItemString += "CPU" + str(j - 1) + "_Freq : " + str(numpy.round(self.mMeasurementData.tail(1)[maxCpu].values, 0)) + "MHz\t"
        self.resultListView.addItem(startItemString)
        self.resultListView.addItem(endItemString)

        self.resultListView.addItem("   - CPU 온도 (시작) : " + str(self.mMeasurementData.head(1).Temperature.values) + "\n   - CPU 온도 (종료) : " + str(self.mMeasurementData.tail(1).Temperature.values))

        num_bars = len(self.mThroughputResult.Throughput)


        for i in range(1, num_bars + 1):
            itemString = "<" + str(i) + " 회차>"
            if (self.mThroughputResult.Throughput[i - 1] == maxThroughput):
                itemString += "\t<최대>"
            elif (self.mThroughputResult.Throughput[i - 1] == minThroughput):
                itemString += "\t<최소>"
            elif (self.mThroughputResult.Throughput[i - 1] < meanThroughput):
                itemString += "\t<평균 이하>"
            itemString += "\n\tT-put : " + str(numpy.round(self.mThroughputResult.Throughput[i - 1], 1)) + " Mbps,\tCPU 온도 : " + str(numpy.round(self.mThroughputResult.AvgTemperature[i - 1], 2)) + "\tCPU 점유율(%) : " + str(numpy.round(self.mThroughputResult.AvgCpuOccupancy[i - 1], 2)) + "\n\t"
            for j in range(1, cpuCount + 1):
                maxCpu = 'AvgMaxCpuFreq' + str(j - 1)
                itemString += "CPU" + str(j - 1) + "_Freq : " + str(numpy.round(self.mThroughputResult[maxCpu][i - 1],0)) + "MHz\t"
            item = QListWidgetItem(itemString)
            if (self.mThroughputResult.Throughput[i - 1] < meanThroughput):
                item.setBackground(QColor('yellow'))
            if (self.mThroughputResult.Throughput[i - 1] == minThroughput):
                item.setBackground(QColor('red'))
            if (self.mThroughputResult.Throughput[i - 1] == maxThroughput):
                item.setBackground(QColor('green'))
            self.detailedListView.addItem(item)

    def resultListOneClickedItem(self, item):
        self.viewIndex = -1
        index = self.resultListView.currentRow()


    def detailedListOneClickedItem(self, item):
        self.viewIndex = self.detailedListView.currentRow()


    def __fileOpenBtn_clicked__(self):

        options = QFileDialog.Options()
        self.selectedFileName = QFileDialog.getOpenFileName(self,"CSV File Open", "","CSV (쉼표로 분리) (*.csv)", options=options)
        print(self.selectedFileName[0])
        if (self.selectedFileName[0]):
            self.mRawData = self.getDataFrameFromFile(self.selectedFileName[0])
            self.makeData(self.mRawData)
            self.printResult()
            self.fileOpened = True

    def __summaryGraphBtn_clicked__(self):
        if (self.fileOpened == False) :
            self.showWarningDialog("먼저 CSV 파일을 선택하세요.      ")
        else:
            self.mGraphManager.create_summary_graph(self.mThroughputResult, self.mMeasurementData, self.mGroupedDataList, self.viewIndex)

    def __cpuTempUsageGraphBtn_clicked__(self):
        if (self.fileOpened == False) :
            self.showWarningDialog("먼저 CSV 파일을 선택하세요.      ")
        else:
            self.mGraphManager.create_temperature_cpuusage_graph(self.mThroughputResult, self.mMeasurementData, self.mGroupedDataList, self.viewIndex)


    def __cpuClockGraphBtn_clicked__(self):
        if (self.fileOpened == False) :
            self.showWarningDialog("먼저 CSV 파일을 선택하세요.      ")
        else:
            self.mGraphManager.create_cpuclock_graph(self.mThroughputResult, self.mMeasurementData, self.mGroupedDataList, self.viewIndex)


    def showWarningDialog(self, text):
        QMessageBox.about(self, "Warning", text)

    def __close_myApp__(self):
        self.myApp.quit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = TputAnalyzer()
    myWindow.show()
    app.exec_()