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
        self.resultListView.setGeometry(30, 60, 830, 190)
        self.detailedListView = QListWidget(self)
        self.detailedListView.setGeometry(30, 290, 600, 550)
        #self.detailedListView.doubleClicked.connect(self.doubleClickedItem)
        self.detailedListView.itemActivated.connect(self.doubleClickedItem)
        self.fileOpened = False

    def pushButtonClicked(self):
        print(self.lineEdit.text())

    def getDataFrameFromFile(self, file_path):
        self.data_frame = pd.read_csv(file_path)
        print(self.data_frame)
        return self.data_frame

    def makeData(self, rawData):
        self.mMeasurementData = self.mThroughputManager.addThroughputColumn(rawData, rawData.Direction[0])
        #self.mMeasurementData = self.mThroughputManager.convertToKorTime(self.mMeasurementData)
        self.mMeasurementData = self.mThroughputManager.addRealTimeColumn(self.mMeasurementData)

        print(self.mMeasurementData)

        self.mGroupedDataList = self.mThroughputManager.groupMeasurementData(self.mMeasurementData)
        self.mThroughputResult = self.mThroughputManager.makeThroughputResult(self.mGroupedDataList, rawData.Direction[0])
        print(self.mThroughputResult)

    def printResult(self):

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
        print(testAppName)

        self.resultListView.addItem("   - 측정 앱 : " + testAppName)
        self.resultListView.addItem("   - 결과 파일 : " + self.selectedFileName[0])

        self.resultListView.addItem("< 측정 시간 >")
        self.resultListView.addItem("   - 시작 : " + self.mThroughputResult.iloc[0].StartTime)
        self.resultListView.addItem("   - 종료 : " + self.mThroughputResult.iloc[-1].EndTime)

        self.resultListView.addItem("< 측정 결과 >")

        # 평균
        meanThroughput = self.mThroughputResult.Throughput.mean()
        # 최대
        maxThroughput = self.mThroughputResult.Throughput.max()
        # 최소
        minThroughput = self.mThroughputResult.Throughput.min()
        # 표준편차
        stdThroughput = self.mThroughputResult.Throughput.std()
        # 분산
        varThroughput = self.mThroughputResult.Throughput.var()

        print(varThroughput)
        self.resultListView.addItem("   - 평균 : " + str(meanThroughput) + " Mbps,   최대 : " + str(maxThroughput) + " Mbps,   최소 : " + str(minThroughput) + " Mbps")
        self.resultListView.addItem("   - 표준편차 : " + str(stdThroughput) + ",   분산 : " + str(varThroughput))
        print("abc")

        num_bars = len(self.mThroughputResult.Throughput)
        for i in range(1, num_bars + 1):
            print(self.mThroughputResult.AvgTemperature[i - 1])
            item = QListWidgetItem(" - " + str(i) + " 회차 T-put : " + str(numpy.round(self.mThroughputResult.Throughput[i-1],1))
                                   + " Mbps,  CPU 온도 : " + str(numpy.round(self.mThroughputResult.AvgTemperature[i-1],2))
                                   + " ,  CPU 점유율(%) : " + str(numpy.round(self.mThroughputResult.AvgCpuOccupancy[i - 1], 2)))
            if (self.mThroughputResult.Throughput[i - 1] < meanThroughput):
                item.setBackground(QColor('#fdc086'))
            self.detailedListView.addItem(item)
        print("abc")

    def doubleClickedItem(self, item):
        print(item.text())
        print(self.detailedListView.currentRow())
        index = self.detailedListView.currentRow()
        print(index)
        self.mGraphManager.create_grouped_graph(self.mGroupedDataList[index])
        #print(self.listWidget.currentItem().text())

        #theListWidget = self.sender()
        #currentItem = theListWidget.currentItem()
        #currentItemText = currentItem.text()
        #currentItem.setBackground(QtGui.QColor('red'))

    def __fileOpenBtn_clicked__(self):
        self.selectedFileName = QFileDialog.getOpenFileName(self)
        #print(self.selectedFileName[0])
        self.mRawData = self.getDataFrameFromFile(self.selectedFileName[0])
        #self.mFileName = 'C:/Company/0605/LGM-G600K_V10t_20170607_094951_Asia_Seoul.csv'
        #self.selectedFileName[0] = self.mFileName;
        #self.mRawData = self.getDataFrameFromFile(self.mFileName)

        self.makeData(self.mRawData)
        self.printResult()
        self.fileOpened = True

    def __summaryGraphBtn_clicked__(self):
        if (self.fileOpened) :
            self.mGraphManager.create_summary_graph(self.mThroughputResult, self.mMeasurementData)
        else:
            QMessageBox.about(self, "Warning", "먼저 CSV 파일을 선택하세요.      ")

    def __cpuTempUsageGraphBtn_clicked__(self):
        if (self.fileOpened) :
            self.mGraphManager.create_temperature_cpuusage_graph(self.mThroughputResult, self.mMeasurementData)
        else:
            QMessageBox.about(self, "Warning", "먼저 CSV 파일을 선택하세요.      ")


    def __cpuClockGraphBtn_clicked__(self):
        if (self.fileOpened) :
            self.mGraphManager.create_cpuclock_graph(self.mThroughputResult, self.mMeasurementData)
        else:
            QMessageBox.about(self, "Warning", "먼저 CSV 파일을 선택하세요.      ")


    def __cpuClockTempGraphBtn_clicked__(self):
        if (self.fileOpened) :
            self.mGraphManager.create_cpuclock_temperature_graph(self.mThroughputResult, self.mMeasurementData)
        else:
            QMessageBox.about(self, "Warning", "먼저 CSV 파일을 선택하세요.      ")


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