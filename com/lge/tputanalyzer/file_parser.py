import pandas

class FileParser:
    def getDataFrameFromFile(self, file_path):
        self.data_frame = pandas.read_csv(file_path)
        return self.data_frame