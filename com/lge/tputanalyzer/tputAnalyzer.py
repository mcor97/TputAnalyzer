import ui_holder
import file_parser
import graph_manager
import tput_manager
from PyQt5.QtWidgets import *
import sys
import pandas as pd
import numpy

class TputAnalyzer:
    def __init__(self):
        self.mFileParser = file_parser.FileParser()
        self.mGraphManager = graph_manager.GraphManager()
        self.mThroughputManager = tput_manager.TputManager()
        self.myApp = QApplication(sys.argv)
        self.mUiHolder = ui_holder.UiHolder(self.myApp)

    def create_dialog(self):
        self.mUiHolder.show()
        self.myApp.exec_()

if __name__ == "__main__":
    mTputAnalyzer = TputAnalyzer()
    # mTputAnalyzer.create_dialog()

    # mFileName = mTputAnalyzer.mUiHolder.getSeldectedFileName()
    # print(mFileName)
    # mFileName = 'D:/Utils_for_adb/LG-F600L_V29d_20170426_033825_Asia_Seoul.csv'
    # mFileName = 'D:/Utils_for_adb/LG-F600L_V29d_20170424_032245_Asia_Seoul.csv'
    mFileName = 'D:/Utils_for_adb/LGM-V300L_V07t_20170428_045919_Asia_Seoul_GSO_ON_C10.csv'
    mRawData = mTputAnalyzer.mFileParser.getDataFrameFromFile(mFileName)
    # print(mRawData)

    # Remove garbage column
    # print(mRawData.shape), shape[0] means the count of row and shape[1] measn the count of column.
    # mRawData = mRawData.drop(['Unnamed: '.__str__() + (mRawData.shape[1]-1).__str__()], axis=1)

    # mMeasurementData = mTputAnalyzer.mThroughputManager.addDlTputColumn(mRawData)
    mMeasurementData = mTputAnalyzer.mThroughputManager.addThroughputColumn(mRawData, 'UL')
    mMeasurementData = mTputAnalyzer.mThroughputManager.addAvgCpuClockColumn(mMeasurementData)
    mMeasurementData = mTputAnalyzer.mThroughputManager.addRealTimeColumn(mMeasurementData)
    # print(mMeasurementData)

    mGroupedDataList = mTputAnalyzer.mThroughputManager.groupMeasurementData(mMeasurementData)
    # print('--------------------')
    # print(mGroupedDataList[0])
    # print(mGroupedDataList[1])
    mThroughputResult = mTputAnalyzer.mThroughputManager.makeThroughputResult(mGroupedDataList, 'UL')
    # print(mThroughputResult)

    mTputAnalyzer.mGraphManager.create_bar_graph(mThroughputResult.Throughput, mThroughputResult.CallCount)
    # mTputAnalyzer.mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData.Temperature)
    mTputAnalyzer.mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData['CPU_Usage(%)'])

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