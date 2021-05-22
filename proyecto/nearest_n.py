# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
# ---

from IPython import get_ipython

# %%
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as la

# Inutil en notebook es para vim
matplotlib.use("module://matplotlib-backend-kitty")

# Ejemplo de juguete
n_cities = 30

x = np.asarray(range(int(-n_cities / 2), int(n_cities / 2) + 1, 1))
y = np.sqrt(n_cities ** 2 / 4 - x ** 2)

cities = np.asarray(list(zip(x, y)))

# %% [markdown]
# Idea: Tomo una ciudad aleatoriamente, calculo la distancia a el resto de las ciudades como una
# función vectorizada sobre todo cities, tomo argmin, y asi sucesivamente.
# Para ir descartando ciudades las vamos marcando como nan para que no entrene en el cálculo de la
# norma

# %%
# Lista de las visitadas
visitados = []
index = range(len(cities))

# Index aleatorio de la primera ciudad
curr_city = np.random.randint(0, len(cities))
visitados.append(curr_city)

# Hacemos copia de cities para no desmadrarlo
cities2 = np.copy(cities)

# for c in range(len(cities) - 1):
while len(visitados) != len(index):
    # Marcamos la ciudad actual como visitada
    # Asi se descarta del cálculo
    cities2[curr_city] = np.nan

    # De las ciudades que no son nan, obtenemos la más cercana
    distancias = la.norm(cities2 - cities[curr_city], axis=1)

    # Tomamos la ciudad más cercana como la actual (exluyendo nan)
    curr_city = np.nanargmin(distancias)
    visitados.append(curr_city)

# %% [makdown]
# Graficando para ver si hace sentido

# %%
plt.plot(cities[:, 0], cities[:, 1])
plt.plot(cities[visitados, 0], cities[visitados, 1], "*-")
plt.show()

print(visitados)
