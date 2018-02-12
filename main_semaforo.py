from libs import communications,semaforo

c = communications.CommunicationManager()
c.open_serial_port()

# main

var = input('Elige entre : [0] Modo de vuelo, [1] Modo sin vuelo, [2] Introducir datos.')
var = int(var)
if var == 1:
    modo = input('Elige entre: [0]-.Velocidad alta, [1].-Velocidad media, [2].-Velocidad baja ')
    modo = int(modo)
    if modo == 0:
        velocidad = 10
        filename = 'v10'
    if modo == 1:
        velocidad = 7
        filename = 'v7'
    if modo == 2:
        velocidad = 4
        filename = 'v4'
    thread_adquisicion = semaforo.Thread_Adquisicion(velocidad)
    thread_lectura = semaforo.Thread_Lectura(filename)
    input('Pulsa enter para empezar.')
    thread_adquisicion.start()
    thread_lectura.start()

elif var == 0:
    modo = input('Elige entre: [0]-.Velocidad alta, [1].-Velocidad media, [2].-Velocidad baja ')
    modo = int(modo)
    if modo == 0:
        velocidad = 10
        filename = 'v10'
    if modo == 1:
        velocidad = 7
        filename = 'v7'
    if modo == 2:
        velocidad = 4
        filename = 'v4'
    thread_adquisicion = semaforo.Thread_Adquisicion(velocidad)
    thread_orden = semaforo.Thread_Orden(filename)
    input('Pulsa enter para empezar.')
    thread_adquisicion.start()
    thread_orden.start()

elif var == 2:
    numero_muestras = input('A continuación se procederá a introducir las muestras personalmente, elige el número de muestras (multiplo de 6): ')
    numero_muestras = int(numero_muestras)
    velocidad = input('Introduce la velocidad de adquisición, 10-Rápido - 3-Lento:')
    velocidad = int(velocidad)
    print('El numero elegido es :'+str(numero_muestras)+' por lo tanto se introducirán '+str(numero_muestras/6)+'muestras.')
    filename = input(('Introduce el nombre del fichero:'))
    thread_adquisicion2 = semaforo.Thread_Adquisicion2(numero_muestras,velocidad)
    thread_guardar = semaforo.Thread_Guardado(numero_muestras,filename)
    input('Pulsa enter para empezar')
    thread_adquisicion2.start()
    thread_guardar.start()
