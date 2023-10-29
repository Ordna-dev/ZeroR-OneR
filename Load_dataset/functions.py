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
        test, train = divideData(data) #Se asignan las instancias a los conjuntos de entrenamiento y prueba

        print("\nConjunto de entrenamiento:\n")
        print(train)

        print("\nConjunto de prueba:\n")
        print(test)
        
        class_attribute = input("\nIntroduce el nombre del atributo clase: ")

        print("\nOneR - Alejandro Guerrero Moya")
        print("\nTabla de frencuencias en el conjunto de entrenamiento:")
        oneR(train, class_attribute)

        print("\nTabla de frecuencias en el conjunto de prueba:")
        oneR(test, class_attribute)

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

def zeroR(): #Parte de Isaac

    return 0

def oneR(data, class_attribute): #Algoritmo de OneR hecho por Alejandro Guerrero Moya
    # Tabla de frecuencias

    # Se obtienen todos los valores únicos del atributo clase
    class_values = data[class_attribute].unique()

    # Iteracion sobre cada columna
    for column in data.columns:

        #Si la columna es la clase atributo, se salta
        if column == class_attribute:
            continue
        
        # Se crea la tabla de frecuencias
        frequency_table = data.groupby([column, class_attribute]).size()

        # Se imprime el nombr del atributo
        print(f"\nAtributo: {column}.")

        # Iteracion sobre cada valor unico en la columna

        for value in data[column].unique():
            # Imprimir conteos para vada valor de la clase atributo
            counts = []
            for class_value in class_values:
                count = frequency_table.get((value, class_value), 0)
                counts.append(f"{class_value}: {count}")

            print(f"Valor: {value}. {', '.join(counts)}.")
    
    #Tabla de reglas

    print("\nTabla de reglas\n")

    # Inicializa el error mínimo como infinito
    min_error = float('inf')

    # Inicializa el atributo con el error mínimo como None
    min_error_attr = None

    # Itera sobre cada columna en los datos
    for column in data.columns:

        # Si la columna es el atributo clase, la salta
        if column == class_attribute:
            continue

        # Crea una tabla de frecuencias para cada valor de la columna y el atributo clase
        frequency_table = data.groupby([column, class_attribute]).size()

        # Inicializa la tabla de reglas y los contadores de error e instancias totales
        rule_table = {}
        total_error = 0
        total_instances = 0

        print(f"\nAtributo: {column}.")

        # Itera sobre cada valor único en la columna
        for value in data[column].unique():

            # Inicializa un diccionario para contar las ocurrencias de cada valor de clase
            counts = {}

            # Llena el diccionario con las ocurrencias de cada valor de clase para el valor actual de la columna
            for class_value in class_values:
                count = frequency_table.get((value, class_value), 0)
                counts[class_value] = count

            # Encuentra el valor de clase más frecuente y calcula el error para este valor de la columna
            max_class_value = max(counts, key=counts.get)
            error = sum(count for class_value, count in counts.items() if class_value != max_class_value)

            # Actualiza los contadores de error e instancias totales
            total_instances += sum(counts.values())
            total_error += error

            # Agrega la regla a la tabla de reglas
            rule_table[value] = (max_class_value, error, sum(counts.values()))

            print(f"Valor: {value}->{max_class_value}. {error}/{sum(counts.values())}.")

        # Imprime el error total para este atributo
        print(f"Error total: {total_error}/{total_instances}.")
        
        # Si el error total para este atributo es menor que el error mínimo actual, actualiza el error mínimo y el atributo con el error mínimo
        if total_error < min_error:
            min_error = total_error
            min_error_attr = column

    # Imprime el atributo con el error total más pequeño y su error
    print(f"\nEl atributo con el error total más pequeño es: {min_error_attr} con un error total de {min_error}.")
