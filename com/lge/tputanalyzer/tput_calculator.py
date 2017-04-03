import numpy

class TputCalculator :
    def add_tput_column(self, data):
        tput = numpy.zeros(len(data.Time))

        for i in numpy.arange(1, len(data.Time)):
            tput[i] = ((data.ReceivedBytes[i]) / (data.Time[i] - data.Time[i - 1])) * 8 * 1024 / 1000 / 1000

        data['Throughput'] = tput
        return data
