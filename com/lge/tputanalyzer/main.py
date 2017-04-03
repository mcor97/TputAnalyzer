import file_parser
import graph_manager
import tput_manager

fp = file_parser.FileParser()
graphManager = graph_manager.GraphManager()
tputManager = tput_manager.TputManager()

tputManager.create_summary_info_frame()
rawDataFrame = fp.get_dataframe_from_file('C:/1490929091716_70_47.csv')
tputDataFrame = tputManager.add_tput_column(rawDataFrame)

summaryInfoList = tputManager.make_summary_info_list(tputDataFrame)
summaryInfoDataFrame = tputManager.make_sumary_info(summaryInfoList)

print(summaryInfoDataFrame)

graphManager.create_bar_graph(summaryInfoDataFrame.Throughput, summaryInfoDataFrame.CallCount)
graphManager.create_line_graph(tputDataFrame, tputDataFrame.Time, tputDataFrame.Throughput, tputDataFrame.Time, tputDataFrame.Temperature)
