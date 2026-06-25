# Este archivo es para crear métodos que se puedan usar en otros archivos para analizar imágenes de cultivos de bacterias.

# Arreglos
import numpy as np

# Directorios
import os

# Graficas
import matplotlib.pylab as plt

# Procesamiento de imagenes (mirar con cual libreria quedarse)
from PIL import Image, ImageSequence
from skimage.morphology import opening, disk, reconstruction, local_minima , closing,  square,   white_tophat
from skimage.filters import  rank, threshold_triangle, threshold_otsu, sobel, threshold_local,sobel,  threshold_sauvola, threshold_niblack
from skimage.color import label2rgb
from skimage import exposure
from skimage import filters
import imageio
import glob
import tifffile

#Tiempo
import time

def analisis_imagenes(valor_Top_Hat: int, nombres) -> None:

    start = time.time()

    # Crea algunas matrices para almacenar información sobre el área, intensidad, etc.
    areaactual = np.zeros([1,101]) 
    areamaxima = np.zeros([1,101]) 

    # EN REVISION: Crea una matriz para almacenar la máscara de área máxima
    # mascaraareamax = np.zeros([900, 2560], dtype = bool)

    intensidad = np.zeros([1,101])
    intensidadFondo = np.zeros([1,101])
    area = np.zeros([1,101])

    #Definimos la variable coloniasFijas como False
    coloniasFijas = False

    # Define el estado de las colonias
    coloniasFijas = False

    # Define una lista de tiempos
    tiempos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]
    contador = 0


    #---------------------------------------------------------------------

    # Itera sobre cada archivo de la lista de nombres de archivo
    for nombre in nombres:
        
        # Abre la imagen como una pila de imágenes y guarda la primera imagen de la pila en una variable
        stack = Image.open(nombre)
        frnm = 0

        # Crea algunas matrices para almacenar información sobre la intensidad, fondo, área, etc. en cada marco de la pila
        tintensidad = np.zeros([1,101])
        fondoIterado = np.zeros([1,101])
        Intesidad_Fondo = np.zeros([1,101])
        
        # Itera sobre cada marco de la pila
        for frame in ImageSequence.Iterator(stack):
                        
            # Convierte el marco a una matriz NumPy
            arreglo_imagen = np.array(frame)    
            """
            # También se convierte el siguente marco a una matriz NumPy
            if frnm <= 100:
                next_frame = next(ImageSequence.Iterator(stack))

                # Se convierte el siguiente marco a una matriz NumPy
                arreglo_imagen_next = np.array(next_frame)

                # Corremos 19 pixeles hacia arriba la imagen siguiente
                arreglo_imagen_next = np.roll(arreglo_imagen_next, -19, axis=0)

            """


            # Queremos reducir el ruido de fondo, por medio de un filtro de mediana
            # Usamos la libreria skimage.filters
            #arreglo_imagen = filters.median(arreglo_imagen)
            filtroMedia = "No"

            # Aplica un filtro gaussiano a la imagen
            sigma = 1
            imagen = filters.gaussian(arreglo_imagen, sigma = sigma)
            
            # Aplica un filtro de tophat blanco a la imagen
            imagen = white_tophat(imagen, footprint=disk(valor_Top_Hat))

            # Se calcula el umbral usando el método de Otsu para la imagen actual
            umbral = threshold_otsu(imagen)
            #umbral =threshold_triangle(imagen)



            

            # Se crea una máscara binaria a partir de la imagen y el umbral
            mascara = imagen > umbral

            # Se verifica si el nombre de la imagen contiene "T015"
            #if "T015" in nombre:
            #    coloniasFijas = True

            # Se guarda el área actual de la colonia en un arreglo
            areaactual[0,frnm] = np.sum(mascara)
            #areaactual[0,frnm] = np.sum(mascara)


            # Si las colonias no son fijas, se usa la máscara actual
            if coloniasFijas == False:
                mascaraSum=mascara

            # Si las colonias son fijas, se une la máscara actual con la máscara anterior
            """
            elif coloniasFijas == True:
                mascaraSum = np.logical_or( mascaraareamax[:,2090*frnm:2090*(frnm+1)]  , mascara )
                mascaraareamax[:,2090*(frnm):2090*(frnm+1)] = mascaraSum
            """

            # Se calcula la intensidad de la imagen dentro de la máscara
            tintensidad[0,frnm] = np.mean(arreglo_imagen[mascaraSum]) 

            # Se crea una máscara con los pixeles que no están en la máscara actual
            notMask =   np.logical_not(mascara)

            # Se calcula la intensidad de la imagen fuera de la máscara
            fondoIterado[0,frnm] = np.mean(arreglo_imagen[notMask]) 

            # Se calcula el área de la máscara
            Intesidad_Fondo[0,frnm] = np.mean(mascaraSum)

            # Imprimimos varias cosas para verificar que todo esté bien
            print("tintensidad: ", tintensidad[0,frnm]
                    , "fondoIterado: ", fondoIterado[0,frnm]
                    , "Intesidad_Fondo: ", Intesidad_Fondo[0,frnm])


            #Hacemos tres gráficas en un subplot para ver la imagen original, la máscara y la imagen sin máscara
            #La grafica es para presentar el array 2D
            plt.figure(figsize=(30,30), dpi=100, facecolor='w', edgecolor='k')
            plt.subplot(1,3,1)
            plt.imshow(arreglo_imagen)
            plt.title("Imagen original")
            plt.xlabel("Número de pixel")
            plt.ylabel("Intensidad")
            
            plt.subplot(1,3,2)
            plt.imshow(mascara)
            plt.title("Máscara")
            plt.xlabel("Número de pixel")
            plt.ylabel("Intensidad")


            plt.subplot(1,3,3)
            plt.imshow(notMask)
            plt.title("Imagen sin máscara")
            plt.xlabel("Número de pixel")
            plt.ylabel("Intensidad")

            # Guradamos las tres imagenes en un archivo .tif
            # El archivo se nombra de acuerdo al número de tiempo, el valor del filtro de tophat, el número de frame y el tiempo del computador en segundo en que se tomó la imagen
            nombre = 'imagen-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '_' + str(time.time()) + '.tif'
            plt.savefig(nombre, bbox_inches='tight')
            # Cerramos la figura para que no se acumulen en memoria
            plt.close()


            frnm += 1 # incrementar el número del frame


        """
        # A partirn de las imagenes guardadas, creamos un gif

        # Modificamos la velocidad del gif para que dure 150 segundos
        # La velocidad se calcula como 1/(tiempo de cada frame)
        velocidad = 0.5
        # Creamos el gif
        with imageio.get_writer('imagen-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '.gif', mode='I', duration=velocidad) as writer:
            for filename in glob.glob('imagen-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '_*.tif'):
                print("Archivo agregado: ", filename)
                image = imageio.imread(filename)
                writer.append_data(image)
        """
        
        # Se agrupan los acrchivos .tif en un solo archivo .tif por planos.
        # Se hace uso de la libreria tifffile
        # Se crea un array con los nombres de los archivos .tif
        imagenes = glob.glob('imagen-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '_*.tif')
        # Se crea un array vacio para guardar las imagenes
        imagenes_array = []
        # Se recorre el array de los nombres de los archivos .tif
        for i in imagenes:
            # Se abre cada archivo .tif y se guarda en el array
            imagenes_array.append(tifffile.imread(i))
        # Se crea un array con los datos de las imagenes
        imagenes_array = np.array(imagenes_array)
        # Se guarda el array en un archivo .tif
        # El tipo de archivo es 16 bits
        tifffile.imsave('Stack-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '.tif', imagenes_array)
        print("Archivo .tif por planos creados")


        # Eliminamos las imagenes que se usaron para crear el gif
        for filename in glob.glob('imagen-' + str(tiempos[contador]) + '_TH-' + str(valor_Top_Hat) + '_*.tif'):
            os.remove(filename)
            print("Archivo eliminado: ", filename)

        # Nombre del archivo donde se guardará la información de la intensidad

        nombre = "intensidad" + str(tiempos[contador]) + ".txt"

        #Guardamos el array en el archivo
        np.savetxt(nombre, tintensidad, delimiter=",", fmt="%s")
        contador += 1
    
    
    # Se crea un archivo con la informacion de: valor del top hat, sigma del filtro gaussiano y si se esta aplicando un filtro de media.
    # Se guarda en un archivo txt y cada dato es un salto de linea con el nombre de la variabel primero
    # El archivo se llama nombra con los valores de los parametros y con las convenciones para los parametros: TH = Top Hat, G = Gaussiano, M = Media
    # El archivo se guarda en la carpeta de la imagen
    archivo = open("parametros.txt", "w")
    archivo.write("TH = " + str(valor_Top_Hat) + "\n")
    archivo.write("G = " + str(sigma) + "\n")
    archivo.write("M = " + str(filtroMedia) + "\n")
    archivo.close()



    end = time.time()
    print("Tiempo de ejecución: ", end - start)
    # Guardamaos la información de la intensidad, fondo y área en las matrices de información
    
    # Para la intensidad agregamos en orden al array de ceros antes creado
    #intensidad = np.concatenate((intensidad,tintensidad))
    # Para el fondo
    #intensidadFondo = np.concatenate((intensidadFondo,fondoIterado))
    # Para el area
    #area = np.concatenate((area,Intesidad_Fondo))
    
# Obtiene el directorio de trabajo actual y lo guarda en la variable directorio
directorio_trabajo = os.getcwd()

# Une el directorio con el nombre de la carpeta 'stacks' y lo guarda en la variable path_crecimiento
path_crecimiento = os.path.join(directorio_trabajo)

# Crea una lista de nombres de archivos que terminan en '.tif' en la carpeta 'stacks'
nombresCR = [os.path.join(path_crecimiento,file) for file in os.listdir(path_crecimiento) if (file.endswith('.tif') )]
nombres = sorted(nombresCR)


analisis_imagenes(10, nombres)