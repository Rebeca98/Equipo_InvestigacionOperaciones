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
#     name:
#     python394jvsc74a57bd0b51b1ace3c01efe6b1476470ed0211d96a9adc30e31e28e4cb788503ec9588a6
# ---

# +
import matplotlib
import tikzplotlib
import matplotlib.pyplot as plt

matplotlib.use("pgf")

plt.rcParams.update(
    {"pgf.texsystem": "pdflatex", "font.family": "serif", "font.serif": []}
)

plt.style.use("ggplot")

# +
import numpy as np
import numpy.linalg as la

# matplotlib.use("module://matplotlib-backend-kitty")

# np.set_printoptions(threshold=0)
np.random.seed(42)

# %matplotlib inline
# -

# Obtenemos las ciudades de los datos dados para el proyecto procesados
cities = np.genfromtxt("csv/Qatar.csv", delimiter=",")
cities = cities[1:, 1:]
n_cities = cities.shape[0]
n_cities

# +
# Mapa del país
plt.scatter(cities[:, 0], cities[:, 1], marker="*")
plt.title("Localizacion de ciudades (Qatar)")

plt.savefig("qatar.pdf")


# -
def d(i, j):
    """
    Función de distancia entre las ciudades i,j calculada como la norma de la diferencia
    entre los vectores de coordenadas de las ciudades.

    Args:
        i,j: Ints que funcionen como índices válidos de cities
    """
    return la.norm(cities[i, :] - cities[j, :])


class Individual:
    """
    Representación de un individuo en la población. Tiene como características su genoma y
    los métodos para calcular fitness, llevar a cabo mutaciones y el two-point crossover
    """

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


def greedy_popuation(n_population, ratio=1 / 2):
    """
    Genera población parte aleatoria parte generada mediante vecinos más cercanos.

    Args:
        n_population: Tamaño total de la población
        ratio: Qué porcentaje de la población se genera greedily. 0 -> toda random
    """
    # Guardamos la población generada en population
    population = []

    # Primero generamos los de vecinos más cercanos
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


def calculate_wheel_probability(population):
    """
    Calcula la probabilidad de reproducción para cada individuo en `population`. El de menor
    fitness es el que tiene más probabilidades de reproducirse
    """
    fitnesses = np.array([p.fitness for p in population])
    fitnesses = np.max(fitnesses) + 1 - fitnesses
    s = np.sum(fitnesses)
    return fitnesses / s


calculate_wheel_probability([i, o])


def GA(
    n_population=100, n_generation=1000, cross_rate=0.3, mutate_rate=0.2, greedy_rate=0,
):
    """
    Resuelve el problema del agente viajero mediante una versión modificada de la estrategia
    de algoritmos genéticos. Se genera una población del tamaño especificado y con las
    características de aleatoriedad deseadas.

    Args:
        n_population: Tamaño total de la población
        n_generation: Número de generaciones
        cross_rate:
        mutate_rate:
        greedy_rate: Porcentaje de la población inicial que se genera mediante vecinos
        verbose: Controla la cantidad de información que imprime el algoritmo
    """
    # Para la generación 0
    # Pk = random_population(n_population)
    history = []
    Pk = greedy_popuation(n_population, greedy_rate)
    best_individual = Pk[Pk.argmin()]
    for k in range(1, n_generation):
        # Creamos la siguiente generacion
        Pk_next = np.array([])
        # Para seleccionar usamos wheel roulette selection
        # Calculamos la wheel probability
        wheel_prob = calculate_wheel_probability(Pk)
        # 1. Copy: seleccionamos (1 − cross_rate) × n individuos de Pk y los insertamos en
        # Pk+1
        Pk_next = np.append(
            Pk_next,
            np.random.choice(
                Pk, round((1 - cross_rate) * n_population), p=wheel_prob, replace=True
            ),
        )
        # 2. Crossover: seleccionamos (cross_rate * n) parejas de Pk y los cruzamos para
        # añadirlos en Pk+1
        parejas = np.random.choice(
            Pk, 2 * round(cross_rate * n_population), p=wheel_prob, replace=True
        ).reshape(-1, 2)
        Pk_next = np.append(Pk_next, [p.cross(q) for p, q in parejas])

        # 3. Mutate: seleccionamos mutate_rate de la población Pk+1 y la mutamos
        mutate_index = np.random.choice(
            len(Pk_next), int(mutate_rate * len(Pk_next)), replace=True
        )
        Pk_next[mutate_index] = np.array([x.mutate() for x in Pk_next[mutate_index]])

        # Acualizamos la generación
        Pk = Pk_next
        if Pk[Pk.argmin()] < best_individual:
            best_individual = Pk[Pk.argmin()]

        history.append(best_individual)

    return best_individual, history


# + tags=[]
best_ga, hist_ga = GA(n_population=15, n_generation=10000)
best_nn, hist_nn = GA(n_population=15, n_generation=10000, greedy_rate=9 / 10)
# -

best_ga_sm, hist_ga_sm = GA(n_population=15, n_generation=10)
best_nn_sm, hist_nn_sm = GA(n_population=15, n_generation=10, greedy_rate=9 / 10)

# +
fig, axs = plt.subplots(2, 2, figsize=(8, 7))

# Tour GA
axs[0, 0].plot(cities[best_ga.genome][:, 0], cities[best_ga.genome][:, 1], "*")
axs[0, 0].plot(cities[best_ga.genome][:, 0], cities[best_ga.genome][:, 1], "--")
axs[0, 0].set_title("Tour (Alg. Genetico) 10k gens.")

# Tour NN
axs[0, 1].plot(cities[best_nn.genome][:, 0], cities[best_nn.genome][:, 1], "*")
axs[0, 1].plot(cities[best_nn.genome][:, 0], cities[best_nn.genome][:, 1], "--")
axs[0, 1].set_title("Tour (Hibrido) 10k gens.")

# Tour NN chico
axs[1, 0].plot(cities[best_ga_sm.genome][:, 0], cities[best_ga_sm.genome][:, 1], "*")
axs[1, 0].plot(cities[best_ga_sm.genome][:, 0], cities[best_ga_sm.genome][:, 1], "--")
axs[1, 0].set_title("Tour (Alg. Genetico) 10 gens.")

# Tour NN chico
axs[1, 1].plot(cities[best_nn_sm.genome][:, 0], cities[best_nn_sm.genome][:, 1], "*")
axs[1, 1].plot(cities[best_nn_sm.genome][:, 0], cities[best_nn_sm.genome][:, 1], "--")
axs[1, 1].set_title("Tour (Hibrido) 10 gens.")

fig.tight_layout()

plt.savefig("tours.pdf")

# +
fig, axs = plt.subplots(1, 2, figsize=(8, 4))

# Mejora GA
axs[0].plot(range(len(hist_ga)), [ind.fitness for ind in hist_ga])
axs[0].set_title("Mejora por generación (Alg. Genético)")

# Mejora NN
axs[1].plot(range(len(hist_nn)), [ind.fitness for ind in hist_nn])
axs[1].set_title("Mejora por generación (Hibrido)")


fig.tight_layout()

plt.savefig("mejora.pdf")
# -


# +
plt.plot(range(len(hist_ga)), [ind.fitness for ind in hist_ga], label="Alg. Genetico")
plt.plot(range(len(hist_nn)), [ind.fitness for ind in hist_nn], label="Hibrido")
plt.title("Distancia de ruta A. G vs. Hibrido")
plt.legend()

plt.savefig("comparacion.pdf")
# -
