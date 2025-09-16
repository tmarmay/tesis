import numpy as np

def idx(k, N, i, j):
    return k * N * N + i * N + j

def constraint_32_eq(DIM, C, N, V):
    """
    Cada orden sea atendida una vez
    """
    A_eq = []
    b_eq = []
    
    for i in C:
        row = np.zeros(DIM)
        
        for k in range(V):
            for j in range(N):
                row[idx(k, N, i, j)] += 1
        
        A_eq.append(row)
        b_eq.append(1)
    
    return np.array(A_eq), np.array(b_eq)

def constraint_33_eq(C, N, V):
    """
    Que el vehiculo no supere la capacidad
    """
    pass

def constraint_34_eq(DIM, N, V):
    """
    Todos los vehiculos tienen que salir del depot

    Estoy obligando a usar todos los vehiculos, capaz conviene ponerla en ub
    """
    A_eq = []
    b_eq = []
    
    
    for k in range(V):
        row = np.zeros(DIM)
        for j in range(N):
            row[idx(k=k, N=N, i=0, j=j)] = 1
    
        A_eq.append(row)
        b_eq.append(1)
    
    return np.array(A_eq), np.array(b_eq)


def constraint_35_eq(DIM, C, N, V):
    """
    Conservación de flujo: para cada nodo i y vehículo k,
    lo que entra = lo que sale.
    """
    A_eq = []
    b_eq = []
    
    for h in C:
        for k in range(V):
            row = np.zeros(DIM)
            for i in range(N):
                row[idx(k=k, N=N, i=i, j=h)] += 1
            for j in range(N):
                row[idx(k=k, N=N, i=h, j=j)] += -1
        
            A_eq.append(row)
            b_eq.append(0)
    
    return np.array(A_eq), np.array(b_eq)

def constraint_36_eq(DIM, N, V, DEPOT):
    """
    El vehiculo termina en el depot
    """
    A_eq = []
    b_eq = []
    
    for k in range(V):
        row = np.zeros(DIM)
        for i in range(N):
            row[idx(k=k, N=N, i=i, j=DEPOT)] = 1

        A_eq.append(row)
        b_eq.append(1)
    
    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)
    
    return np.array(A_eq), np.array(b_eq)

def build_capacity_constraints(q, Q, N, V):
    """
    Restricciones de capacidad: suma de demandas <= capacidad.
    q: lista de demandas por cliente (long N)
    Q: capacidad del vehículo
    """
    A_ub = []
    b_ub = []
    
    for k in range(V):
        for i in range(N):
            row = np.zeros(V * N * N)
            for j in range(N):
                idx = k*N*N + i*N + j
                row[idx] = q[i]  # peso asociado al cliente i
        A_ub.append(row)
        b_ub.append(Q)
    
    return np.array(A_ub), np.array(b_ub)
