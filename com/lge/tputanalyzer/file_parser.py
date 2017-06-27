#-*- encoding: utf-8 -*-
import pandas as pd

class FileParser:
    def getDataFrameFromFile(self, file_path):
        self.data_frame = pd.read_csv(file_path)
        print(self.data_frame)
        return self.data_frame