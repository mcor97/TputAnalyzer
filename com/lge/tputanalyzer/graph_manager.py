import matplotlib.pyplot as plt
import seaborn as sns

class GraphManager :

    def create_temperature_cpuusage_graph(self, throughputResult, measurementData):

        num_bars = len(measurementData.Time)
        plt.figure(figsize=(19, 9))
        plt.subplot(211)
        plt.plot(measurementData.Time, measurementData.Throughput)
        plt.plot(measurementData.Time, measurementData.Temperature)

        # write t-put result on bar-graph
        i = 0
        for k in range(1, num_bars + 1):
            if (k < num_bars and measurementData.Temperature[k] != measurementData.Temperature[k - 1]):
                plt.text(measurementData.Time[k - 1], measurementData.Temperature[k - 1], measurementData.Temperature[k - 1], ha='center', va='bottom', color='r')


        plt.title('Throughput - Temperature Graph', size=10)
        plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=20)
        plt.legend(['Throughput', 'Temperature'])
        plt.grid()

        plt.subplot(212)
        plt.plot(measurementData.Time, measurementData.Throughput)
        plt.plot(measurementData.Time, measurementData['CPU_Usage(%)'])
        #plt.xlabel('time (ms)', size=10)
        plt.ylabel('Throughput (Mbps) / CPU Usage (%)', size=10)
        plt.title('Throughput - CPU Usage (Detailed Graph)', size=20)
        plt.legend(['Throughput', 'CPU Usage(%)'])
        plt.grid()
        plt.show()

    def create_cpuclock_graph(self, throughputResult, measurementData):

        cpuCount = 0
        for s in list(measurementData):
            if "Freq" in s:
                cpuCount+= 1

        num_bars = len(measurementData.CPU0_Freq0)

        cpuYlimMax = 0
        for i in range (1, cpuCount+1):
            if (cpuYlimMax < measurementData['CPU0_Freq' + str(i-1)].max()):
                cpuYlimMax =  measurementData['CPU0_Freq' + str(i-1)].max()

        for j in range (1, cpuCount+1):
            cpu = 'CPU0_Freq' + str(j-1)
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

            maxHit = False
            minHit = False
            plt.plot(measurementData.Time, measurementData.Throughput*10000)
            plt.plot(measurementData.Time, measurementData[cpu])
            i = 0
            for k in range(1, num_bars + 1):
                if (measurementData[cpu][k - 1] == measurementData[cpu].max() and maxHit == False):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='r')
                    maxHit = True

                if (measurementData[cpu][k - 1] == measurementData[cpu].min() and minHit == False):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='r')
                    minHit = True

                if (k == (round(num_bars / 20) * i + 1)):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='b', size=8)
                    i += 1

            if (subplotNum == 100 * subplotTotalCount + 11):
                plt.title('Throughput - CPU Clock Graph', size=20)
            plt.ylabel('CPU' + str(j-1) + ' Clock (KHz)', size=10)
            plt.legend(['Throughput', 'CPU Clock(KHz)'])
            plt.ylim(0, cpuYlimMax + 100000)
            plt.grid()
            if (subplotNum == 100 * subplotTotalCount + 10 + subplotTotalCount):
                plt.show()


    def create_cpuclock_temperature_graph(self, throughputResult, measurementData):

        cpuCount = 0
        for s in list(measurementData):
            if "Freq" in s:
                cpuCount+= 1

        num_bars = len(measurementData.CPU0_Freq0)

        cpuYlimMax = 0
        for i in range (1, cpuCount+1):
            if (cpuYlimMax < measurementData['CPU0_Freq' + str(i-1)].max()):
                cpuYlimMax =  measurementData['CPU0_Freq' + str(i-1)].max()

        for j in range (1, cpuCount+1):
            cpu = 'CPU0_Freq' + str(j-1)
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

            maxHit = False
            minHit = False
            plt.plot(measurementData.Time, measurementData.Throughput*10000)
            plt.plot(measurementData.Time, measurementData[cpu])
            plt.plot(measurementData.Time, measurementData.Temperature*10000)
            i = 0
            for k in range(1, num_bars + 1):
                if (measurementData[cpu][k - 1] == measurementData[cpu].max() and maxHit == False):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='r')
                    maxHit = True

                if (measurementData[cpu][k - 1] == measurementData[cpu].min() and minHit == False):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='r')
                    minHit = True

                if (k == (round(num_bars / 20) * i + 1)):
                    plt.text(measurementData.Time[k - 1], measurementData[cpu][k - 1], measurementData[cpu][k - 1], ha='center', va='bottom', color='b', size=8)
                    i += 1

                if (k < num_bars and measurementData.Temperature[k] != measurementData.Temperature[k - 1]):
                    plt.text(measurementData.Time[k - 1], measurementData.Temperature[k - 1], measurementData.Temperature[k - 1], ha='center', va='bottom', color='r', size=8)

            if (subplotNum == 100 * subplotTotalCount + 11):
                plt.title('Throughput - CPU Clock - Temperature Graph', size=20)
            plt.ylabel('CPU' + str(j-1) + ' Clock (KHz)', size=10)
            plt.legend(['Throughput', 'CPU Clock(KHz)', 'Temperature'])
            plt.ylim(0, cpuYlimMax + 100000)
            plt.grid()
            if (subplotNum == 100 * subplotTotalCount + 10 + subplotTotalCount):
                plt.show()


    def create_summary_graph(self, throughputResult, measurementData):
        plt.figure(figsize=(19, 9))
        plt.subplot(211)
        num_bars = len(throughputResult.Throughput)
        plt.bar(throughputResult.CallCount, throughputResult.Throughput, align='center',width=0.4, facecolor='#9999ff', edgecolor='white', label='Throughput')  ## 세로 막대
        plt.bar(throughputResult.CallCount + 0.4, throughputResult.AvgTemperature, align='center',width=0.4, color='g', edgecolor='white', label='Temperature')  ## 세로 막대

        # write t-put result on bar-graph
        i = 0
        for k in range(1, num_bars + 1):
            if (throughputResult.Throughput[k - 1] == throughputResult.Throughput.max()):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom', color='r')

            if (throughputResult.Throughput[k - 1] == throughputResult.Throughput.min()):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom', color='r')

            if (k < num_bars and round(throughputResult.AvgTemperature[k - 1]) != round(throughputResult.AvgTemperature[k])):
                plt.text(k+0.4, round(throughputResult.AvgTemperature[k - 1],0), round(throughputResult.AvgTemperature[k - 1],0), ha='center', va='bottom', color='r')

            #if (num_bars <= 30):
            if (k == (round(num_bars / 20) * i + 1)):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom')
                plt.text(k + 0.4, round(throughputResult.AvgTemperature[k - 1], 0), round(throughputResult.AvgTemperature[k - 1], 0), ha='center', va='bottom')
                i += 1

        plt.legend(['Throughput', 'Temperature'])
        plt.xlabel('Call Count', size=10)
        plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=10)
        title = measurementData.Direction[0] + ' Throughput Result (Summary Graph)'
        print(title)
        plt.title(title, size=20)
        plt.grid()


        plt.subplot(212)
        plt.plot(throughputResult.CallCount, throughputResult.Throughput)
        plt.plot(throughputResult.CallCount, throughputResult.AvgTemperature)

        for k in range(1, num_bars + 1):
            if (throughputResult.Throughput[k - 1] == throughputResult.Throughput.max()):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom', color='r')

            if (throughputResult.Throughput[k - 1] == throughputResult.Throughput.min()):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom', color='r')

            if (k < num_bars and round(throughputResult.AvgTemperature[k - 1]) != round(throughputResult.AvgTemperature[k])):
                plt.text(k, round(throughputResult.AvgTemperature[k - 1],0), round(throughputResult.AvgTemperature[k - 1],0), ha='center', va='bottom', color='r')

            if (num_bars <= 30):
                plt.text(k, throughputResult.Throughput[k - 1], throughputResult.Throughput[k - 1], ha='center', va='bottom')
                plt.text(k, round(throughputResult.AvgTemperature[k - 1], 0), round(throughputResult.AvgTemperature[k - 1], 0), ha='center', va='bottom')

        plt.legend(['Throughput', 'Temperature'])
        plt.xlabel('Call Count', size=10)
        plt.ylabel('Throughput (Mbps) / Temperature (.C)', size=10)
        ylimMax = throughputResult.Throughput.max()
        if (throughputResult.AvgTemperature.max() > ylimMax):
            ylimMax = throughputResult.AvgTemperature.max()
        plt.ylim(0, ylimMax+10)
        plt.grid()
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