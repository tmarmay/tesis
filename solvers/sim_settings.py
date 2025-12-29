import numpy as np

# Coordenadas del depósito y clientes
V = 2 # Vehicles = Depots
CUSTOMERS = 2
N = CUSTOMERS + 2*V # por el momento con el mismo depot y return


C = [i for i in range(CUSTOMERS)] #CUSTOMERS
DEPOTS = [i for i in range(C[-1] + 1, C[-1] + 1 + V)]
RETURNS_milp = [i for i in range(C[-1] + V + 1, N)]

RETURNS = { #no me gusta porq difiere de milp, verificar mas adalente
    DEPOTS[v]: C[-1] + 1 + V + v
    for v in range(V)
}

Q = [2 for _ in range(V)] # capacidad máxima del vehículo.
demands = [1 for _ in range(CUSTOMERS)] #Demenda de cada customer i

#la matriz tiene que ser espejo con la diagonal porque no es dirigido
# para decir que no puedo ir de i a j: Poner 0 en eta[i][j] y/o tau[i][j] va a hacer que la prob sea 0
cost_matrix = np.array([
# 0   1   2   3   4   5   6
[99, 12,  5,  7,  9,  8, 13],  # 0 depot v0
[12, 99,  7,  1,  6, 13,  8],  # 1 depot v1

[ 5,  7, 99,  4,  6,  5,  7],  # 2 cliente 0
[ 7,  1,  4, 99,  5,  7,  5],  # 3 cliente 1
[ 9,  6,  6,  5, 99,  6,  4],  # 4 cliente 2

[ 8, 13,  5,  7,  6, 99, 11],  # 5 return v0
[13,  8,  7,  5,  4, 11, 99],  # 6 return v1
])

F = [5 for _ in range(V)] # penalizacion por usar auto

tij = np.array([
# 0   1   2   3   4   5   6
[99, 10,  4,  6,  8,  7, 12],  # 0 depot v0
[10, 99,  6,  1,  5, 12,  7],  # 1 depot v1

[ 4,  6, 99,  3,  5,  4,  6],  # 2 cliente 0
[ 6,  1,  3, 99,  4,  6,  4],  # 3 cliente 1
[ 8,  5,  5,  4, 99,  5,  3],  # 4 cliente 2

[ 7, 12,  4,  6,  5, 99, 10],  # 5 return v0
[12,  7,  6,  4,  3, 10, 99],  # 6 return v1
])

ei = np.array([
    0,   # depot 0
    0,   # depot 1

    5,   # cliente 0
    0,   # cliente 1
   10,   # cliente 2

    0,   # return v0
    0    # return v1
])

li = np.array([
  999,  # depot 0
  999,  # depot 1

   20,  # cliente 0
   15,  # cliente 1
   30,  # cliente 2

  999,  # return v0
  999   # return v1
])
