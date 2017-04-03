import file_parser
import graph
import tput_calculator

fp = file_parser.FileParser()
graph = graph.Graph()
tputCalulator = tput_calculator.TputCalculator()

tputCalulator.create_summary_info_frame()
rawDataFrame = fp.get_dataframe_from_file('C:/1490929091716_70_47.csv')
tputDataFrame = tputCalulator.add_tput_column(rawDataFrame)

summaryInfoList = tputCalulator.make_summary_info_list(tputDataFrame)
summaryInfoDataFrame = tputCalulator.make_sumary_info(summaryInfoList)

print(summaryInfoDataFrame)

graph.create_bar_graph(summaryInfoDataFrame.Throughput, summaryInfoDataFrame.CallCount)
graph.create_line_graph(tputDataFrame, tputDataFrame.Time, tputDataFrame.Throughput, tputDataFrame.Time, tputDataFrame.Temperature)
