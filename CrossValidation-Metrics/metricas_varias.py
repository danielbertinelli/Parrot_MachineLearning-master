from sklearn.metrics import classification_report
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
import sys
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.model_selection import cross_val_score, cross_val_predict, ShuffleSplit, train_test_split, validation_curve, StratifiedKFold
np.random.seed(5)

#Datos de la base de datos para realizar la clasificación
datos = np.genfromtxt('v8.csv', delimiter = ';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]
x_train, x_eval, y_train, y_eval = train_test_split(digitos, etiquetas, test_size=0.5,
                                                    train_size=0.5,
                                                    random_state=1982)
tiempo_inicial = time.time()
scaler = StandardScaler()
scaler.fit(x_train)
X_train = scaler.transform(x_train)
X_test = scaler.transform(x_eval)
#Creamos clasificador

clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, max_iter=9, hidden_layer_sizes=12)
clf_decisiontree = DecisionTreeClassifier(max_depth=7, min_samples_leaf=1)



clf_neuronal.fit(X_train, y_train)

tiempo_transcurrido = time.time()-tiempo_inicial

print('Tiempo para MLP:'+str(tiempo_transcurrido))

tiempo_inicial2 = time.time()

clf_decisiontree.fit(x_train,y_train)

tiempo_transcurrido2 = time.time()-tiempo_inicial2
print('Tiempo para DT:'+str(tiempo_transcurrido2))

#Obtenemos los aciertos que tienen cada uno de los clasificadores

expected = y_eval
predicted_neu = clf_neuronal.predict(X_test)
predicted_tree = clf_decisiontree.predict(x_eval)

print("Report de clasificación para MLP Classifier:\n\%s\n"
       %(metrics.classification_report(expected, predicted_neu)))
print("Report de clasificación para Decision Tree:\n%s\n"
       %(metrics.classification_report(expected, predicted_tree)))

# #Matrices de Confusión
#
print("Confusion matrix Decision Tree:\n%s" % metrics.confusion_matrix(expected, predicted_tree))
print("Confusion matrix MLP Classifier:\n%s" % metrics.confusion_matrix(expected, predicted_neu))

#crossvalidation scores
cv1 = cross_val_score(clf_neuronal, X_test, y_eval, cv=3)
cv2 = cross_val_score(clf_decisiontree, x_eval, y_eval, cv=3)


#print('Scores validación cruzada: Stump:'+str(cv1) +' Tree:'+str(cv2)+' AdaBoost Discreto:'+str(cv3)+' GradientBoost:'+str(cv4))
print("Precisión Nueronal: %0.2f (+/- %0.2f)" % (cv1.mean(), cv1.std() * 2))
print("Precisión Tree: %0.2f (+/- %0.2f)" % (cv2.mean(), cv2.std() * 2))



# precision = []
# for k, (train, test) in enumerate(kpliegues):
#     clf_neuronal.fit(X_train[train], y_train[train])
#     score = clf_neuronal.score(x_train[test], y_train[test])
#     precision.append(score)
#     print('Pliegue: {0:}, Dist Clase: {1:}, Prec: {2:.3f}'.format(k+1,
#                         np.bincount(y_train[train]), score))
#
# # imprimir promedio y desvio estandar
# print('Precision promedio Neuronal: {0: .3f} +/- {1: .3f}'.format(np.mean(precision),
#                                           np.std(precision)))
