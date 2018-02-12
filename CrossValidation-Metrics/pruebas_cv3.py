from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize, StandardScaler

np.random.seed(10)
datos = np.genfromtxt('muestra_datos.csv', delimiter = ';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]
vector_barrido=[]
i=1
for i in range(25):
    i+=1
    vector_barrido.append(i)

print(vector_barrido)
X_train, X_test, y_train, y_test = train_test_split(
    digitos, etiquetas, test_size=0.5, random_state=5)
parameters = {'max_iter': vector_barrido , 'hidden_layer_sizes': vector_barrido}
skf = StratifiedKFold(n_splits=2, random_state=5)
mlp = MLPClassifier(solver='lbfgs', early_stopping=False)
clf = GridSearchCV(mlp, parameters,cv=skf)
clf.fit(X_train,y_train)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))
print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))
print()

#print(X_train)