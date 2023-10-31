# Programa hecho por:
# Guerrero Moya Alejandro
# Vazquez Valadez Angel Isaac

import pandas
import tkinter
import random
from tkinter import filedialog
from pandas import DataFrame
from typing import Dict
from collections import defaultdict

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
        print("\nZeroR: entrenamiento\n")
        zeroR(train, "calories")
        print("\nZeroR: prueba\n")
        zeroR(test, "calories")

        print("\nOneR: entrenamiento\n")
        oneR(train, "mfr")
        print("\nOneR: prueba\n")
        oneR(test, "mfr")
        # Naive Bayes
        naive_bayes = NaiveBayes()
        naive_bayes.fit(train, "mfr")
        naive_bayes.predict(test, "mfr")



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
                # print(f"Si {column} = {value}, entonces {target_column} = {most_common_class} con el error = {error}")
            
            error_rate = total_error / dataframe.shape[0]
            
            if error_rate < lowest_error_rate:
                lowest_error_rate = error_rate
                best_attribute = column
                best_rule = f"El mejor atributo {target_column} es {column} con el menor error = {error_rate}"
    
    print(best_rule)
    return best_attribute, lowest_error_rate


class NaiveBayes:
    def __init__(self):
        self.priors = dict()
        self.likelihoods = defaultdict(lambda: defaultdict(dict))
        self.classes = []
    
    # metodo de entrenamiento
    def fit(self, dataframe: DataFrame, target_column: str):
        total_records = len(dataframe)
        
        # Calcular a priori
        self.classes = dataframe[target_column].unique()
        print("\nClases unicas: ", self.classes)

        # Iterar sobre cada clase
        for cls in self.classes:
            # Calcular la probabilidad de que la clase sea igual a la clase actual
            self.priors[cls] = len(dataframe[dataframe[target_column] == cls]) / total_records
        
        print("\nProbabilidades a priori: ", self.priors)

        # calcula la probabilidad condicional
        for column in dataframe.columns:
            # Ignorar el atributo clase
            if column != target_column:
                # Iterar sobre cada valor del atributo
                for cls in self.classes:
                    # Obtener el subconjunto de datos donde el valor del atributo es igual al valor actual
                    cls_subset = dataframe[dataframe[target_column] == cls]
                    # Iterar sobre cada valor del atributo
                    for value in dataframe[column].unique():
                        # Calcular la probabilidad de que el valor del atributo sea igual al valor actual
                        self.likelihoods[column][value][cls] = len(cls_subset[cls_subset[column] == value]) / len(cls_subset)
    
        print("\nProbabilidades condicionales: ", dict(self.likelihoods))


    # metodo de prediccion
    def predict(self, dataframe: DataFrame, target_column: str):
        predictions = []
        # Iterar sobre cada fila del dataframe
        for _, row in dataframe.iterrows():
            # Obtener los valores de cada atributo
            record = row.drop(target_column).to_dict()
            print("\nRegistro actual: ", record)

            # Calcular la probabilidad de que la clase sea igual a la clase actual
            probabilities = dict()
            for cls in self.classes:
                prob = self.priors[cls]
                # Calcular la probabilidad condicional
                for feature, value in record.items():
                    # Si el valor del atributo no existe en el conjunto de entrenamiento, ignorarlo
                    prob *= self.likelihoods.get(feature, {}).get(value, {}).get(cls, 0)
                # Asignar la probabilidad a la clase actual
                probabilities[cls] = prob
            
            print("\nProbabilidades: ", probabilities)
            # Obtener la clase con la probabilidad mas alta
            predictions.append(max(probabilities, key=probabilities.get))
        
        print("\nPredicciones: ", predictions)

        # Calcular la precision
        correct_predictions = sum([1 for actual, pred in zip(dataframe[target_column], predictions) if actual == pred])
        accuracy = correct_predictions / len(dataframe)
        print(f"\nPrecision NaiveBayes: {accuracy * 100:.2f}%")
        return predictions