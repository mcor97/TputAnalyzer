import matplotlib.pyplot as plt
import seaborn as sns

class GraphManager :
    def create_line_graph(self, data, time1, throughput, time2, cpuUsage):
        plt.figure(figsize=(15, 8))
        plt.plot(time1, throughput, time2, cpuUsage, 'c')
        plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throuthput (Mbps)', size=20)
        plt.title('Detailed Throughput Graph', size=20)
        # plt.legend(['Throughput', 'Temperature'])
        plt.legend(['Throughput', 'CPU Usage(%)'])
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
        plt.ylabel('Throughput (Mbps)', size=15)
        plt.title('Throughput Result', size=15)
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