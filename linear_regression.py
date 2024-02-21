import numpy as np


class SimpleLinearRegression:
    def __init__(self):
        self.intercept_ = None
        self.coef_ = None
        self.X = None

    def fit(self, x, y):
        # Dodaj kolumnę jedynek do macierzy X, aby uwzględnić wyraz wolny w równaniu liniowym
        self.X = np.c_[np.ones((x.shape[0], 1)), x]

        # Oblicz współczynniki regresji liniowej
        theta = np.linalg.inv(self.X.T.dot(self.X)).dot(self.X.T).dot(y)

        # Pierwszy element wektora theta to wyraz wolny, a pozostałe to współczynniki
        self.intercept_ = theta[0]
        self.coef_ = theta[1:]

    def predict(self, x):
        X = np.c_[np.ones((x.shape[0], 1)), x]
        y_pred = X.dot(np.hstack(([self.intercept_], self.coef_)))

        return y_pred
