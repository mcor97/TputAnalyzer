import ui_holder
import file_parser
import graph_manager
import tput_manager
from PyQt5.QtWidgets import *
import sys

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
    mTputAnalyzer.create_dialog()

    mFileName = mTputAnalyzer.mUiHolder.getSeldectedFileName()
    print(mFileName)

    mRawData = mTputAnalyzer.mFileParser.getDataFrameFromFile(mFileName)
    mRawData.plot()
    mMeasurementData = mTputAnalyzer.mThroughputManager.addThroughputColumn(mRawData)
    mMeasurementData = mTputAnalyzer.mThroughputManager.addAvgCpuClockColumn(mMeasurementData)
    mMeasurementData = mTputAnalyzer.mThroughputManager.addRealTimeColumn(mMeasurementData)

    # print(mMeasurementData)
    mGroupedDataList = mTputAnalyzer.mThroughputManager.groupMeasurementData(mMeasurementData)
    mThroughputResult = mTputAnalyzer.mThroughputManager.makeThroughputResult(mGroupedDataList)

    # print(mThroughputResult)
    mTputAnalyzer.mGraphManager.create_bar_graph(mThroughputResult.Throughput, mThroughputResult.CallCount)
    mTputAnalyzer.mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData.Temperature)