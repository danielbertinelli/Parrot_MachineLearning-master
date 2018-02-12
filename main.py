from libs import gestiondatos,algoritmos
from threading import Thread
import time
import numpy as np





np.random.seed(777) #Semilla aleatoria para que las pruebas de precisión sean siempre iguales

i = input('Elige entre las dos opciones: [0]Configuración predeterminada, [1]Configuración personalizada:')
i = int(i)
gestionador = gestiondatos.GestiondeDatos()

print('Cargado gestionador')
if i==0:
    print('Modo predeterminado elegido')
    modo = input('Elige entre: [0]-.Velocidad alta, [1].-Velocidad media, [2].-Velocidad baja ')
    modo = int(modo)
    if modo == 0:
        algoritmos.Algoritmos().Entrena_algoritmo('v10.csv')
        print('Algoritmo MLP entrenado')
        velocidad_adquisicion = 10
    elif modo == 1:
        algoritmos.Algoritmos().Entrena_algoritmo('v7.csv')
        print('Algoritmo MLP entrenado')
        velocidad_adquisicion = 7
    # Declaración de los hilos
    elif modo == 2:
        algoritmos.Algoritmos().Entrena_algoritmo('v4.csv')
        print('Algoritmo MLP entrenado')
        velocidad_adquisicion = 4

    peticion_aceleracion = Thread(target=gestionador.adquieredatos,args=(velocidad_adquisicion,))
    lectura_orden = Thread(target=gestionador.lee_plotea_ordena)  #

    #iniciar los hilos
    peticion_aceleracion.start()
    lectura_orden.start()





elif i ==1:
    print('Modo personalizado seleccionado')
    numero_muestras = input('A continuación se procederá a introducir las muestras personalmente, elige el número de muestras (multiplo de 6): ')
    numero_muestras = int(numero_muestras)
    velocidad = input('Introduce la velocidad de adquisición, 10-Rápido - 3-Lento:')
    velocidad = int(velocidad)
    print('El numero elegido es :'+str(numero_muestras)+' por lo tanto se introducirán '+str(numero_muestras/6)+'muestras.')
    filename = input(('Introduce el nombre del fichero:'))

    time.sleep(1)

    #Declaración de los hilos
    peticion_aceleracion = Thread(target = gestionador.adquieredatos2, args=(numero_muestras,velocidad))
    guardar = Thread(target = gestionador.lee_y_guarda, args=(numero_muestras,filename))
    print('A continuación se procede a realizar la recogida de muestras')

    peticion_aceleracion.start()
    guardar.start()
    guardar.join()

    time.sleep(3)
    print('Entrenando algoritmo')
    algoritmos.Algoritmos().Entrena_algoritmo(filename + '.csv')
    print('Algoritmo MLP entrenado')
    # Declaración de los hilos
    peticion_aceleracion2 = Thread(target=gestionador.adquieredatos,args=(velocidad,))
    lectura_orden = Thread(target=gestionador.lee_plotea_ordena)  #

    # iniciar los hilos
    var = input('Pulsa enter para comenzar a pilotar el drone')
    peticion_aceleracion2.start()
    print('Iniciada la adquisición de movimientos')
    lectura_orden.start()
    print('Iniciada la clasificación de movimientos')


