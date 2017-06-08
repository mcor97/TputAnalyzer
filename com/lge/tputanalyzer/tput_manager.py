import numpy
import pandas as pd
import time

class TputManager :

    def addThroughputColumn(self, dataFrame, direction):
        throughput = numpy.zeros(len(dataFrame.Time))

        for i in numpy.arange(1, len(dataFrame.Time)):
            if direction == 'DL':
                if (dataFrame.ReceivedBytes[i] != 0):
                    throughput[i] = ((dataFrame.ReceivedBytes[i]) / (dataFrame.Time[i] - dataFrame.Time[i-1])) * 8 * 1024 / 1000 / 1000
                else:
                    throughput[i] = 0
            elif direction == 'UL':
                if(dataFrame.SentBytes[i] != 0):
                    throughput[i] = ((dataFrame.SentBytes[i]) / (dataFrame.Time[i] - dataFrame.Time[i - 1])) * 8 * 1024 / 1000 / 1000
                else:
                    throughput[i] = 0

        dataFrame['Throughput'] = throughput
        return dataFrame

    def addRealTimeColumn(self, dataFrame):
        data = [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(dataFrame.Time[i] / 1000)) for i in range(len(dataFrame.Time))]
        realTime = pd.Series(data, name='RealTime')
        dataFrame = dataFrame.join(realTime)
        return dataFrame

    def groupMeasurementData(self, dataFrame):
        groupedDataList = []

        callCount = dataFrame.max()['CallCnt']
        print("call count max : ", callCount)

        for j in range(0, callCount):
            # groupedData = dataFrame[dataFrame.CallCount == (j + 1)]
            groupedData = dataFrame[dataFrame.CallCnt == (j + 1)]

            length = len(groupedData.Throughput)
            for m in numpy.arange(0, length - 2):
                if groupedData.iloc[0]['Throughput'] < 1 and groupedData.iloc[1]['Throughput'] < 1:
                    groupedData = groupedData.drop(groupedData.index[0])

            for m in numpy.arange(0, length - 2):
                if groupedData.iloc[-1]['Throughput'] < 1 and groupedData.iloc[-2]['Throughput'] < 1:
                    groupedData = groupedData.drop(groupedData.index[-1])

            groupedDataList.append(groupedData)
        return groupedDataList


    def makeThroughputResult(self, groupedList, direction):

        throughputResult = pd.DataFrame(columns=(
            'CallCount', 'StartTime', 'EndTime', 'Throughput', 'MinTemperature', 'AvgTemperature', 'MaxTemperature',
            "MinCpuOccupancy", "AvgCpuOccupancy", "MaxCpuOccupancy"))

        for k in range(0, len(groupedList)):
            print("--------------------------------")

            ## Time conversion
            startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(groupedList[k].head(1)['Time'].values / 1000))
            endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(groupedList[k].tail(1)['Time'].values / 1000))

            ## Throughput
            elapsedTime = groupedList[k].tail(1)['Time'].values - groupedList[k].head(1)['Time'].values

            if direction == 'DL':
                receivedBytes = groupedList[k].sum()['ReceivedBytes']
                througthput = numpy.round(receivedBytes / elapsedTime * 8 * 1024 / 1000 / 1000, 1)
            elif direction == 'UL':
                sentytes = groupedList[k].sum()['SentBytes']
                througthput = numpy.round(sentytes / elapsedTime * 8 * 1024 / 1000 / 1000, 1)

            ## Temperature
            minTemperature = groupedList[k].min()['Temperature']
            maxTemperature = groupedList[k].max()['Temperature']
            avgTemperature = groupedList[k].mean()['Temperature']

            ## CPU Occupancy
            minCpuOccupancy = groupedList[k].min()['CPU_Usage(%)']
            maxCpuOccupancy = groupedList[k].max()['CPU_Usage(%)']
            avgCpuOccupancy = groupedList[k].mean()['CPU_Usage(%)']

            throughputResult.loc[k] = [k + 1, startTime, endTime, througthput, minTemperature, avgTemperature, maxTemperature,
                                       minCpuOccupancy, avgCpuOccupancy, maxCpuOccupancy]
        return throughputResult
