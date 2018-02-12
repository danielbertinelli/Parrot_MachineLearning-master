import time
import warnings
from libs import communications, filterings,algoritmos
from pyardrone import ARDrone
from pygame import mixer
import sys


warnings.filterwarnings("ignore", category=DeprecationWarning)
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()


clasificador = algoritmos.Algoritmos()
communication.open_serial_port()
drone=ARDrone()
old_prediction = []
old_prediction.append(0)
x = []
y = []
z = []
digitos_prediccion = []
digitos_prediccion2 = []
muestras = []
vectorguardado=[]

class GestiondeDatos():
    # Método para realizar peticiones de aceleración y esperar cuando se procese una muestra

    def adquieredatos2(self,n_muestras,velocidad):
        vlcty = 1/velocidad
        while (len(digitos_prediccion)) < n_muestras * 30:
            communication.send_data_request()
            time.sleep(vlcty)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(0.11)

        print('Fin de la adquisición')

    def adquieredatos(self,velocidad):
        vlcty = 1/velocidad
        print('Velocidad '+str(vlcty))
        tiempo_inicial_adquisicion = time.time()
        while (time.time() - tiempo_inicial_adquisicion) <= 1300:
            communication.send_data_request()
            time.sleep(vlcty)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(0.5)




    # Método para leer los datos del reloj y guardarlos en un fichero con etiqueta
    def lee_y_guarda(self,n_muestras,filename):

        archi = open(filename + '.csv', 'a')
        print('Guardando datos')
        print('Numero de muestras input' + str(n_muestras))
        n_iteraciones = 0
        contador = -1
        while len(digitos_prediccion)< n_muestras*30:
            bytestoread, inbyte = communication.read_data()
            if (bytestoread == 7) or (bytestoread == 14):
                contador += 1
                print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                    bytestoread))
                x.append((inbyte[bytestoread - 3]))
                y.append((inbyte[bytestoread - 2]))
                z.append((inbyte[bytestoread - 1]))
                digitos_prediccion.append(x[contador])
                digitos_prediccion.append(y[contador])
                digitos_prediccion.append(z[contador])
                print('X: ' + str(x[contador]) + 'Y: ' + str(y[contador]))
                print('contador de thread 2 ' + str(contador))
                print('contador de iteraciones ' + str(n_iteraciones))
                if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                    muestra_guardar = digitos_prediccion[0 + (30 * (n_iteraciones)):30 + ((n_iteraciones) * 30)]
                    n_iteraciones = n_iteraciones + 1
                    if n_iteraciones<= n_muestras/6:  #Los movimientos aleatorios
                        muestra_guardar.append(0)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/6:
                            var = input('El próximo movimiento es hacia arriba')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras/3 and n_iteraciones>n_muestras/6 :  #Los movimientos hacia arriba
                        muestra_guardar.append(1)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/3:
                            var = input('El próximo movimiento es hacia abajo')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras/2 and n_iteraciones>n_muestras/3:  #Los movimientos hacia abajo
                        muestra_guardar.append(2)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/2:
                            var = input('El próximo movimiento es hacia la derecha')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras*4/6 and n_iteraciones>n_muestras/2 :  #Los movimientos hacia la derecha
                        muestra_guardar.append(3)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras*4/6:
                            var = input('El próximo movimiento es hacia la izquierda')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

                    if n_iteraciones<= n_muestras*5/6 and n_iteraciones>n_muestras*4/6 :  #Los movimientos hacia la derecha
                        muestra_guardar.append(4)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras*5/6:
                            var = input('El próximo movimiento es de cambio de modo')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

                    if n_iteraciones<= n_muestras and n_iteraciones>n_muestras*5/6 :  #Los movimientos de cambio de modo
                        muestra_guardar.append(5)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras:
                            print('Final de la recogida de muestras')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

        print('Fichero Guardado')
        print('Vector a guardar: '+str(vectorguardado))
        digitos_prediccion.clear()

        for i in range(len(vectorguardado)):
            vector_aux = vectorguardado[i]
            filtering.filter_aceleration_pro(vector_aux,True)
            for j in range(len(vector_aux)):
                if j%30==0 and j !=0:

                    archi.write(str(vector_aux[j]))
                else:
                    archi.write(str(vector_aux[j]) + ';')
            archi.write('\n')



#Metodo para leer y clasificarr las muestras
    def leedatos(self):
        print(str(digitos_prediccion))
        contador = -1
        tiempo_inicial_lectura = time.time()


        while (time.time() - tiempo_inicial_lectura) <= 1300:
            bytestoread, inbyte = communication.read_data()

            if (bytestoread == 7) or (bytestoread == 14):
                contador += 1
                print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                    bytestoread))
                x.append((inbyte[bytestoread - 3]))
                y.append((inbyte[bytestoread - 2]))
                z.append((inbyte[bytestoread - 1]))
                digitos_prediccion.append(x[contador])
                digitos_prediccion.append(y[contador])
                digitos_prediccion.append(z[contador])
                print('Longitud de digitos de prediccion'+ str(len(digitos_prediccion)))
                print('contador de thread 2 ' + str(contador))
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(1)




    # #Metodo para clasificar
    def clasifica_muestras(self):
        mixer.init()
        alertamovimiento = mixer.Sound("DeskBell.wav")
        alertamal = mixer.Sound("buzzer.wav")
        alertamodo = mixer.Sound("ding.wav")
        n_iteraciones = 0
        t=time.time()
        while time.time()-t<=1300:
            try:

                if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                    print('DENTRO DE CLASIFICADOR' +str(len(digitos_prediccion)))
                    filtering.filter_aceleration_pro(digitos_prediccion,False)
                    prediccion = clasificador.Clasificador(n_iteraciones, digitos_prediccion)
                    n_iteraciones = n_iteraciones + 1

                    if prediccion == 1:
                        print('arriba')
                        alertamovimiento.play()

                    if prediccion == 2:
                        print('abajo')
                        alertamovimiento.play()

                    if prediccion == 3:
                        print('derecha')
                        alertamovimiento.play()

                    if prediccion == 4:
                        print('izquierda')
                        alertamovimiento.play()

                    if prediccion == 5:
                        print('modo2')
                        alertamodo.play()

                    if prediccion == 0:
                        print('random')
                        alertamal.play()

            except:
                time.sleep(0.4)# alertamovimiento.play()
            time.sleep(1)
        time.sleep(0.4)
        print(digitos_prediccion)





    # Método para leer los datos, clasificarlos y ejecutar ordenes del dron
    def lee_plotea_ordena(self):
        contador = -1
        tiempo_inicial_lectura = time.time()
        n_iteraciones = 0
        mixer.init()
        alertamovimiento = mixer.Sound("DeskBell.wav")
        alertamal = mixer.Sound("buzzer.wav")
        alertamodo=mixer.Sound("ding.wav")


        drone.trim()
        modo = True  # Por defecto esta en vertical pues al inicio el dron esta en el suelo.

        drone.navdata_ready.wait()
        drone.set_navdata_available()
        navdata = drone.get_navdata()
        bateria = navdata.vbat_flying_percentage

        while (time.time() - tiempo_inicial_lectura) <= 1300:
            bytestoread, inbyte = communication.read_data()

            if (bytestoread == 7) or (bytestoread == 14):
                contador += 1
                print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                    bytestoread))
                x.append((inbyte[bytestoread - 3]))
                y.append((inbyte[bytestoread - 2]))
                z.append((inbyte[bytestoread - 1]))

                filtering.filter_acceleration(x, contador)
                filtering.filter_acceleration(y, contador)
                filtering.filter_acceleration(z, contador)
                digitos_prediccion.append(x[contador])
                digitos_prediccion.append(y[contador])
                digitos_prediccion.append(z[contador])
                print('X: ' + str(x[contador]) + 'Y: ' + str(y[contador]))
                print('contador de thread 2 ' + str(contador))
                print('contador de iteraciones ' + str(n_iteraciones))
                cont_predicciones = 0

                if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                    prediccion = clasificador.Clasificador(n_iteraciones,digitos_prediccion)
                    n_iteraciones = n_iteraciones + 1
                    print('Bateria =' + str(bateria))
                    print(old_prediction)
                    print('contador predicciones : '+str(cont_predicciones))
                    if prediccion == 1:
                        print('arriba')

                        if modo == True:  # movimientos verticales
                            if drone.state.fly_mask == False and old_prediction[cont_predicciones - 1] == 1:  # está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
                                drone.takeoff()
                                time.sleep(3.5)
                                alertamovimiento.play()
                                time.sleep(0.15)
                            else:  # dron esta volando
                                timex = time.time()
                                while time.time() - timex <= 0.8:
                                    drone.move(up=0.7)
                                alertamovimiento.play()
                                time.sleep(0.15)
                        else:  # movimientos plano horizontal
                            if drone.state.fly_mask == True:  # está volando
                                time1 = time.time()
                                while time.time() - time1 <= 1:
                                    drone.move(backward=0.15)
                                alertamovimiento.play()
                                time.sleep(0.15)
                        cont_predicciones += 1

                    elif prediccion == 2:
                        print('abajo')


                        if modo == True:  # movimientos verticales
                            timex2 = time.time()
                            while time.time() - timex2 <= 0.8:
                                drone.move(down=0.7)
                            alertamovimiento.play()
                            time.sleep(0.15)
                        else:  # movimientos horizontales
                            if drone.state.fly_mask == True:  # volando
                                time1 = time.time()
                                while time.time() - time1 <= 1:
                                    drone.move(forward=0.15)
                                alertamovimiento.play()
                                time.sleep(0.15)
                        cont_predicciones += 1

                    elif prediccion == 3:
                        print('derecha')
                        cont_predicciones += 1
                        if modo==True:
                            time2 = time.time()
                            while time.time() - time2 <= 1:
                                drone.move(right=0.1)
                            alertamovimiento.play()
                            time.sleep(0.15)
                        else:
                            time3 = time.time()
                            while time.time()-time3<=1:
                                drone.move(cw=0.3)
                            alertamovimiento.play()
                            time.sleep(0.15)


                    elif prediccion == 4:
                        print('izquierda')
                        cont_predicciones += 1
                        if modo == True:
                            time1 = time.time()
                            while time.time() - time1 <= 1:
                                drone.move(left=0.1)
                            alertamovimiento.play()
                            time.sleep(0.15)
                        else:
                            time1=time.time()
                            while time.time()-time1 <= 1:
                                drone.move(ccw=0.3)
                            alertamovimiento.play()
                            time.sleep(0.15)

                    if prediccion == 5:
                        print('modo2')
                        if drone.state.fly_mask == True and old_prediction[cont_predicciones - 1] == 5:
                            drone.land()
                            alertamodo.play()
                            time.sleep(0.1)
                            print()
                            print('Fin del vuelo.')
                            sys.exit()

                        else:
                            modo = not modo
                            alertamodo.play()
                            time.sleep(0.15)
                        cont_predicciones += 1

                    elif prediccion == 0:
                        print('random')
                        alertamal.play()
                        time.sleep(0.15)
                        cont_predicciones += 1
                    if cont_predicciones >= 1:
                        old_prediction.append(int(prediccion))
        print(digitos_prediccion)
        drone.land()

