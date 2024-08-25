import sys
from matplotlib import pyplot as plt
import numpy as np

from pyPRUF.membership_functions import MembershipFunction, Trapezoidal, Triangular

def plot_function(f, x_range=(-1000, 1000), num_points=1000, title="Grafico della funzione"):
    """
    Plotta il grafico di una funzione data.
    
    Parametri:
    f (function): La funzione da plottare. Deve essere una funzione di una variabile reale.
    x_range (tuple): Una tupla (min, max) che definisce l'intervallo dell'asse x.
    num_points (int): Il numero di punti da plottare tra x_range[0] e x_range[1].
    title (str): Il titolo del grafico.
    """
    x = np.linspace(x_range[0], x_range[1], num_points, dtype=float)
    y = [f(value) for value in x]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_function(f = Triangular(-MembershipFunction.INF, 50.0, 150.0),
            title = 'Triangular(-Inf, b, c)')

plot_function(f = Triangular(-50.0, 50.0, MembershipFunction.INF),
            title = 'Triangular(a, b, Inf)')

plot_function(f = Triangular(-50.0, 50.0, 150.0),
            title = 'Triangular(a, b, c)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -MembershipFunction.INF, 50.0, 150.0),
            title = 'Trapezoidal(-Inf, -Inf, c, d)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -50.0, 50.0, 150.0),
            title = 'Trapezoidal(-Inf, b, c, d)')

plot_function(f = Trapezoidal(-200.0, -100.0, 100.0, 200.0),
                title = 'Trapezoidal(a, b, c, d)')

plot_function(f = Trapezoidal(20.0, 50.0, 100.0, MembershipFunction.INF),
                title = 'Trapezoidal(a, b, c, Inf)')

plot_function(f = Trapezoidal(20.0, 50.0, MembershipFunction.INF, MembershipFunction.INF),
                title = 'Trapezoidal(a, b, Inf, Inf)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -100.0, 100.0, MembershipFunction.INF),
                title = 'Trapezoidal(-Inf, b, c, Inf)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -MembershipFunction.INF, 100.0, MembershipFunction.INF),
                title = 'Trapezoidal(-Inf, -Inf, c, Inf)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -100.0, MembershipFunction.INF, MembershipFunction.INF),
                title = 'Trapezoidal(-Inf, b, Inf, Inf)')

plot_function(f = Trapezoidal(-MembershipFunction.INF, -MembershipFunction.INF, MembershipFunction.INF, MembershipFunction.INF),
                title = 'Trapezoidal(-Inf, -Inf, Inf, Inf)')