import pandas as pd

class DataWriter:
    def __init__(self,data,filename) -> None:
        self.data = data
        self.filename = filename

    def writeTocsv(self):
        d = pd.DataFrame(self.data)
        print(d)
        d.to_csv(self.filename, sep='\t', encoding='utf-8', index=False)