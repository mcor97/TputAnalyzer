import matplotlib.pyplot as plt

class Graph :

    def create_line_graph(self, data, label1, label2, label3, label4):
        plt.figure(figsize=(15, 8))
        plt.plot(label1, label2, label3, label4, 'c')
        plt.xlabel('time (ms)', size=15)
        plt.ylabel('Throuthput', size=15)
        plt.title('Throughput Graph', size=15)
        plt.legend(['Throughput', 'Temperature'])
        plt.grid(True)
        plt.show()

    def create_bar_graph(self, data, labels):
        num_bars = len(data)
        positions = range(1, num_bars + 1)
        ##    plt.barh(positions, data, align='center') ## 가로 막대
        plt.figure(figsize=(15, 8))
        plt.bar(positions, data, align='center', width=0.5)  ## 세로 막대
        plt.xticks(positions, labels)
        plt.xlabel('Call Count', size=15)
        plt.ylabel('Throughput', size=15)
        plt.title('Throughput Summary', size=15)
        plt.grid()
        plt.show()
