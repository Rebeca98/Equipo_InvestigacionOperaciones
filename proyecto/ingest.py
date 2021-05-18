import csv
import glob
import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set()

matplotlib.use("module://matplotlib-backend-kitty")

exportando = False


# Asumiento el que los .txt están de hermanos
os.chdir(os.getcwd())

for filename in glob.glob("*.txt"):

    coordenadas = pd.read_csv(
        filename, sep=" ", names=["idx", "x", "y"], usecols=[1, 2]
    )

    city_name = str.split(filename, ".")[0]
    if exportando:

        sns.scatterplot(x="x", y="y", data=coordenadas)
        coordenadas.to_csv(f"csv/{city_name}.csv")

    sns.scatterplot(x="x", y="y", data=coordenadas)

    plt.title(f"{city_name}")
    plt.show()
