import matplotlib.pyplot as plt

class GraphManager :
    def create_line_graph(self, data, label1, label2, label3, label4):
        plt.figure(figsize=(15, 8))
        plt.plot(label1, label2, label3, label4, 'c')
        plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throuthput (Mbps)', size=15)
        plt.title('Detailed Throughput Graph', size=15)
        plt.legend(['Throughput', 'Temperature'])
        plt.grid(True)
        plt.show()

    def create_bar_graph(self, data, labels):
        num_bars = len(data)
        positions = range(1, num_bars + 1)
        ##    plt.barh(positions, data, align='center') ## 가로 막대
        plt.figure(figsize=(15, 8))
        
        #plt.bar(positions, data, align='center', width=0.5)  ## 세로 막대
        plt.bar(positions, data, align='center', width=0.5, facecolor='#9999ff', edgecolor='white')  ## 세로 막대

        for k in range(1, num_bars + 1):
            print(k)
            plt.text(k, data[k-1], data[k-1], ha='center', va='bottom')

        plt.xticks(positions, labels)
        plt.xlabel('Call Count', size=15)
        plt.ylabel('Throughput (Mbps)', size=15)
        plt.title('Throughput Result', size=15)
        plt.grid()
        plt.show()
