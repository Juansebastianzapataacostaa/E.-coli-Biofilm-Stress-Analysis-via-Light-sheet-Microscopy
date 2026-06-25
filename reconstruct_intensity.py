import os
import numpy as np
import matplotlib.pyplot as plt
import re

def read_and_calculate_average(file_path):
    data = np.loadtxt(file_path, delimiter=',')
    return np.mean(data)
   

def main():
    folder = os.getcwd()
    file_extension = '.txt'

    files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(file_extension)]
    intensidad_promedio = []

    for file_path in files:
        average = read_and_calculate_average(file_path)
        if average is not None:
            intensidad_promedio.append(average)

    if intensidad_promedio:
        maximo = np.max(intensidad_promedio)
        intensidad_promedio = intensidad_promedio / maximo

    # Etiquetas para el eje x
    etiquetas = [os.path.splitext(os.path.basename(file))[0] for file in files]
    etiquetas_numeros = [int(re.search(r'\d+', tag).group()) for tag in etiquetas if re.search(r'\d+', tag)]

    # Se grafican los valores promedio de intensidad en funcion del tiempo
    plt.plot(etiquetas_numeros, intensidad_promedio, 'o-')
    plt.xlabel('Tiempos')
    plt.ylabel('Intensidad promedio')
    plt.title('Intensidad promedio de Bacteria')
    plt.show()

main()

