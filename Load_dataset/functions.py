import pandas, tkinter, random
from tkinter import filedialog

def main(): #Funcion que se encarga de leer el archivo csv y ejecuta las funciones de ZeroR y OneR

    notCatchedData = True

    while(notCatchedData):

        window = tkinter.Tk() 
        window.withdraw() #Código para abrir la ventana de explorador de archivos

        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]) #El usuario sólo puede seleccionar archivos csv

        #Si el usuario cancela la seleccion de archivo, se sale del loop
        if filename == '':
            print("Se cancelo la seleccion de archivo")
            break

        try:
            read = pandas.read_csv(filename) #Si lee el archivo se asignan los atributos y las instancias a una variable
            notCatchedData = False
        except FileNotFoundError:
            print(f"No se encontro el archivo {filename}.") #En caso contrario, mandará mensaje de error a consola

    data = read.head(50) if filename else None #Leer maximo 50 instancias

    if data is not None:
        train, test = divideData(data) #Se asignan las instancias a los conjuntos de entrenamiento y prueba
        #class_attribute = random.choice(data.columns)
        print("\nConjunto de entrenamiento:\n")
        print(test)
        #testing(test, class_attribute)
        print("\nConjunto de prueba:\n")
        print(train)
        #testing(train, class_attribute)

        #Aca van a llamar las funciones de zeroR y oneR


def divideData(data):
    #Se mezclan el orden de los datos
    data = data.sample(frac=1)

    #Calculo de el indice donde se dividen los datos
    divide_index = int(len(data) * 0.7)

    #Se dividen los datos los conjuntos de entrenamiento y prueba
    train = data[:divide_index]
    test = data[divide_index:]

    #Retornamos los conjuntos
    return test, train

def testing(data, class_attribute): #Función puramente para pruebas, pueden tomarlo como base para la realizacion de ZeroR y OneR
    
    counts = data[class_attribute].value_counts() 
    counts_string = str(counts) #Toma los atributos y los cuenta
    counts_string = '\n'.join(counts_string.split('\n')[:-1]) #No imprimir la ultima linea de impresión ya que hay informacion basura

    print(f"\nRecuentos para el atributo clase {class_attribute}:\n{counts_string}")

def zeroR(): #Parte de Esparza

    return 0

def oneR(): #Parte de Isaac

    return 0