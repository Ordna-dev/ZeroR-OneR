import pandas

read = pandas.read_csv("Load_dataset/cerealPython.csv")

def printCSV():
    return read.head()