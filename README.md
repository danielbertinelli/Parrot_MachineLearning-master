# Parrot_MachineLearning
Control del Parrot 2.0 de ARDrone gracias a un reloj con acelerómetro (eZ430-Chronos de Texas Instruments) y machine learning
El código presente en este repositorio permite actualmente iniciar la conexión con el reloj, tomar muestras, leerlas, entrenar un algoritmo clasificador (Machine Learning) y clasificar las muestras obtenidas con el reloj.

-La carpeta libs contiene todos los scripts necesarios para realizar la adquisición de los datos, filtrado de ruido y graficado de las muestras, cortesía de Mónica Milán (@mncmilan). También contiene el gestionador.

-La carpeta CrossValidation-Metrics contiene los scripts para realizar diferentes medidas de precisión del algoritmo entrenado.

-Los archivos muestra_datos.csv y datos_muestra.csv contienen muestras guardadas de diferentes movimientos etiquetados por las cifras del 0 al 5. Siendo 0 movimento random, 1 arriba, 2 abajo, 3 giro derecha, 4 giro izquierda y 5 cambio de modo(giro completo hacia la izquierda).

-El script main contiene el programa principal, tiene dos modos [0].Predeterminado y [1]. Personalizado, el modo predeterminado se sirve de las muestras que contiene el archivo muestra_datos.csv para entrenar algoritmo y permitir el pilotaje del drone a una velocidad moderada. El modo personalizado permite al usuario construir su propias muestras para entrenar al algoritmo a la velocidad que se desee.