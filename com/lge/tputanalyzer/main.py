import file_parser
import graph_manager
import tput_manager

mFileParser = file_parser.FileParser()
mGraphManager = graph_manager.GraphManager()
mThroughputManager = tput_manager.TputManager()

mRawData = mFileParser.getDataFrameFromFile('D:/Utils_for_adb/LG-F600L_V29d_20170424_032245_Asia_Seoul.csv')
mRawData.plot()
mMeasurementData = mThroughputManager.addThroughputColumn(mRawData)
mMeasurementData = mThroughputManager.addAvgCpuClockColumn(mMeasurementData)
mMeasurementData = mThroughputManager.addRealTimeColumn(mMeasurementData)

mGroupedDataList = mThroughputManager.groupMeasurementData(mMeasurementData)
mThroughputResult = mThroughputManager.makeThroughputResult(mGroupedDataList)

# print(mMeasurementData)
print(mThroughputResult)

mGraphManager.create_bar_graph(mThroughputResult.Throughput, mThroughputResult.CallCount)
mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData.Temperature)
