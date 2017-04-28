import pandas as pd

class FileParser:
    def getDataFrameFromFile(self, file_path):
        self.data_frame = pd.read_csv(file_path)
        return self.data_frame