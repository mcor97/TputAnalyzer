#-*- encoding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy

#DISPLAY_DETAIL_DATA = True
DISPLAY_DETAIL_DATA = False
DISPLAY_DELTA = 5


class GraphManager :

    def create_temperature_cpuusage_graph(self, throughputResult, measurementData, groupedList, index):
        if (index == -1):
            num_bars = len(measurementData.Time)
            alignValue = measurementData.Throughput.max() / measurementData.Temperature.max() / 2

            plt.figure(figsize=(19, 9))
            plt.subplot(211)
            plt.plot(measurementData.Time, measurementData.Throughput)
            plt.plot(measurementData.Time, measurementData.Temperature * alignValue)

            dontDisplayData = False
            for k in range(1, num_bars + 1):
                if (DISPLAY_DETAIL_DATA == False) :
                    if (k < num_bars + DISPLAY_DELTA and dontDisplayData == False and measurementData.Throughput[k - 1] != 0):
                        plt.text(measurementData.Time[k + DISPLAY_DELTA - 1],
                                 numpy.round(measurementData.Throughput[k + DISPLAY_DELTA - 1], 0),
                                 numpy.round(measurementData.Throughput[k + DISPLAY_DELTA - 1], 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(measurementData.Time[k + DISPLAY_DELTA - 1],
                                 numpy.round(measurementData.Temperature[k + DISPLAY_DELTA - 1], 0) * alignValue,
                                 numpy.round(measurementData.Temperature[k + DISPLAY_DELTA - 1], 0), ha='center', va='bottom',
                                 color='green', size=8)
                        dontDisplayData = True

                    if (measurementData.Throughput[k - 1] == 0):
                        dontDisplayData = False
                else :
                    if (k < num_bars and measurementData.Throughput[k - 1] != 0 and measurementData.Throughput[k - 1] < measurementData.Throughput.mean()):
                        if (k > 2) :
                            plt.text(measurementData.Time[k - 2],
                                     numpy.round(measurementData.Throughput[k - 2], 0),
                                     numpy.round(measurementData.Throughput[k - 2], 0), ha='center', va='bottom',
                                     color='blue', size=8)

                        plt.text(measurementData.Time[k - 1],
                                 numpy.round(measurementData.Throughput[k - 1], 0),
                                 numpy.round(measurementData.Throughput[k - 1], 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(measurementData.Time[k],
                                 numpy.round(measurementData.Throughput[k], 0),
                                 numpy.round(measurementData.Throughput[k], 0), ha='center', va='bottom',
                                 color='blue', size=8)

                    if (k == 1 or (k < num_bars and measurementData.Temperature[k - 1] != measurementData.Temperature[k])):
                        plt.text(measurementData.Time[k - 1],
                                 numpy.round(measurementData.Temperature[k - 1], 0) * alignValue,
                                 numpy.round(measurementData.Temperature[k - 1], 0), ha='center', va='bottom',
                                 color='green', size=8)
                        plt.text(measurementData.Time[k],
                                 numpy.round(measurementData.Temperature[k], 0) * alignValue,
                                 numpy.round(measurementData.Temperature[k], 0), ha='center', va='bottom',
                                 color='green', size=8)

            plt.title('Throughput - Temperature Graph', size=20)
            plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=10)
            plt.legend(['Throughput', 'Temperature'])
            plt.grid(True)

            plt.subplot(212)
            alignValue = measurementData.Throughput.max() / measurementData['CPU_Usage(%)'].max() / 2
            plt.plot(measurementData.Time, measurementData.Throughput)
            plt.plot(measurementData.Time, measurementData['CPU_Usage(%)'] * alignValue)

            dontDisplayData = False
            for k in range(1, num_bars + 1):
                if (DISPLAY_DETAIL_DATA == False) :
                    if (k < num_bars + DISPLAY_DELTA and dontDisplayData == False and measurementData.Throughput[k - 1] != 0):
                        plt.text(measurementData.Time[k + DISPLAY_DELTA - 1],
                                 numpy.round(measurementData.Throughput[k + DISPLAY_DELTA - 1], 0),
                                 numpy.round(measurementData.Throughput[k + DISPLAY_DELTA - 1], 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(measurementData.Time[k + DISPLAY_DELTA - 1],
                                 numpy.round(measurementData['CPU_Usage(%)'][k + DISPLAY_DELTA - 1], 0) * alignValue,
                                 numpy.round(measurementData['CPU_Usage(%)'][k + DISPLAY_DELTA - 1], 0), ha='center', va='bottom',
                                 color='green', size=8)
                        dontDisplayData = True

                    if (measurementData.Throughput[k - 1] == 0):
                        dontDisplayData = False
                else :
                    if (k < num_bars and measurementData.Throughput[k - 1] != 0 and measurementData.Throughput[k - 1] < measurementData.Throughput.mean()):
                        if (k > 2) :
                            plt.text(measurementData.Time[k - 2],
                                     numpy.round(measurementData.Throughput[k - 2], 0),
                                     numpy.round(measurementData.Throughput[k - 2], 0), ha='center', va='bottom',
                                     color='blue', size=8)

                        plt.text(measurementData.Time[k - 1],
                                 numpy.round(measurementData.Throughput[k - 1], 0),
                                 numpy.round(measurementData.Throughput[k - 1], 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(measurementData.Time[k],
                                 numpy.round(measurementData.Throughput[k], 0),
                                 numpy.round(measurementData.Throughput[k], 0), ha='center', va='bottom',
                                 color='blue', size=8)

                    if (k < num_bars and (measurementData['CPU_Usage(%)'][k - 1] == measurementData['CPU_Usage(%)'].max() or measurementData['CPU_Usage(%)'][k - 1] == measurementData['CPU_Usage(%)'].min())):
                        plt.text(measurementData.Time[k - 1],
                                 numpy.round(measurementData['CPU_Usage(%)'][k - 1], 0) * alignValue,
                                 numpy.round(measurementData['CPU_Usage(%)'][k - 1], 0), ha='center', va='bottom',
                                 color='green', size=8)

                    if (k == 1 or ((k % 10) == 0)):
                        plt.text(measurementData.Time[k - 1],
                                 numpy.round(measurementData['CPU_Usage(%)'][k - 1], 0) * alignValue,
                                 numpy.round(measurementData['CPU_Usage(%)'][k - 1], 0), ha='center', va='bottom',
                                 color='green', size=8)

            #plt.xlabel('time (ms)', size=10)
            plt.title('Throughput - CPU Usage Graph', size=20)
            plt.ylabel('Throughput (Mbps) / CPU Usage (%)', size=10)
            plt.legend(['Throughput', 'CPU Usage(%)'])
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        else:
            num_bars = len(groupedList[index].Time)
            alignValue = measurementData.Throughput.max() / measurementData.Temperature.max() / 2

            plt.figure(figsize=(19, 9))
            plt.subplot(211)
            plt.plot(groupedList[index].Time, groupedList[index].Throughput)
            plt.plot(groupedList[index].Time, groupedList[index].Temperature * alignValue)

            for k in range(1, num_bars + 1):
                if (DISPLAY_DETAIL_DATA == False) :
                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0),
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0), ha='center', va='bottom',
                             color='blue', size=8)
                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1].Temperature, 0) * alignValue,
                             numpy.round(groupedList[index].iloc[k - 1].Temperature, 0), ha='center', va='bottom',
                             color='green', size=8)

                else :
                    if (k < num_bars and groupedList[index].iloc[k-1].Throughput < groupedList[index].Throughput.mean()):
                        if (k > 2) :
                            plt.text(groupedList[index].iloc[k - 2].Time,
                                     numpy.round(groupedList[index].iloc[k - 2].Throughput, 0),
                                     numpy.round(groupedList[index].iloc[k - 2].Throughput, 0), ha='center',
                                     va='bottom', color='blue', size=8)

                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1].Throughput, 0),
                                 numpy.round(groupedList[index].iloc[k - 1].Throughput, 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(groupedList[index].iloc[k].Time,
                                 numpy.round(groupedList[index].iloc[k].Throughput, 0),
                                 numpy.round(groupedList[index].iloc[k].Throughput, 0), ha='center', va='bottom',
                                 color='blue', size=8)

                    if (k == 1 or (k < num_bars and groupedList[index].iloc[k-1].Temperature != groupedList[index].iloc[k].Temperature)):
                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1].Temperature, 0) * alignValue,
                                 numpy.round(groupedList[index].iloc[k - 1].Temperature, 0), ha='center', va='bottom',
                                 color='green', size=8)
                        plt.text(groupedList[index].iloc[k].Time,
                                 numpy.round(groupedList[index].iloc[k].Temperature, 0) * alignValue,
                                 numpy.round(groupedList[index].iloc[k].Temperature, 0), ha='center', va='bottom',
                                 color='green', size=8)

            plt.title('Throughput - Temperature Graph', size=20)
            plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=10)
            plt.legend(['Throughput', 'Temperature'])
            plt.grid(True)

            plt.subplot(212)
            alignValue = measurementData.Throughput.max() / measurementData['CPU_Usage(%)'].max() / 2

            plt.plot(groupedList[index].Time, groupedList[index].Throughput)
            plt.plot(groupedList[index].Time, groupedList[index]['CPU_Usage(%)'] * alignValue)


            for k in range(1, num_bars + 1):
                if (DISPLAY_DETAIL_DATA == False):
                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0),
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0), ha='center', va='bottom',
                             color='blue', size=8)
                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0) * alignValue,
                             numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0), ha='center', va='bottom',
                             color='green', size=8)

                else :
                    if (k < num_bars and groupedList[index].iloc[k - 1].Throughput < groupedList[index].Throughput.mean()):
                        if (k > 2):
                            plt.text(groupedList[index].iloc[k - 2].Time,
                                     numpy.round(groupedList[index].iloc[k - 2].Throughput, 0),
                                     numpy.round(groupedList[index].iloc[k - 2].Throughput, 0), ha='center',
                                     va='bottom', color='blue', size=8)

                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1].Throughput, 0),
                                 numpy.round(groupedList[index].iloc[k - 1].Throughput, 0), ha='center', va='bottom',
                                 color='blue', size=8)
                        plt.text(groupedList[index].iloc[k].Time,
                                 numpy.round(groupedList[index].iloc[k].Throughput, 0),
                                 numpy.round(groupedList[index].iloc[k].Throughput, 0), ha='center', va='bottom',
                                 color='blue', size=8)

                    if (k < num_bars and (groupedList[index].iloc[k - 1]['CPU_Usage(%)'] == groupedList[index]['CPU_Usage(%)'].max() or
                                                  groupedList[index].iloc[k - 1]['CPU_Usage(%)'] == groupedList[index]['CPU_Usage(%)'].min())):
                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0) * alignValue,
                                 numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0), ha='center', va='bottom',
                                 color='green', size=8)

                    if (k == 1 or ((k % 10) == 0)):
                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0) * alignValue,
                                 numpy.round(groupedList[index].iloc[k - 1]['CPU_Usage(%)'], 0), ha='center', va='bottom',
                                 color='green', size=8)

            # plt.xlabel('time (ms)', size=10)
            plt.title('Throughput - CPU Usage Graph', size=20)
            plt.ylabel('Throughput (Mbps) / CPU Usage (%)', size=10)
            plt.legend(['Throughput', 'CPU Usage(%)'])
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    def create_cpuclock_graph(self, throughputResult, measurementData, groupedList, index):
        if (index == -1):
            cpuCount = 0
            for s in list(measurementData):
                if "CPU_CUR_Freq" in s:
                    cpuCount+= 1

            num_bars = len(measurementData.CPU_CUR_Freq0)
            cpuYlimMax = 0
            alignValue = 3000 / measurementData.Throughput.max()
            cpuYlimMax = measurementData.Throughput.max() * alignValue

            for j in range(1, cpuCount + 1):
                currentCpu = 'CPU_CUR_Freq' + str(j - 1)
                maxCpu = 'CPU_MAX_Freq' + str(j - 1)
                subplotTotalCount = cpuCount
                subplotRowCount = j

                if (subplotTotalCount > 4):
                    subplotTotalCount = subplotTotalCount - 4

                if (j > 4):
                    subplotRowCount = subplotRowCount - 4

                if (subplotRowCount == 1):
                    plt.figure(figsize=(19, 9))

                subplotNum = 100 * subplotTotalCount + 10 + subplotRowCount
                plt.subplot(subplotNum)

                plt.plot(measurementData.Time, measurementData.Throughput * alignValue)
                plt.plot(measurementData.Time, measurementData.Temperature * alignValue)
                plt.plot(measurementData.Time, measurementData[maxCpu])
                plt.plot(measurementData.Time, measurementData[currentCpu])

                maxCurrentCpuHit = False
                minCurrentCpuHit = False
                maxMaxCpuHit = False
                minMaxCpuHit = False
                dontDisplayData = False
                for k in range(1, num_bars + 1):
                    if (DISPLAY_DETAIL_DATA == False):
                        if (k < num_bars + DISPLAY_DELTA and dontDisplayData == False and measurementData.Throughput[k - 1] != 0) :
                            plt.text(measurementData.Time[k + DISPLAY_DELTA - 1], measurementData[maxCpu][k + DISPLAY_DELTA - 1],
                                     measurementData[maxCpu][k + DISPLAY_DELTA - 1],
                                     ha='center', va='bottom', color='r', size=8)
                            plt.text(measurementData.Time[k + DISPLAY_DELTA - 1], measurementData[currentCpu][k + DISPLAY_DELTA - 1],
                                     measurementData[currentCpu][k + DISPLAY_DELTA - 1],
                                     ha='center', va='bottom', color='purple', size=8)
                            plt.text(measurementData.Time[k + DISPLAY_DELTA - 1],
                                     numpy.round(measurementData.Temperature[k + DISPLAY_DELTA - 1], 0) * alignValue,
                                     numpy.round(measurementData.Temperature[k + DISPLAY_DELTA - 1], 0), ha='center', va='bottom',
                                     color='green', size=8)
                            dontDisplayData = True

                        if (measurementData.Throughput[k - 1] == 0) :
                            dontDisplayData = False

                    else:
                        if (measurementData[maxCpu][k - 1] == measurementData[maxCpu].max() and maxMaxCpuHit == False):
                            plt.text(measurementData.Time[k - 1], measurementData[maxCpu][k - 1], measurementData[maxCpu][k - 1],
                                     ha='center', va='bottom', color='r', size=8)
                            maxMaxCpuHit = True

                        if (measurementData[maxCpu][k - 1] == measurementData[maxCpu].min() and minMaxCpuHit == False):
                            plt.text(measurementData.Time[k - 1], measurementData[maxCpu][k - 1], measurementData[maxCpu][k - 1],
                                     ha='center', va='bottom', color='r', size=8)
                            minMaxCpuHit = True

                        if ((k % 10) == 0):
                            plt.text(measurementData.Time[k - 1], measurementData[maxCpu][k - 1], measurementData[maxCpu][k - 1],
                                     ha='center', va='bottom', color='b', size=8)

                        if (measurementData[currentCpu][k - 1] == measurementData[currentCpu].max() and maxCurrentCpuHit == False):
                            plt.text(measurementData.Time[k - 1], measurementData[currentCpu][k - 1], measurementData[currentCpu][k - 1],
                                     ha='center', va='bottom', color='purple', size=8)
                            maxCurrentCpuHit = True

                        if (measurementData[currentCpu][k - 1] == measurementData[currentCpu].min() and minCurrentCpuHit == False):
                            plt.text(measurementData.Time[k - 1], measurementData[currentCpu][k - 1], measurementData[currentCpu][k - 1],
                                     ha='center', va='bottom', color='purple', size=8)
                            minCurrentCpuHit = True

                        if (k == 1 or ((k % 10) == 0)):
                            plt.text(measurementData.Time[k - 1], measurementData[currentCpu][k - 1], measurementData[currentCpu][k - 1],
                                     ha='center', va='bottom', color='purple', size=8)


                        if (k == 1 or (k < num_bars and measurementData.Temperature[k - 1] != measurementData.Temperature[k])):
                            plt.text(measurementData.Time[k],
                                     numpy.round(measurementData.Temperature[k], 0) * alignValue,
                                     numpy.round(measurementData.Temperature[k], 0), ha='center', va='bottom',
                                     color='green', size=8)

                        if (k < num_bars and measurementData.Throughput[k - 1] != 0  and measurementData.Throughput[k - 1] != 0 and measurementData.Throughput[k - 1] < measurementData.Throughput.mean()):
                            if (k > 2):
                                plt.text(measurementData.Time[k - 2],
                                         numpy.round(measurementData.Throughput[k - 2], 0) * alignValue,
                                         numpy.round(measurementData.Throughput[k - 2], 0), ha='center', va='bottom',
                                         color='blue', size=8)

                            plt.text(measurementData.Time[k - 1],
                                     numpy.round(measurementData.Throughput[k - 1], 0) * alignValue,
                                     numpy.round(measurementData.Throughput[k - 1], 0), ha='center', va='bottom',
                                     color='blue', size=8)
                            plt.text(measurementData.Time[k],
                                     numpy.round(measurementData.Throughput[k], 0) * alignValue,
                                     numpy.round(measurementData.Throughput[k], 0), ha='center', va='bottom',
                                     color='blue', size=8)


                if (subplotNum == 100 * subplotTotalCount + 11):
                    plt.title('Throughput - CPU Clock Graph', size=20)
                plt.ylabel('CPU' + str(j - 1) + ' Clock (MHz)', size=10)
                plt.legend(['Throughput', 'Temperature', 'Max CPU Clock(MHz)', 'Current CPU Clock(MHz)'])
                plt.ylim(0, cpuYlimMax + 100)
                plt.grid(True)
                if (subplotNum == 100 * subplotTotalCount + 10 + subplotTotalCount):
                    plt.tight_layout()
                    plt.show()
        else:
            cpuCount = 0
            for s in list(measurementData):
                if "CPU_CUR_Freq" in s:
                    cpuCount += 1
            num_bars = len(groupedList[index].CPU_CUR_Freq0)

            cpuYlimMax = 0
            alignValue = 3000 / groupedList[index].Throughput.max()
            cpuYlimMax = groupedList[index].Throughput.max() * alignValue

            for j in range(1, cpuCount + 1):
                currentCpu = 'CPU_CUR_Freq' + str(j - 1)
                maxCpu = 'CPU_MAX_Freq' + str(j - 1)
                subplotTotalCount = cpuCount
                subplotRowCount = j

                if (subplotTotalCount > 4):
                    subplotTotalCount = subplotTotalCount - 4

                if (j > 4):
                    subplotRowCount = subplotRowCount - 4

                if (subplotRowCount == 1):
                    plt.figure(figsize=(19, 9))

                subplotNum = 100 * subplotTotalCount + 10 + subplotRowCount
                plt.subplot(subplotNum)


                plt.plot(groupedList[index].Time, groupedList[index].Throughput * alignValue)
                plt.plot(groupedList[index].Time, groupedList[index].Temperature * alignValue)
                plt.plot(groupedList[index].Time, groupedList[index][maxCpu])
                plt.plot(groupedList[index].Time, groupedList[index][currentCpu])

                for k in range(1, num_bars + 1):
                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0) * alignValue,
                             numpy.round(groupedList[index].iloc[k - 1].Throughput, 0), ha='center', va='bottom',
                             color='blue', size=8)

                    plt.text(groupedList[index].iloc[k - 1].Time,
                             numpy.round(groupedList[index].iloc[k - 1].Temperature, 0) * alignValue,
                             numpy.round(groupedList[index].iloc[k - 1].Temperature, 0), ha='center', va='bottom',
                             color='green', size=8)

                    if (k == 1 or (k < num_bars and groupedList[index].iloc[k-1][maxCpu] != groupedList[index].iloc[k][maxCpu])):
                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1][maxCpu], 0),
                                 numpy.round(groupedList[index].iloc[k - 1][maxCpu], 0), ha='center', va='bottom',
                                 color='red', size=8)

                    if (k == 1  or (k < num_bars and groupedList[index].iloc[k-1][currentCpu] != groupedList[index].iloc[k][currentCpu])):
                        plt.text(groupedList[index].iloc[k - 1].Time,
                                 numpy.round(groupedList[index].iloc[k - 1][currentCpu], 0),
                                 numpy.round(groupedList[index].iloc[k - 1][currentCpu], 0), ha='center', va='bottom',
                                 color='purple', size=8)

                if (subplotNum == 100 * subplotTotalCount + 11):
                    plt.title('Throughput - CPU Clock Graph', size=20)
                plt.ylabel('CPU' + str(j - 1) + ' Clock (MHz)', size=10)
                plt.legend(['Throughput', 'Temperature', 'Max CPU Clock(MHz)', 'Current CPU Clock(MHz)'])
                plt.ylim(0, cpuYlimMax + 100)
                plt.grid(True)
                if (subplotNum == 100 * subplotTotalCount + 10 + subplotTotalCount):
                    plt.tight_layout()
                    plt.show()

    def create_summary_graph(self, throughputResult, measurementData, groupedList, index):
        plt.figure(figsize=(19, 9))
        ax = plt.subplot(111)

        cpuCount = 0
        for s in list(measurementData):
            if "CPU_CUR_Freq" in s:
                cpuCount += 1

        alignTputValue = 3000 / throughputResult.Throughput.max() #groupedList[index].Throughput.max()
        alignTemperatureValue = 500 / throughputResult.AvgTemperature.max()

        num_bars = len(throughputResult.Throughput)
        plt.bar(throughputResult.CallCount, throughputResult.Throughput * alignTputValue, align='center',width=0.5, facecolor='#9999ff', edgecolor='white', label='Throughput')  ## 세로 막대
        plt.plot(throughputResult.CallCount, throughputResult.AvgTemperature * alignTemperatureValue, label='Temperature')  ## 세로 막대

        for j in range(1, cpuCount + 1):
            maxCpu = 'AvgMaxCpuFreq' + str(j - 1)
            cpuLabel = 'CPU' + str(j-1) + " Max Frequency"
            ax.plot(throughputResult.CallCount, throughputResult[maxCpu], label=cpuLabel)

        ax.legend()

        for k in range(0, num_bars):
            xAxisValue = k + 1
            if (k == 0):
                plt.text(xAxisValue, throughputResult.Throughput[k] * alignTputValue, throughputResult.Throughput[k],
                         ha='center', va='bottom', color='r')
                plt.text(xAxisValue, round(throughputResult.AvgTemperature[k], 0) * alignTemperatureValue,
                         round(throughputResult.AvgTemperature[k], 0), ha='center', va='bottom', color='r')


            if (num_bars > 100):
                if (throughputResult.Throughput[k] < throughputResult.Throughput.mean()):
                    plt.text(xAxisValue, throughputResult.Throughput[k] * alignTputValue, throughputResult.Throughput[k], ha='center', va='bottom')
            else:
                plt.text(xAxisValue, throughputResult.Throughput[k] * alignTputValue, throughputResult.Throughput[k], ha='center', va='bottom')
                plt.text(xAxisValue, round(throughputResult.AvgTemperature[k], 0) * alignTemperatureValue, round(throughputResult.AvgTemperature[k], 0), ha='center', va='bottom')

            if (xAxisValue < num_bars and round(throughputResult.AvgTemperature[k]) != round(throughputResult.AvgTemperature[k + 1])):
                plt.text(xAxisValue + 1, round(throughputResult.AvgTemperature[k + 1],0) * alignTemperatureValue, round(throughputResult.AvgTemperature[k + 1],0), ha='center', va='bottom', color='r')

            if (throughputResult.Throughput[k] == throughputResult.Throughput.max() or
                        throughputResult.Throughput[k] == throughputResult.Throughput.min() or
                        throughputResult.Throughput[k] == throughputResult.Throughput.mean()):
                plt.text(xAxisValue, throughputResult.Throughput[k] * alignTputValue, throughputResult.Throughput[k], ha='center', va='bottom', color='red')

            for j in range(1, cpuCount + 1):
                maxCpu = 'AvgMaxCpuFreq' + str(j - 1)
                if (k == 0):
                    plt.text(xAxisValue, throughputResult[maxCpu][k], throughputResult[maxCpu][k], ha='center', va='bottom', color='red')
                if (xAxisValue < num_bars and throughputResult[maxCpu][k] != throughputResult[maxCpu][k + 1]):
                    plt.text(xAxisValue + 1, throughputResult[maxCpu][k + 1], throughputResult[maxCpu][k + 1], ha='center', va='bottom', color='red')

        plt.xlabel('Call Count', size=10)
        plt.ylabel('Throughput (Mbps) / Temperature (.C) / CPU Clock (MHz)', size=10)
        title = measurementData.Direction[0] + ' Overall Result Graph'
        plt.title(title, size=20)
        plt.grid(True)

        plt.tight_layout()
        plt.show()


    def create_line_graph(self, measurementData, time1, throughput, Temperature, cpuUsage):
        plt.figure(figsize=(15, 8))

        plt.subplot(211)
        plt.plot(measurementData.Time, throughput)
        plt.plot(time1, Temperature)
        plt.title('Throughput - Temperature (Detailed Graph)', size=10)
        #plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=10)
        plt.legend(['Throughput', 'Temperature'])
        plt.grid(True)
        # plt.show()

        #plt.figure(figsize=(15, 8))
        plt.subplot(212)
        plt.plot(time1, throughput)
        plt.plot(time1, cpuUsage)
        plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throughput (Mbps) / CPU Usage (%)', size=10)
        plt.title('Throughput - CPU Usage (Detailed Graph)', size=10)
        plt.legend(['Throughput', 'CPU Usage(%)'])
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    def create_line_graph2(self, data, time1, throughput, time2, temperature, cpuUsage):
        plt.figure(figsize=(15, 8))
        plt.plot(time1, throughput, time2, temperature, cpuUsage, 'c')
        plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throuthput (Mbps)', size=20)
        plt.title('Detailed Throughput Graph', size=20)
        plt.legend(['Throughput', 'Temperature'])
        # plt.legend(['Throughput', 'CPU Usage(%)'])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def create_bar_graph(self, data, labels):
        num_bars = len(data)
        positions = range(1, num_bars + 1)
        ##    plt.barh(positions, data, align='center') ## 가로 막대
        plt.figure(figsize=(15, 8))

        #plt.bar(positions, data, align='center', width=0.5)  ## 세로 막대
        plt.bar(positions, data, align='center', width=0.5, facecolor='#9999ff', edgecolor='white')  ## 세로 막대

        #write t-put result on bar-graph
        for k in range(1, num_bars + 1):
            plt.text(k, data[k-1], data[k-1], ha='center', va='bottom')

        plt.xticks(positions, labels)
        plt.xlabel('Call Count', size=15)
        plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=15)
        plt.title('Throughput Result (Summary Graph)', size=15)
        plt.grid()
        plt.show()

    def create_distplot_graph(self, data):
        sns.distplot(data)
        plt.show()

    def create_pairplot_graph(self, data):
        sns.pairplot(data, hue='CPU Usage', palette='husl')
        plt.show()

    def create_lmplot_graph(self, xAxis, yAxis, Data):
        sns.set_style("darkgrid")
        sns.lmplot(x=xAxis, y=yAxis, data=Data, size=20)
        plt.show()

    def create_boxplot_graph(self, data, columnName):
        plt.figure(figsize=(8,6))
        sns.boxplot(x=data[columnName])
        plt.show()

    def create_kdeplot_graph(self, data):
        sns.kdeplot(data, shade=True, color="r")
        plt.show()