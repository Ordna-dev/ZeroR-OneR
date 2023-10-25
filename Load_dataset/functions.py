import pandas

read = pandas.read_csv("Load_dataset/cerealPython.csv") #ejemplo de uso de pandas

def printCSV():
    return read.head()