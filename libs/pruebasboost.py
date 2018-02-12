import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
import sys


#Imports relacionados con Machine Learning, métricas,preprocesado de datos..clasificadores.
from sklearn.preprocessing import normalize
from sklearn.model_selection import cross_val_score, cross_val_predict, ShuffleSplit, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier

#Datos de la base de datos para realizar la clasificación
datos = np.genfromtxt('muestra_datos.csv', delimiter = ';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]

x_train, x_eval, y_train, y_eval = train_test_split(digitos, etiquetas, test_size=0.3,
                                                    train_size=0.7,
                                                    random_state=1982)
n_estimators = 400

#Instancias de los clasificadores y entrenamiento
clf_stump = DecisionTreeClassifier(max_depth=1, min_samples_leaf=1) #Stump significa tocón
clf_stump.fit(x_train, y_train)
clf_stump_err = 1-clf_stump.score(x_eval, y_eval)
print('Error del tocón'+str(clf_stump_err))
clf_tree = DecisionTreeClassifier(max_depth=9, min_samples_leaf=1)
clf_tree.fit(x_train, y_train)
clf_tree_err = 1-clf_tree.score(x_eval, y_eval)
print('Error del árbol de decisión'+str(clf_tree_err))
clf_adaBoostdis = AdaBoostClassifier(base_estimator=clf_stump, learning_rate=1, n_estimators=n_estimators, algorithm="SAMME") #AdaBoost discreto
clf_adaBoostreal = AdaBoostClassifier(base_estimator=clf_stump, learning_rate=1, n_estimators=n_estimators, algorithm="SAMME.R")
clf_adaBoostdis.fit(x_train, y_train)
clf_adaBoostreal.fit(x_train, y_train)

#plots
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([1, n_estimators], [clf_stump_err] * 2, 'k-',
        label='Decision stump Error')
ax.plot([1, n_estimators], [clf_tree_err] * 2, 'k--',
        label='Decision Tree Error')

#Errores del AdaBoost real y discreto para los valores de entrenamiento y de testeo
ada_discrete_err = np.zeros((n_estimators,))
for i, y_pred in enumerate(clf_adaBoostdis.staged_predict(x_eval)):
    ada_discrete_err[i] = zero_one_loss(y_pred, y_eval)
#print('AdaBdiscrete eval'+str(ada_discrete_err))
ada_discrete_err_train = np.zeros((n_estimators,))
for i, y_pred in enumerate(clf_adaBoostdis.staged_predict(x_train)):
    ada_discrete_err_train[i] = zero_one_loss(y_pred, y_train)
#print(('AdaBdiscrete train'+str(ada_discrete_err_train)))
ada_real_err = np.zeros((n_estimators,))
for i, y_pred in enumerate(clf_adaBoostreal.staged_predict(x_eval)):
    ada_real_err[i] = zero_one_loss(y_pred, y_eval)
#print('AdaBreal eval'+str(ada_real_err))
ada_real_err_train = np.zeros((n_estimators,))
for i, y_pred in enumerate(clf_adaBoostreal.staged_predict(x_train)):
    ada_real_err_train[i] = zero_one_loss(y_pred, y_train)

#print('AdaBreal train'+str(ada_real_err_train))
ax.plot(np.arange(n_estimators) + 1, ada_discrete_err,
        label='Discrete AdaBoost Test Error',
        color='red')
ax.plot(np.arange(n_estimators) + 1, ada_discrete_err_train,
        label='Discrete AdaBoost Train Error',
        color='blue')
ax.plot(np.arange(n_estimators) + 1, ada_real_err,
        label='Real AdaBoost Test Error',
        color='orange')
ax.plot(np.arange(n_estimators) + 1, ada_real_err_train,
        label='Real AdaBoost Train Error',
        color='green')

ax.set_ylim((0.0, 1))
ax.set_xlabel('n_estimators')
ax.set_ylabel('error rate')

leg = ax.legend(loc='upper right', fancybox=True)
leg.get_frame().set_alpha(0.7)

plt.show()
