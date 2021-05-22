---
title: Prueba
author:
- Juanito
- Alonso
- Rebe
bibliography: refs.bib
...

---
header-includes:
  - \usepackage{nicefrac}
  - \usepackage{algorithm2e}
---

# Implementación

El algoritmo Simplex modificado que decidimos implementar es el conocido
como el método de la gran M. Con esta implementación podemos resolver
cualquier Problema de Programación Lineal (PPL) bien definido, con el
origen incluido o exluido del polítopo factible. Elegimos el método de
la gran M en vez de las dos fases por su facilidad de implementación, y
dado que al ser una implementación computacional, manipular una M
considerablemente grande no afecta la velocidad de ejecución puesto que
en el estándar IEEE de tipo de datos *float*, la multiplicación entre
números toma el mismo tiempo sin importar el tamaño del número, lo cual
nos permitió elegir M suficientemente grande para asegurar que el método
fuese exitoso.

Para implementar el algoritmo Simplex dividimos el algoritmo en pequeñas
subrutinas, cada una independiente de las demás, siguiendo la filosofía
de diseño Unix. Para referirnos a cada una de estas subrutinas,
escribimos su nombre en `este formato` para acentuar su papel como
programas.

Cabe mencionar que por brevedad, reducimos la cantidad de detalles
presentados en el pseudocódigo que mostramos a continuación. Para más
detalles, se puede consultar el código que se entrega con el proyecto.

## Pivoteo

Para el proceso básico de identificar pivotes según la regla de Bland, y
después hacer un uno principal en el pivote identificado sobre la tabla,
usamos dos subrutinas: una que encuentra el pivote y otra que hace la
operación de pivoteo.

\begin{algorithm}[H]
\DontPrintSemicolon
\SetAlgoLined
\KwResult{Write here the result}
\SetKwInOut{Input}{Input}\SetKwInOut{Output}{Output}
\Input{Write here the input}
\Output{Write here the output}
\BlankLine
\While{While condition}{
    instructions\;
    \eIf{condition}{
        instructions1\;
        instructions2\;
    }{
        instructions3\;
    }
}
\caption{While loop with If/Else condition}
\end{algorithm}

El algoritmo de pivoteo está inspirado en la idea de una factorización
LU "incompleta". Calcular la factorización LU equivale a encontrar una
matriz L que encodifica todo el proceso de pivoteo del Gauss-Jordan.
Usamos una estrategia similar pero para un solo pivote.

Como se puede ver, no hay ningúna estructura de repetición en
`pivotea`.
Aprovechamos las propiedades de las matrices elementales y las
optimizaciones del lenguaje [Matlab]{.smallcaps} para hacer el algoritmo
lo más rápido y eficiente posible al crear unos principales en un solo
paso en vez de buscar entrada por entrada candidatos y hacer divisiones
renglón por renglón[^1].

## Algoritmo Simplex

Con la subrutina `Simplexealo` implementamos el proceso de repetición
del pivoteo hasta que se encuentra la tabla final, y además checamos las
condiciones de terminación que nos permiten saber si el algoritmo
Simplex terminó con soluciones óptimas, degeneradas, o si el polítopo
factible del problema no está acotado.

# *Benchmarking*

Con el propósito de medir cuantitativamente el desemepeño de nuestra
implementación del algoritmo Simplex con la regla de Bland, decidimos
implementar una serie de pruebas diseñadas para medir el desempeño en el
peor caso, y desempeño promedio, como es descrito en [@vanderbei].

## Análisis de peores casos

Para medir el desempeño en el peor de los casos posibles, nos servimos
de un problema conocido en la comunidad de optimización por sus
propiedades: el problema de Klee-Minty, que es bien sabido toma una
cantidad exponencial de pasos para resolver a medida que crece la
dimensión. Como menciona [@murty], el poliedro descrito por el problema
de Klee-Minty de $d$ dimensiones, es un poliedro con $2^d$ vértices, y
en [@vanderbei] se muestra que Simplex implementado con la regla de
mayor descenso (distinta de Bland) toma $2^d-1$ iteraciones en terminar.
Es decir, visita casi todos los vértices del poliedro. Ahora, con la
Regla de Bland se prueba en [@chvatal] que el número de iteraciones está
acotado por el $d$-ésimo número de Fibonacci[^2], que a su vez sigue
creciendo más que polinomialmente.

Para probar estos resultados teóricos y verificar la validez de nuestra
implementación llevamos a cabo experimentos en los que resolvíamos el
problema de programación lineal de Klee-Minty con punto inicial en el
origen para $d$ de 2 a 30[^3]. En la figura
[\[fig:k-m-steps\]](#fig:k-m-steps){reference-type="ref"
reference="fig:k-m-steps"} se puede ver una gráfica de dimensión del
problema vs. el número de pasos que requiere nuestra implementación para
llegar al punto óptimo del problema $(0, \dots, x_d)$ [@murty]. Nótese
por favor que el eje del número de pasos está en escala logarítmica.

Como se puede ver en la figura, para el problema K-M de dimensión 30
iniciando en el origen, se necesitan más de 2 millones de pasos! Para el
PPL Klee-Minty de 30 dimensiones el tiempo que tardó para ser resuelto
fue de 243.8 segundos[^4]: poco más de 4 minutos en un solo problema!
Resulta de cierta forma escandaloso si pensamos que 30 variables de
decisión y restricciones no es excesivamente grande para un problema de
la vida real.

## Análisis de caso promedio

Para probar el desempeño en el caso promedio, simulamos problemas de
dimensión $d$ generando matrices de constantes, vectores de costos y
restricciones aleatorias emulando el método utilizado en [@chvatal]. En
la figura [\[fig:al-steps\]](#fig:al-steps){reference-type="ref"
reference="fig:al-steps"} mostramos los resultados del mismo
experimento: dimensión del problema vs. número de pasos para resolverlo,
pero ahora con un problema de programación lineal generado
aleatoriamente y el eje $y$ en escala lineal. Cabe aclarar que en estos
experimentos el PPL también se inicia en el origen.

Como muestra la figura
[\[fig:al-steps\]](#fig:al-steps){reference-type="ref" reference="fig:al-steps"}, el comportamiento del algoritmo para
problemas generados aleatoriamente es radicalmente distinto: la linea ni
siquiera es estrictamente creciente. La figura sugiere que la cantidad
de pasos si va aumentando poco a poco, pero el tamaño de esta muestra es
muy pequeña para asegurarlo.

## Análisis de caso promedio

Para tener una mejor idea del comportamiento en el caso promedio
simulamos problemas de dimensión de hasta 500. En la figura
[1](#fig:caso_aleatorio){reference-type="ref" reference="fig:caso_aleatorio"} (página ) mostramos una gráfica de
dimensión del PPL vs. la cantidad de pasos que se necesitan para
resolverlo en la gráfica superior, y el tiempo para resolver todo el
problema en la gráfica inferior. Cada gráfica tiene su respectiva recta
de regresión lineal.

![Analisis de tiempo de compleción y pasos requeridos en caso
aleatorio](resources/img/analisis-500-rand.pdf){#fig:caso_aleatorio
width="\\textwidth"}

La figura muestra que al aumentar las dimensiones, la cantidad de pasos
requeridos para resolver el PPL no crece tan rápidamente. La recta de
regresión lineal (apenas visible) sugiere que casi se quedan constantes.
Sin embargo, la gráfica inferior que reporta el tiempo para resolver el
PPL si muestra una claro incremento a en el tiempo a medida que aumentan
las dimensiones. La recta de mínimos cuadrados sugiere una relación
no-lineal. Dado que aumenta el tiempo para resolver, pero no
necesariamente la cantidad de pasos, concluimos que el tiempo necesitado
para cambiar variables y pasar de una s.b.f a otra requiere más tiempo.

Podemos notar que el máximo tiempo de resolución para un PPL de
dimensión hasta 500 es apenas menor que 0.5 segundos. Lo cual sugiere
que en la práctica, incluso un problema con 500 variables de decisión y
restricciones está al alcance de cómputo modesto.
