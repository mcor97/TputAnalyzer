import pandas

class FileParser:
    def get_dataframe_from_file(self, file_path):
        self.data_frame = pandas.read_csv(file_path)
        return self.data_frame