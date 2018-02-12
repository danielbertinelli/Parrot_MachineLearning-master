print(__doc__)

from sklearn.preprocessing import normalize
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import datasets


vector_barrido = []
mlp = MLPClassifier(solver='lbfgs', early_stopping=False)
datos = np.genfromtxt('muestra_datos.csv', delimiter = ';')
X = (datos[:, :-1])
y = datos[:, -1]
for i in range(100):
    i+=1
    vector_barrido.append(i)
maxiter = vector_barrido

scores = list()
scores_std = list()
for mi in maxiter:
    mlp.max_iter = mi
    this_scores = cross_val_score(mlp, X, y, n_jobs=1)
    scores.append(np.mean(this_scores))
    scores_std.append(np.std(this_scores))

# Do the plotting
import matplotlib.pyplot as plt
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.plot(maxiter, scores, label='CV score')
plt.plot(maxiter, np.array(scores) + np.array(scores_std), 'b--',label='CV máx score')
plt.plot(maxiter, np.array(scores) - np.array(scores_std), 'b--',label='CV min score')
plt.legend()
locs, labels = plt.yticks()
plt.yticks(locs, list(map(lambda x: "%g" % x, locs)))
plt.ylabel('CV score')
plt.xlabel('Máx. Iterations')
plt.ylim(0, 1.1)
plt.show()