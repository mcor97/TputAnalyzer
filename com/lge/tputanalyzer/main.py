import file_parser
import graph_manager
import tput_manager

mFileParser = file_parser.FileParser()
mGraphManager = graph_manager.GraphManager()
mThroughputManager = tput_manager.TputManager()

mRawData = mFileParser.getDataFrameFromFile('C:/1490929091716_70_47.csv')
mMeasurementData = mThroughputManager.addThroughputColumn(mRawData)
mMeasurementData = mThroughputManager.addAvgCpuClockColumn(mMeasurementData)
mMeasurementData = mThroughputManager.addRealTimeColumn(mMeasurementData)

mGroupedDataList = mThroughputManager.groupMeasurementData(mMeasurementData)
mThroughputResult = mThroughputManager.makeThroughputResult(mGroupedDataList)

##print(mMeasurementData)
print(mThroughputResult)

mGraphManager.create_bar_graph(mThroughputResult.Throughput, mThroughputResult.CallCount)
mGraphManager.create_line_graph(mMeasurementData, mMeasurementData.Time, mMeasurementData.Throughput, mMeasurementData.Time, mMeasurementData.Temperature)
