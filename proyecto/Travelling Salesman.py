# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: 'Python 3.9.4 64-bit (''AnAp'': conda)'
#     name: python394jvsc74a57bd0b51b1ace3c01efe6b1476470ed0211d96a9adc30e31e28e4cb788503ec9588a6
# ---

import matplotlib
import matplotlib.pyplot as plt

# +
import numpy as np
import numpy.linalg as la

matplotlib.use("module://matplotlib-backend-kitty")

np.set_printoptions(threshold=0)

# %matplotlib inline
# -

cities = np.genfromtxt("csv/Qatar.csv", delimiter=",")
cities = cities[1:, 1:]
n_cities = cities.shape[0]
cities

plt.scatter(cities[:, 0], cities[:, 1], marker=".")


def d(i, j):
    return np.linalg.norm(cities[i, :] - cities[j, :])


d(0, 1)


class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = sum(
            [d(genome[i], genome[i + 1]) for i in range(0, len(genome) - 1)]
        ) + d(genome[len(genome) - 1], genome[0])

    # Muta al individuo
    def mutate(self):
        genome = np.copy(self.genome)
        i, j = np.random.choice(len(genome), size=2, replace=False)
        genome[i], genome[j] = genome[j], genome[i]
        return Individual(genome)

    # Two point crossover
    def cross(self, q):
        child = np.copy(self.genome)
        start, end = np.sort(np.random.choice(len(child), size=2, replace=False))
        child[:start] = child[end + 1 :] = -1
        child[child == -1] = np.setdiff1d(q.genome, child, assume_unique=True)
        return Individual(child)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __repr__(self):
        return "Individual(genome: {0}, fitness: {1})".format(
            self.genome.__str__(), self.fitness
        )


i = Individual(np.array([0, 5, 10, 15]))
i.fitness

o = i.mutate()
o.genome, o.fitness, i.genome, i.fitness

a = Individual(np.array([1, 2, 3, 4, 5]))
b = Individual(np.array([2, 1, 3, 5, 4]))
c = a.cross(b)
a.genome, b.genome, c.genome


# DEPRECATED: Lo generaliza greedy_popuation con ratio=0
def random_population(n_population):
    # TODO: Generar individuos aleatorios
    return np.array(
        [Individual(np.random.permutation(n_cities)) for _ in range(n_population)]
    )


def greedy_popuation(n_population, ratio=1 / 2):
    """
    Genera población parte aleatoria parte generada mediante nearest neighbours

    Args:
        n_population: Tamaño total de la población
        ratio: Qué porcentaje de la población se genera greedily. 0 -> toda random
    """
    # Guardamos la población generada en population
    population = []

    # Primero generamos los de nearest neighbours
    n_greedy = round(n_population * ratio)
    n_random = n_population - n_greedy

    for _ in range(n_greedy):
        # Anotamos las ciudades visitadas modificando una copia de la lista de ciudades. Las
        # visitadas se vuelven nan. Asi se excluyen del cálculo de distancias.
        visitados = []
        index = range(len(cities))
        # Elegimos ciudad al azar
        curr_city = np.random.randint(0, len(cities))
        visitados.append(curr_city)
        city_record = np.copy(cities)

        while len(visitados) != len(index):
            city_record[curr_city] = np.nan

            distancias = la.norm(city_record - cities[curr_city], axis=1)
            # Tomamos la ciudad más cercana como actual
            curr_city = np.nanargmin(distancias)
            visitados.append(curr_city)

        # Añadiendo el individuo a la población
        population.append(Individual(visitados))

    # Generamos el resto de la población aleatoriamente
    population = population + [
        Individual(np.random.permutation(n_cities)) for _ in range(n_random)
    ]

    return np.array(population)


# El de menor fitness es el que tiene más probabilidades de reproducirse
def calculate_wheel_probability(population):
    fitnesses = np.array([p.fitness for p in population])
    # fitnesses = np.min(fitnesses) + np.max(fitnesses) - fitnesses
    # return fitnesses / np.sum(fitnesses)
    fitnesses = np.max(fitnesses) + 1 - fitnesses
    s = np.sum(fitnesses)
    return fitnesses / s


calculate_wheel_probability([i, o])


def GA(
    n_population=100,
    n_generation=1000,
    cross_rate=0.3,
    mutate_rate=0.2,
    greedy_rate=0,
    verbose=False,
    print_interval=10,
):
    """
    Resuelve el problema del agente viajero mediante una versión modificada de la estrategia del 
    algoritmos genéticos. Se genera una población del tamaño especificado y con las características 
    de aleatoriedad deseadas.

    Args:
        n_population: Tamaño total de la población
        n_generation: Número de generaciones
        cross_rate:
        mutate_rate:
        greedy_rate: Porcentaje de la población inicial que se genera mediante nearest neighbours
        verbose: Controla la cantidad de información que imprime el algoritmo
    """
    # Para la generación 0
    # Pk = random_population(n_population)
    Pk = greedy_popuation(n_population, greedy_rate)
    best_individual = Pk[Pk.argmin()]
    for k in range(1, n_generation):
        # Creamos la siguiente generacion
        Pk_next = np.array([])
        # Para seleccionar usamos wheel roulette selection
        # Calculamos la wheel probability
        wheel_prob = calculate_wheel_probability(Pk)

        # 1. Copy: seleccionamos (1 − cross_rate) × n individuos de Pk y los insertamos en Pk+1
        Pk_next = np.append(
            Pk_next,
            np.random.choice(
                Pk, round((1 - cross_rate) * n_population), p=wheel_prob, replace=False
            ),
        )

        # 2. Crossover: seleccionamos (cross_rate * n) parejas de Pk y los cruzamos para añadirlos en Pk+1
        parejas = np.random.choice(
            Pk, 2 * round(cross_rate * n_population), p=wheel_prob, replace=False
        ).reshape(-1, 2)
        Pk_next = np.append(Pk_next, [p.cross(q) for p, q in parejas])

        # 3. Mutate: seleccionamos mutate_rate de la población Pk+1 y la mutamos
        mutate_index = np.random.choice(
            len(Pk_next), int(mutate_rate * len(Pk_next)), replace=False
        )
        Pk_next[mutate_index] = np.array([x.mutate() for x in Pk_next[mutate_index]])

        # Acualizamos la generación
        Pk = Pk_next
        if Pk[Pk.argmin()] < best_individual:
            best_individual = Pk[Pk.argmin()]

        # Imprimimos status
        if verbose is True or k % print_interval == 0:
            print(f"Generation {k}: {best_individual}")
            # print(Pk)

    return best_individual


GA(n_population=20, n_generation=10, verbose=True)

# + tags=[]
GA(n_population=20, n_generation=10, greedy_rate=1 / 5, verbose=True)
# -

