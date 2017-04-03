import time
import file_parser
import graph
import tput_calculator
import pandas

fp = file_parser.FileParser()
graph = graph.Graph()
tputCal = tput_calculator.TputCalculator()
rawData = fp.get_dataframe_from_file('C:/1490929091716_70_47.csv')

print("call count max : ", rawData.max()['CallCount'])

tputData = tputCal.add_tput_column(rawData)

tputData.assign(sum=tputData['ReceivedBytes'] + tputData['SentBytes'])

summary_info = pandas.DataFrame(columns = ('CallCount', 'StartTime', 'EndTime', 'Throughput', 'Temperature_Min', 'Temperature_Avg','Temperature_Max'))

call_count_list = []

for j in range(0, rawData.max()['CallCount']):
    call_count_list.append(rawData[(rawData.CallCount == (j+1)) & (rawData.ReceivedBytes > 1000)])
    print("list len : ", len(call_count_list))

for k in range(0, len(call_count_list)):
    print("--------------------------------")
    received_bytes = call_count_list[k].sum()['ReceivedBytes']

    tail_value = call_count_list[k].tail(1)['Time'].values
    head_value = call_count_list[k].head(1)['Time'].values

    tmp1 = call_count_list[k].head(2)['Time'].values[1]
    tmp2 = call_count_list[k].head(2)['Time'].values[0]

    print("tmp1 : ", tmp1)
    print("tmp2 : ", tmp2)
    print("minus : ", tmp1-tmp2)
    print("tempature : ", call_count_list[k].mean()['Temperature'])

    elapsed_time = tail_value - head_value + (tmp1-tmp2)
    print(elapsed_time)
    average_tput = received_bytes / elapsed_time * 8 * 1024 / 1000 / 1000
    print("Average T-put : " , average_tput)

    summary_info.loc[k] = [k+1, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(call_count_list[k].head(1)['Time'].values/1000)), time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(call_count_list[k].tail(1)['Time'].values/1000)), average_tput, call_count_list[k].mean()['Temperature'], call_count_list[k].mean()['Temperature'], call_count_list[k].mean()['Temperature']]

print("--------------------------------")

print(summary_info)

graph.create_bar_graph(summary_info.Throughput, summary_info.CallCount)
graph.create_line_graph(tputData, tputData.Time, tputData.Throughput, tputData.Time, tputData.Temperature)
