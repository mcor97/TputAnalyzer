import ui_holder
import file_parser
import graph_manager
import tput_manager
from PyQt5.QtWidgets import *
import sys

if __name__ == "__main__":
    mFileParser = file_parser.FileParser()
    mGraphManager = graph_manager.GraphManager()
    mThroughputManager = tput_manager.TputManager()

    myApp = QApplication(sys.argv)
    mUiHolder = ui_holder.UiHolder(myApp)
    mUiHolder.show()
    myApp.exec_()

    mFileName = mUiHolder.getSeldectedFileName()
    print(mFileName)

    mRawData = mFileParser.getDataFrameFromFile(mFileName)
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