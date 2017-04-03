import numpy
import pandas
import time

class TputManager :
    summaryInfoFrame = pandas.DataFrame()
    summaryInfoList = []

    def add_tput_column(self, data):
        tput = numpy.zeros(len(data.Time))

        for i in numpy.arange(1, len(data.Time)):
            tput[i] = ((data.ReceivedBytes[i]) / (data.Time[i] - data.Time[i - 1])) * 8 * 1024 / 1000 / 1000

        data['Throughput'] = tput
        return data

    def create_summary_info_frame(self):
        TputManager.summaryInfoFrame = pandas.DataFrame(columns = ('CallCount', 'StartTime', 'EndTime', 'Throughput', 'Temperature_Min', 'Temperature_Avg','Temperature_Max'))

    def get_summary_info_frame(self):
        return TputManager.summaryInfoFrame

    def make_summary_info_list(self, dataFrame):
        
        callCount = dataFrame.max()['CallCount']
        print("call count max : ", callCount)

        for j in range(0, callCount):
            newDataFrame = dataFrame[dataFrame.CallCount == (j + 1)]

            length = len(newDataFrame.Throughput)
            for m in numpy.arange(0, length - 2):
                if newDataFrame.iloc[0]['Throughput'] < 1 and newDataFrame.iloc[1]['Throughput'] < 1:
                    newDataFrame = newDataFrame.drop(newDataFrame.index[0])

            for m in numpy.arange(0, length - 2):
                if newDataFrame.iloc[-1]['Throughput'] < 1 and newDataFrame.iloc[-2]['Throughput'] < 1:
                    newDataFrame = newDataFrame.drop(newDataFrame.index[-1])

            ##graph.create_line_graph(newDataFrame, newDataFrame.Time, newDataFrame.Throughput, newDataFrame.Time, newDataFrame.Temperature)
            ##print(newDataFrame['Throughput'])
            TputManager.summaryInfoList.append(newDataFrame)
        return TputManager.summaryInfoList

    def make_sumary_info(self, summaryInfoList):

        for k in range(0, len(summaryInfoList)):
            print("--------------------------------")
            receivedBytes = summaryInfoList[k].sum()['ReceivedBytes']

            startTime = summaryInfoList[k].head(1)['Time'].values
            endTime = summaryInfoList[k].tail(1)['Time'].values

            print("tempature : ", summaryInfoList[k].mean()['Temperature'])

            elapsedTime = endTime - startTime
            print(elapsedTime)
            averageTput = receivedBytes / elapsedTime * 8 * 1024 / 1000 / 1000
            print("Average T-put : ", averageTput)

            TputManager.summaryInfoFrame.loc[k] = [k + 1, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(
                summaryInfoList[k].head(1)['Time'].values / 1000)), time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(
                summaryInfoList[k].tail(1)['Time'].values / 1000)),
                                       averageTput, summaryInfoList[k].mean()['Temperature'],
                                       summaryInfoList[k].mean()['Temperature'],
                                       summaryInfoList[k].mean()['Temperature']]
        return TputManager.summaryInfoFrame
