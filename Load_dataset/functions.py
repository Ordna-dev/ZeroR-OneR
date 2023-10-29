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
        zeroR(train, "calories")
        oneR(train, "mfr")
        


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
    # Obtener la clase mas comun
    most_common_value = dataframe[target_column].mode()[0]
    # Imprimir la clase mas comun
    print(f'ZeroR: {most_common_value}')
    return most_common_value


def oneR(dataframe: DataFrame, target_column: str = "mfr"):
    # inicializar variables
    best_attribute = None # establecer el error minimo hacia el infino
    lowest_error_rate = float('inf')  # atributo error minimo
    best_rule = "" #mejor regla
    print('\nOneR: \n')

    # Iterar sobre cada columna/atributo de los datos excepto el atributo clase, nombre y tipo
    for column in dataframe.columns:
        if column != target_column and column != "name" and column != "type":
            total_error = 0

            # Obtener la tabla de frecuencia de cada valor del atributo
            frequency_table = dataframe[column].value_counts()
            
            # Iterar sobre cada valor de ese atributo
            for value in frequency_table.index:
                # Obtener el subconjunto de datos donde el valor del atributo es igual al valor actual
                subset = dataframe[dataframe[column] == value]
                # Obtener la clase mas comun de ese subconjunto
                most_common_class = subset[target_column].mode()[0]
                # Obtener el numero de instancias que fueron clasificadas incorrectamente
                correctly_classified = subset[subset[target_column] == most_common_class].shape[0]
                
                # Calcular el error
                error = subset.shape[0] - correctly_classified
                total_error += error
                
                # Imprimir la regla
                print(f"Si {column} = {value}, entonces {target_column} = {most_common_class} con el error = {error}")
            
            error_rate = total_error / dataframe.shape[0]
            
            if error_rate < lowest_error_rate:
                lowest_error_rate = error_rate
                best_attribute = column
                best_rule = f"El mejor atributo {target_column} es {column} con el menor error = {error_rate}"
    
    print(best_rule)
    return best_attribute, lowest_error_rate


    
