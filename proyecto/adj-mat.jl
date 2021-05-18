# Pequeño script de Julia para crear la matriz de adyacencias a partir de un csv de localizaciones
# en un país.
# Actualmente asume un csv formateado bonito que primero fue procesado por python, pero se podría
# evitar.
using CSV # Para leer el .csv
using LinearAlgebra # Para norm, entre otros
using NPZ # Para escribir la matriz en formato .npy para que la lea numpy

# Cantidad de lineas
n = (open("csv/Oman.csv") |> readlines |> length) -1

# Guardamos los puntos
puntos = Vector{Vector{Float64}}(undef, n)

# Contador para las columnas
k = 1

# Iterando sobre columna
for row in CSV.Rows("csv/Oman.csv")
	# Obtenemos los datos y los parseamos como Float64
	x = parse(Float64, row.x)
	y = parse(Float64, row.y)

	# Suena poco idiomático pero para esto me da por ahora
	puntos[k] = [x, y]

	# Julia pide global porque k se definió fuera de este scope
	global k = k+1
end


# Ahora si matriz de adyacencias
ady = zeros(n,n)

# Llenamos la matriz de adyacencias por columna porque Julia usa column-major storage
for i = 1:n
	for j = i:n
		# Calculando la distancia entre puntos como la norma de su resta
		ady[i, j] = norm(puntos[i] - puntos[j])
	end
end

# Guardando en formato de matriz matplotlib
npzwrite("mats/oman.npy", ady)
