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
        self.cpuClockTempGraphBtn.clicked.connect(self.__cpuClockTempGraphBtn_clicked__)
        self.resultListView = QListWidget(self)
        self.resultListView.setGeometry(30, 60, 980, 190)
        self.resultListView.itemActivated.connect(self.resultListDoubleClickedItem)
        self.resultListView.itemClicked.connect(self.resultListOneClickedItem)
        self.detailedListView = QListWidget(self)
        self.detailedListView.setGeometry(30, 290, 750, 600)
        self.detailedListView.itemClicked.connect(self.detailedListOneClickedItem)

        self.fileOpened = False
        self.viewIndex = -1

    def pushButtonClicked(self):
        print(self.lineEdit.text())

    def getDataFrameFromFile(self, file_path):
        self.data_frame = pd.read_csv(file_path)
        print(self.data_frame)
        return self.data_frame

    def makeData(self, rawData):
        self.mMeasurementData = self.mThroughputManager.convertFrequencyColumn(rawData)
        self.mMeasurementData = self.mThroughputManager.addThroughputColumn(rawData, rawData.Direction[0])
        #self.mMeasurementData = self.mThroughputManager.convertToKorTime(self.mMeasurementData)
        self.mMeasurementData = self.mThroughputManager.addRealTimeColumn(self.mMeasurementData)

        print(self.mMeasurementData)

        self.mGroupedDataList = self.mThroughputManager.groupMeasurementData(self.mMeasurementData)
        self.mThroughputResult = self.mThroughputManager.makeThroughputResult(self.mGroupedDataList, rawData.Direction[0])
        print(self.mThroughputResult)

    def printResult(self):
        #resultListView.clear()
        #detailedListView.clear()
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

        self.resultListView.addItem("   - 평균 : " + str(meanThroughput) + " Mbps,   최대 : " + str(maxThroughput) + " Mbps,   최소 : " + str(minThroughput) + " Mbps")
        self.resultListView.addItem("   - 표준편차 : " + str(stdThroughput) + ",   분산 : " + str(varThroughput))

        self.detailedListView.addItem("======== 전체 평균 ========")
        item = QListWidgetItem("  - T-put : " + str(meanThroughput) + " Mbps\tCPU 온도 : " + str(meanTemperature))
        item.setBackground(QColor('blue'))
        item.setForeground(QColor('white'))
        self.detailedListView.addItem(item)
        self.detailedListView.addItem("")
        self.detailedListView.addItem("======= 회차별 평균 =======")
        num_bars = len(self.mThroughputResult.Throughput)
        cpuCount = 0
        for s in list(self.mMeasurementData):
            if "CPU_CUR_Freq" in s:
                cpuCount += 1
        print("this this: ", cpuCount)
        for i in range(1, num_bars + 1):
            print(self.mThroughputResult.AvgTemperature[i - 1])
            itemString = "<" + str(i) + " 회차>\n\tT-put : " + str(numpy.round(self.mThroughputResult.Throughput[i - 1], 1)) + " Mbps,\tCPU 온도 : " + str(numpy.round(self.mThroughputResult.AvgTemperature[i - 1], 2)) + "\tCPU 점유율(%) : " + str(numpy.round(self.mThroughputResult.AvgCpuOccupancy[i - 1], 2)) + "\n\t"
            for j in range(1, cpuCount + 1):
                maxCpu = 'AvgMaxCpuFreq' + str(j - 1)
                print(self.mThroughputResult[maxCpu][i - 1])
                itemString += "CPU" + str(j - 1) + "_Freq : " + str(numpy.round(self.mThroughputResult[maxCpu][i - 1],0)) + "KHz\t"
            item = QListWidgetItem(itemString)
            if (self.mThroughputResult.Throughput[i - 1] < meanThroughput):
                item.setBackground(QColor('yellow'))
            if (self.mThroughputResult.Throughput[i - 1] == minThroughput):
                item.setBackground(QColor('red'))
            self.detailedListView.addItem(item)

    def resultListOneClickedItem(self, item):
        self.viewIndex = -1
        print("one clicked")
        print(item.text())
        index = self.resultListView.currentRow()
        print(index)

    def resultListDoubleClickedItem(self, item):
        self.viewIndex = -1
        print(item.text())
        print(self.resultListView.currentRow())
        index = self.resultListView.currentRow()
        print(index)

    def detailedListOneClickedItem(self, item):
        print("one clicked")
        print(item.text())
        index = self.detailedListView.currentRow()
        #item.setBackground(QColor('red'))
        print(index)
        if (index < 4):
            self.viewIndex = -1
        else:
            self.viewIndex = index - 4


    def __fileOpenBtn_clicked__(self):
        options = QFileDialog.Options()
        self.selectedFileName = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV (쉼표로 분리) (*.csv)", options=options)
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


    def __cpuClockTempGraphBtn_clicked__(self):
        #if (self.fileOpened == False) :
        self.showWarningDialog("먼저 CSV 파일을 선택하세요.      ")
        #else:
        #    self.mGraphManager.create_cpuclock_temperature_graph(self.mThroughputResult, self.mMeasurementData, self.mGroupedDataList, self.viewIndex)

    def showWarningDialog(self, text):
        QMessageBox.about(self, "Warning", text)

    def __close_myApp__(self):
        self.myApp.quit()
        self.close()


#if __name__ == "__main__":
    def test(self):
        print("test")
        # sTemperature = numpy.zeros(len(mMeasurementData.ix[:, 8]))
        # sCpuUsage = numpy.zeros(len(mMeasurementData.ix[:, 9]))
        # sThroughput = numpy.zeros(len(mMeasurementData.ix[:, 16]))
        # sReceivedBytes = numpy.zeros(len(mMeasurementData.ix[:, 6]))

        # for i in range(0, 17):
        #     sTemperature[i] = mMeasurementData.ix[:, 8][i]
        #     sCpuUsage[i] = mMeasurementData.ix[:, 9][i]
        #     sThroughput[i] = mMeasurementData.ix[:, 16][i]
        #     sReceivedBytes[i] = mMeasurementData.ix[:, 16][i]

        # temperatureDF = pd.DataFrame(sTemperature, columns=['Temperature'])
        # cpuUsageDF = pd.DataFrame(sCpuUsage, columns=['CPU Usage'])
        # throughputDF = pd.DataFrame(sThroughput, columns=['Throughput'])
        # receivedBytesDF = pd.DataFrame(sThroughput, columns=['ReceivedBytes'])
        # newOne = pd.concat([temperatureDF, cpuUsageDF, throughputDF, receivedBytesDF], axis=1)
        # newOne = pd.concat([cpuUsageDF, throughputDF], axis=1)

        # mTputAnalyzer.mGraphManager.create_pairplot_graph(newOne)
        # mTputAnalyzer.mGraphManager.create_kdeplot_graph(throughputDF)
        # mTputAnalyzer.mGraphManager.create_distplot_graph(throughputDF)
        # mTputAnalyzer.mGraphManager.create_boxplot_graph(mMeasurementData, 'Throughput')
        # print(mMeasurementData.ix[:, 9])
        # print(mMeasurementData.ix[:, 16])
        # print(mMeasurementData)
        # mTputAnalyzer.mGraphManager.create_lmplot_graph('CPU_Usage(%)', 'Throughput', mMeasurementData)
        # print(mRawData.ix[:,9])
        # print(mRawData.ix[:, 9].describe())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = TputAnalyzer()
    myWindow.show()
    app.exec_()