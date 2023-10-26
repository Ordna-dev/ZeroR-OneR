import pandas
import tkinter
from tkinter import filedialog

#read = pandas.read_csv("Load_dataset/cerealPython.csv") #ejemplo de uso de pandas

def printCSV():

    window = tkinter.Tk()
    window.withdraw()

    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    try:
        read = pandas.read_csv(filename)
    except FileNotFoundError:
        print(f"No se encontro el archivo {filename}.")

    return read.head()