import pandas
import tkinter
import random
from tkinter import filedialog
from pandas import DataFrame


def main():  # Funcion que se encarga de leer el archivo csv y ejecuta las funciones de ZeroR y OneR

    notCatchedData = True

    while (notCatchedData):

        try:
            # Si lee el archivo se asignan los atributos y las instancias a una variable
            read = pandas.read_csv("./Load_dataset/cerealPython.csv")
            notCatchedData = False
        except FileNotFoundError:
            # En caso contrario, mandará mensaje de error a consol
            print(f"No se encontro el archivo .")

    data = read.head(50)  # Leer maximo 50 instancias

    if data is not None:
        # Se asignan las instancias a los conjuntos de entrenamiento y prueba
        train, test = divideData(data)
        # class_attribute = random.choice(data.columns)
        print("\nConjunto de entrenamiento:\n")
        print(test)
        # testing(test, class_attribute)
        print("\nConjunto de prueba:\n")
        print(train)
        # testing(train, class_attribute)

        # Aca van a llamar las funciones de zeroR y oneR
        # zeroR(train, "calories")
        oneR(train)


def divideData(data):
    # Se mezclan el orden de los datos
    data = data.sample(frac=1)

    # Calculo de el indice donde se dividen los datos
    divide_index = int(len(data) * 0.7)

    # Se dividen los datos los conjuntos de entrenamiento y prueba
    train = data[:divide_index]
    test = data[divide_index:]

    # Retornamos los conjuntos
    return test, train


# Función puramente para pruebas, pueden tomarlo como base para la realizacion de ZeroR y OneR
def testing(data, class_attribute):

    counts = data[class_attribute].value_counts()
    counts_string = str(counts)  # Toma los atributos y los cuenta
    # No imprimir la ultima linea de impresión ya que hay informacion basura
    counts_string = '\n'.join(counts_string.split('\n')[:-1])

    print(
        f"\nRecuentos para el atributo clase {class_attribute}:\n{counts_string}")


def zeroR(dataframe: DataFrame, target_column: str):
    most_frequent_value = dataframe[target_column].mode().iloc[0]
    print(most_frequent_value)
    return most_frequent_value


def oneR(dataframe: DataFrame):
    best_attributes = {}

    for target in dataframe.columns:
        min_error = float('inf')
        best_attribute_for_target = None

        # Considerar cada otra columna como predictor
        for attribute in dataframe.columns:
            if attribute != target:
                total_error = 0

                for value in dataframe[attribute].unique():
                    sub_df = dataframe[dataframe[attribute] == value]
                    most_common_class = sub_df[target].value_counts().idxmax()

                    # Error es el total de filas menos las que tienen la clase más común
                    error = len(sub_df) - \
                        (sub_df[target] == most_common_class).sum()
                    total_error += error

                if total_error < min_error:
                    min_error = total_error
                    best_attribute_for_target = attribute

        best_attributes[target] = best_attribute_for_target
        print(best_attributes)

    return best_attributes
