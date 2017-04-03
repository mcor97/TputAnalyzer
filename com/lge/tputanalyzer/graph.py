import matplotlib.pyplot as plt

class Graph :

    def create_line_graph(self, data, label1, label2, label3, label4):
        plt.clf()
        ##plt.figure(figsize=(15, 8))
        ##plt.plot(rawData.time, rawData.velocityUsingyDiff, rawData.time, rawData.Position, 'c')
        plt.plot(label1, label2, label3, label4, 'c')
        ##plt.xlabel('time (s)', size=15)
        ##plt.ylabel('rad or rad/sec', size=15)
        ##plt.title('Calculating Velocity using simple differencial', size=15)
        ##plt.legend(['velocityDiff', 'Position'])
        ##plt.axis([4, 25, -270, 240])
        plt.grid(True)
        plt.show()

    def create_bar_graph(self, data, labels):
        num_bars = len(data)
        positions = range(1, num_bars + 1)
        ##    plt.barh(positions, data, align='center') ## 가로 막대
        plt.bar(positions, data, align='center', width=0.5)  ## 세로 막대
        plt.xticks(positions, labels)
        plt.xlabel('Call Count')
        plt.ylabel('Throughtput')
        plt.title('Throughput Summary')
        plt.grid()
        plt.show()
