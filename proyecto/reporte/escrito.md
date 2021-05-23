---
title: |
	![](figs/membrete-ITAM.pdf)
	Reporte IDO
author:
- Juanito
- Alonso
- Rebe
bibliography: refs.bib
geometry:
- margin=2cm
biblio-style: alphabetic
biblatexoptions: [backend=biber, citestyle=alphabetic]
header-includes:
  - \usepackage{pgfplots}
  - \usepackage{float}
  - \definecolor{backcolour}{rgb}{0.95,0.95,0.92}
  - \usepackage[ruled,vlined,linesnumbered]{algorithm2e}
  - \usepackage[utf8]{inputenc}
  - \SetKwRepeat{Do}{do}{while}
  - \usepackage{mathtools}
  - \lstset{language=Python,
	basicstyle=\ttfamily\small,
	numberstyle={\tiny \color{black}},
	backgroundcolor=\color{backcolour},
	breaklines=true,
	numbers=left,
	keywordstyle=\color{blue},
	inputencoding=utf8,
	commentstyle=\color{gray}}
...

# Marco teórico

## Formulación como problema de programación lineal

## Algoritmos genéticos

Quiero citar a [@jaketae] asi con este comando pero no se deja.

\begin{algorithm}[H]
\KwResult{ individuo más apto de $P_k$ }
\textbf{Inicializamos generación $0$}\;
$k \coloneqq 0$\\
$P_k \coloneqq $ población de $n$ individuos generados al azar; \\
\textbf{Evaluar} $P_k:$\\
\Do{el \underline{fitness} del individuo más apto en $P_k$ no sea lo suficientemente bueno}{
	 \textbf{Crear generación $k+1$}\;
	 \textbf{1. Copia:}\;
	 Seleccionar $ (1-\chi) \times  n$ miembros de $P_k$ e insertar en
	 $P_{k+1}$\\
	 \textbf{2. Cruce $k+1$}\;
	 Seleccionar $ \chi \times  n$ miembros de $P_k$; emparejarlos;
	 producir descendencia; insertar la descendencia en $P_{k+1}$\\
	 \textbf{3. Mutar:}\;
	 Seleccionar $ \mu \times  n$ miembros de $P_{k+1}$; invertir bits
	 seleccionados al azar \\
	 \textbf{Evaluar $P_{k+1}$}\;
	 Calcular $ fitness(i) $ para cada $ i \in P_k$\\
	 \textbf{Incrementar: $k :=k+1$}\;
}
\caption{GA($ n,\chi,\mu$) }
\end{algorithm}

## Vecinos más cercanos

\begin{algorithm}[H]
\KwResult{Ruta elegida con vecinos más cercanos a partir de ciudad inicial}
\textbf{Comenzamos con un conjunto de ciudades por visitar y un conjunto de visitados} \\
$c_0 \leftarrow$ ciudad elegida al azar. \\
$c_a \leftarrow c_0$ fijamos la ciudad actual. \\
$V \leftarrow \varnothing$ ciudades visitadas \\
$C \leftarrow \{ c_1, \ldots, c_n \}$ ciudades por visitar \\
\While{$|V| \neq |C|$}
{
	$V \leftarrow V \cup \{c_a \}$ \\
	$c^{*} \leftarrow \min\{d(c_a, c_i) \, | \, c_i \in C \setminus V \}$ \\
	$c_a \leftarrow c^{*}$ \\
}
\caption{Algoritmo vecinos más cercanos}
\end{algorithm}

# Resultados

![Tours](figs/tours.pdf){width="\\textwidth"}


![Disminucion de distancia de tour](figs/mejora.pdf){width="\\textwidth"}

# Conclusión

# Referencias
