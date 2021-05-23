---
title: |
	![](figs/membrete-ITAM.pdf)
	Investigación de Operaciones |
	Proyecto final -- Reporte
author:
- Juan Carlos Sigler
- Alonso Martinez
- Rebeca Angulo
- Carlos Galeana
- Jacqueline Lira
bibliography: refs.bib
lang: es
geometry:
- margin=2cm
biblio-style: alphabetic
biblatexoptions: [backend=biber, citestyle=alphabetic]
header-includes:
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

Planteamos el problema de encontrar un _tour_, es decir una ruta
cerrada que pasa por todas las ciudades, sin repetir ninguna y
regresando a la ciudad de origen como un problema de minimización.
Para el acercamiento mediante algoritmos genéticos planteamos lo
siguiente para un individuo dado.

Sea $G = [g_1, g_2, \ldots, g_n]$ el _genoma_ del individuo. El genoma
se puede representar como una lista ordenada de números $g_i$ con $g_1
\leq g_i \geq g_n$ que representan el índice dado de una ciudad. Cada
ciudad tiene un índice único y lo usamos como su nombre. El conjunto
$C$ es el conjunto de los índices de todas la ciudades.

Entonces, podemos formular el problema como el siguiente problema de
programación lineal en forma estándar:

\begin{equation}
    \min = \sum_{i=1}^{n-1} \| C_i - C_{i+1} \| + \| C_n - C_1 \|
\end{equation}

Sujeto a:

\begin{align*}
	\sum_{i \in G} 1 = |C| & \text{ Se deben visitar todas las ciudades}\\
	g_i \neq g_j \quad \forall i \neq j & \text{ No se repite ninguna
	ciudad en el tour}
\end{align*}

## Algoritmos genéticos

Los algoritmos genéticos son algoritmos de optimización, búsqueda y
aprendizaje inspirados en los procesos de evolución natural y
evolución genética. La evolución es un proceso que opera sobre los
cromosomas. La selección natural, expuesta en la teoría de la
evolución biológica por Charles Darwin (1859), es un mecanismo que
relaciona los cromosomas (genotipo) con el fenotipo (caracteres
observables) y otorga a los individuos más adaptados un mayor número
de oportunidades de reproducirse, lo cual aumenta la probabilidad de
que sus características genéticas se repliquen.

Los procesos evolutivos tienen lugar durante la etapa de reproducción,
algunos de los mecanismos que afectan a la reproducción son la
mutación, causante de que los cromosomas en la descendencia sean
diferentes a los de los padres y el cruce que combina los cromosomas
de los padres para producir una nueva descendencia.

En un algoritmo genético para alcanzar la solución a un problema se
parte de un conjunto inicial de individuos, llamado población, el cual
es generado de manera aleatoria. Cada uno de estos individuos
representa una posible solución al problema. Se construye una función
objetivo mejor conocida como función *fitness*, ya definida en la
ecuación (1), y se definen los *adaptive landscapes*, los cuales son
evaluaciones de la función objetivo para todas las soluciones
candidatas. Por medio de una función de evaluación, se establece una
medida numérica, la cual permite controlar en número de selecciones,
cruces y copias. En general, esta medida puede entenderse como la
probabilidad de que un individuo sobreviva hasta la edad de
reproducción.

### Representación

Para trabajar con las características genotípicas de una población
dotamos a cada individuo de un _genotipo_. En nuestra implementación
éste se representa como una lista de índices de ciudades. En general,
el genotipo es se puede representar como una cadena de bits que se
manipul y muta.

![](figs/gen.png){width="0.2*\textwidth"}

## Operadores genéticos

Una generación se obtiene a partir de la anterior por medio de
operadores, mejor conocidos como operadores genéticos. Los más
empleados son los operadores de selección, cruce, copia y mutación,
los cuales vamos a utilizar en la implementación del algoritmo.

### Selección:

Es el mecanismo por el cual son seleccionados los individuos que serán
los padres de la siguiente generación. Se otorga un mayor número de
oportunidades de reproducción a los individuos más aptos.
Existen diversas formas de realizar una selección, por ejemplo:
1. Selección por truncamiento
2. Selección por torneos
3. Selección por ruleta
4. Selección por jerarquías

Los algoritmos de selección pueden ser divididos en dos grupos:
probabilísticos, en este grupo se encuentran los algoritmos de
selección por ruleta, y determinísticos, como la selección por
jerarquías.

En nuestro algoritmo utilizamos la selección por ruleta, donde cada
padre se elige con una probabilidad proporcional a su desempeño en
relación con la población.

### Cruce:

Consiste en un intercambio de material genético entre dos cromosomas
de dos padres y a partir de esto se genera una descendencia. Existen
diversas formas de hacer un cruce, en nuestro algoritmo utilizamos el
cruce de dos puntos.

![](figs/cross.png){width="0.5\textwidth"}

La idea principal del cruce se basa en que si se toman dos individuos
correctamente adaptados y se obtiene una descendencia que comparta
genes de ambos, al compartir las características buenas de dos
individuos, la descendencia, o al menos parte de ella, debería tener
una mayor bondad que cada uno de los padres.

### Mutación:

Una mutación en un algoritmo genético causa pequeñas alteraciones en
puntos determinados de la codificación del individuo, en otras
palabras, produce variaciones de modo aleatorio en un cromosoma.
Por lo general primero se seleccionan dos individuos de la población
para realizar el cruce y si el cruce tiene éxito entonces el
descendiente muta con cierta probabilidad.

### Copia:

Consiste simplemente en la copia de un individuo en la nueva
generación. Un determinado número de individuos pasa directamente a la
siguiente generación sin sufrir variaciones.

## Implementación

A continuación presentamos el pseudocódigo del algoritmo que
implementaremos. Nos basamos principalmente en [@optimization] y en
[@TSP].

\begin{algorithm}[H]
\KwResult{ individuo más apto de $P_k$ }
\textbf{Inicializamos generación $0$}\;
$k \coloneqq 0$\\
$P_k \coloneqq $ población de $n$ individuos generados al azar; \\
\textbf{Evaluar} $P_k:$\\
\Do{el \underline{fitness} del individuo más apto en $P_k$ no sea lo
suficientemente bueno}{
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

$n$ es el número de individuos en la población.
$\chi$ es la fracción de la población que será reemplazada por el
cruce en cada iteración.
$(1-\chi)$ es la fracción de la población que será copiada.
$\mu$ es la tasa de mutación.

En cuanto a los criterios de terminación de nuestro algoritmo,
nosotros indicamos que debe detenerse cuando alcance el número de
generaciones máximo especificado.

El código de _python_ utilizado para los resultados se adjunta al
final de este documento como un anexo en interés de la brevedad y
legibilidad de este reporte.

## Vecinos más cercanos

El algoritmo de Vecinos más cercanos es otra heurística pensada para
resolver el problema del agente viajero mediante una estrategia
_greedy_. A diferencia de un algoritmo genético, vecinos más cercanos
planea una ruta mediante un criterio simple: si se minimiza la
distancia recorrida al recorrer una ciudad más, es sensato pensar que
se minimiza la distancia total del tour. Entonces, se selecciona una
ciudad al azar para empezar el tour, y se calculan las ciudades más
cercanas sucesivamente hasta que no quede ninguna.

Esta idea queda retratada en el siguiente algoritmo presentado como
pseudocódigo:

\begin{algorithm}[H]
\KwResult{Ruta elegida con vecinos más cercanos a partir de ciudad
inicial}
\textbf{Comenzamos con un conjunto de ciudades por visitar y un
conjunto de visitados} \\
$c_0 \leftarrow$ ciudad elegida al azar. \\
$c_a \leftarrow c_0$ fijamos la ciudad actual. \\
$V \leftarrow \varnothing$ ciudades visitadas \\
$C \leftarrow \{ c_1, \ldots, c_n \}$ ciudades por visitar \\
\While{$|V| \neq |C|$}
{
	$V \leftarrow V \cup \{c_a \}$ \\
	$c^{*} \leftarrow \min\{d(c_a, c_i) \, | \, c_i \in C \setminus V
	\}$ \\
	$c_a \leftarrow c^{*}$ \\
}
\caption{Algoritmo vecinos más cercanos}
\end{algorithm}

Cabe mencionar que para este trabajo, implementamos un algoritmo
genético y otro híbrido con el propósito de comparar su desempeño en
los datos del país de Qatar.

El algoritmo híbrido que desarrollamos consta en una mezcla de las
estrategias de vecinos más cercanos con algoritmos genéticos. Nuestro
algoritmo difiere de uno genético en que la población inicial no se
genera solo aleatoriamente. Damos la posibilidad de elegir qué
porcentaje de esa población son individuos generados con la estrategia
de vecinos más cercanos. Después de la generación de esta población
inicial se deja que el algoritmo continue con el proceso de mutación y
cruza como lo haría sin modificaciones; solo interferimos en la
creación de la población inicial.

La idea detrás de este algoritmo híbrido es fomentar una convergencia
más rápida a un óptimo auténtico introduciendo un "super gen" que
generación a generación se irá haciendo más común en la población por
la ventaja que da. Además, esperamos que la estrategia de mutación
permitiera mejorar paulatinamente una solución que ya era en si muy
buena, y llegar a un óptimo global real y no solo uno local. En la
siguiente sección hablamos con más detalle de lo que sucedió
realmente.

# Resultados

Para dar contexto, presentamos primero un mapa de el país
seleccionada: Qatar.

![Qatar](figs/qatar.pdf){width="0.75\\textwidth"}

Seleccionamos este país porque su baja densidad permite ver sin
mucho esfuerzo qué rutas son más óptimas que otras. Por ejemplo,
cruces de un lado a otro del mapa indican rutas sub-óptimas.

## Pruebas

Para los resultados que se presentan a continuación se corrieron
10,000 generaciones del algoritmo genético tanto en su versión
estándar como la versión híbrida. Para asegurar la reproducibilidad de
estos resultados se fijó el _seed_ de el generador de números
aleatorios. De esta manera aseguramos que las versiones del algoritmo
híbrido que comparamos más tarde comenzaron en la misma ciudad.

En la figura siguiente, presentamos cómo evoluciona la distancia total
del tour a medida que avanzan las generaciones.


![Disminucion de distancia de
tour](figs/mejora.pdf){width="0.85\\textwidth"}

Algunas cosas resultan aparentes de la figura. Por ejemplo: se puede
notar que el algoritmo genético es efectivo y si logra reducir la
distancia total recorrida generación a generación. Es decir el
algoritmo está bien implementado. Dicho eso, también se puede ver con
claridad que hay varias puntos en la gráfica en los cuales la
disminución de distancia total entre generaciones sucesivas es cero.
El algoritmo se estanca.

Otra detalle a notar es que la distancia total recorrida en el caso
del algoritmo híbrido es casi constante. Se empieza con una distancia
muy buena, y la mutación y cruza puede hacer muy poco para mejorarla.
Incluso después de 10 mil generaciones.

La siguiente figura es una comparación directa de la distancia del
tour que proponen el algoritmo genético y el híbrido. Es clara la
diferencia abismal.

![Comparacion directa de las
distancias](figs/comparacion.pdf){width="0.65\\textwidth"}

Finalmente, para hacer claro cómo se comparan en desempeño ambos
algoritmos presentamos la siguiente gráfica que está dividida en 4
subgráficas. Como sugieren los títulos, en la primera fila se
encuentra la comparacion de los tours propuestos por el algoritmo
genético (izquierda) contra el algoritmo híbrido (derecha) ambos al
final de 10,000 generaciones. En la fila de abajo, el análogo pero
para apenas 10 generaciones.

![Tours](figs/tours.pdf){width="\\textwidth"}

El ver los tours graficados directamente sobre el mapa de el país
permite ver con claridad qué ruta es mejor, ya que es fácil ver que
una ruta de apariencia menos caótica es más eficiente en la distancia
total.

Esta figura resulta ilustrativa de dos fenómenos importantes: Primero
que nada, se nota que el algoritmo genético si está encontrando rutas
cada vez mejores, pero lo hace a costa de mucho cómputo pesado y
tiempo. Después, se puede ver que el algoritmo híbrido tiene rutas por
mucho superiores a su contraparte, y además es claro que estas no
mejoran de manera obvia bajo mutación incluso a través de varios miles
de generaciones. Lo cual sugiere que eran rutas muy aceptables desde
el inicio.

# Conclusión

De los resultados anteriores podemos ver el comportamiento de ambos
algoritmos con mucha claridad. En particular vale la pena hacer notar
lo siguiente:

1. El algoritmo genético es muy caro computacionalmente hablando y en
   general propone rutas poco óptimas

2. El algoritmo híbrido llega muy rápido a un óptimo local y no cambia
   mucho después de eso. Lo cual podría sugerir que la solución
   propuesta es de inicio muy buena o que el componente genético no es
   lo suficientemente bueno como para privilegiar las ventajas tan
   pequeñas que podría dar la mutación.

En resumen, se podría decir que bajo estas condiciones particulares y
la implementación específica de ambos algoritmos, resulta mucho más
conveniente resolver el problema del agente viajero mediante una
estrategia greedy como vecinos más cercanos y el algoritmo híbrido que
hacerlo mediante un algoritmo genético. En este caso particular,
parece ser que el algoritmo híbrido es poco efectivo, porque llega a
un óptimo desde la primera iteración y por el resto de las
generaciones y mutaciones no mejora. Entonces no hace falta el
componente genético y se puede lograr una solución satisfactoria con
una sola aplicación del algoritmo de vecinos más cercanos.

# Referencias

# Código en python

\lstinputlisting[caption=Implementación de algoritmos descritos,
firstline=17]{../Travelling Salesman.py}
