import numpy as np
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import time
from sklearn.model_selection import cross_val_score
tiempo_inicial = time.time()
scaler = StandardScaler()

np.random.seed(777)

# Creación del clasificador y entrenamiento
clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, max_iter=26,
                             hidden_layer_sizes=12)

#clf_neuronal = DecisionTreeClassifier()
class Algoritmos():

    # Entrenamiento del algoritmo clasificador
    def Entrena_algoritmo(self, filename):
        # Datos de la base de datos para realizar la clasificación
        datos = np.genfromtxt(filename, delimiter=';')
        digitos = normalize(datos[:, :-1])
        etiquetas = datos[:, -1]
        x_train, x_eval, y_train, y_eval = train_test_split(digitos, etiquetas, test_size=0.5,
                                                            train_size=0.5,
                                                            random_state=1982)

        scaler.fit(x_train)
        X_train = scaler.transform(x_train)
        X_test = scaler.transform(x_eval)

        # Creación del clasificador y entrenamiento


        clf_neuronal.fit(X_train, y_train)
        cv1 = cross_val_score(clf_neuronal, X_test, y_eval, cv=3)
        print("Precisión Neuronal: %0.2f (+/- %0.2f)" % (cv1.mean(), cv1.std() * 2))

    # Método para realizar las clasificaciones
    def Clasificador(self, iteracion,digitos_prediccion):
        test_data = normalize(digitos_prediccion[0 + (30 * (iteracion)):30 + ((iteracion) * 30)])
        test_data = scaler.transform(test_data)
        t=time.time()
        prediccion = clf_neuronal.predict(test_data)
        print('Tiempo de predicción:'+str(time.time()-t))
        return prediccion


