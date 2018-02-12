from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import normalize, StandardScaler
import numpy as np
import time
import sys
from sklearn import metrics

#Datos de la base de datos para realizar la clasificación
datos = np.genfromtxt('muestra_datos.csv', delimiter = ';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]


scaler = StandardScaler()
scaler.fit(digitos)
X_train = scaler.transform(digitos)


clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, max_iter=9, hidden_layer_sizes=12)
clf_decisiontree = DecisionTreeClassifier(max_depth=7, min_samples_leaf=1)


scores_neuronal = cross_val_score(clf_neuronal, X_train, etiquetas, cv=5)
scores_decisiontree = cross_val_score(clf_decisiontree,X_train,etiquetas,cv=5)


print('Cross Validation Scores MLP: '+str(scores_neuronal))
print('Cross Validation Scores DT: '+str(scores_decisiontree))


clf_neuronal.fit(X_train,etiquetas)
clf_decisiontree.fit(X_train,etiquetas)

# scores_neuronal1 = cross_val_score(clf_neuronal, X_train, etiquetas, cv=5)
# scores_decisiontree1 = cross_val_score(clf_decisiontree,X_train,etiquetas,cv=5)

# print('Cross Validation Scores MLP Entrenado: '+str(scores_neuronal1))
# print('Cross Validation Scores DT Entrenado: '+str(scores_decisiontree1))
