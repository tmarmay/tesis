"""
milp2a1.py
Solver Milp for MD-VRP-TW.
2a1 version.
"""

from solvers.utils_vrp import check_tw_feasibility
from solvers.aux.milp_constraints import *
import numpy as np

from scipy.optimize import linprog


N = 3 # Nodos incluye depot y customers
V = 2 # Vehiculos 
C = [1,2] # Customers sin los depots
demands = [1, 2]#despues hay que hacerlo vector por cada customer
Q = 1 # capacidad máxima del vehículo.

DIM = V * N * N

cost_matrix = np.array([[0,10,12],
                  [10,0,8],
                  [12,8,0]])


def build_cost_vector(cost_matrix, N, V):
    """
    Construye el vector de costos c para linprog.
    
    cost_matrix: matriz NxN con costos c[i][j]
    N: número de nodos
    V: número de vehículos

    En este caso no hace falta user idx porque la recorro en orden.
    """
    c = []
    bounds = []
    for k in range(V):
        for i in range(N):
            for j in range(N):
                if i == j:
                    c.append(0)
                    bounds.append((0,0)) # Lo anulo, equivalente a poner un costo muy alto
                else:
                    c.append(cost_matrix[i][j])
                    bounds.append((0,1))
    return np.array(c), bounds

            
def restrictions():
    # assignment
    A_eq2, b_eq2 = constraint_32_eq(DIM, C, N, V)
    A_ub3, b_ub3 = constraint_33_ub(DIM, C, N, V, demands, Q)
    A_eq4, b_eq4 = constraint_34_eq(DIM, N, V)
    A_eq5, b_eq5 = constraint_35_eq(DIM, C, N, V)
    A_eq6, b_eq6 = constraint_36_eq(DIM, N, V, DEPOT=0)

    # Apilamos todas las matrices A_eq verticalmente
    # Concatenamos todos los vectores b_eq horizontalmente
    A_eq = np.vstack([A_eq2, A_eq5, A_eq6, A_eq4])
    b_eq = np.hstack([b_eq2, b_eq5, b_eq6, b_eq4])

    A_ub = np.vstack([A_ub3])
    b_ub = np.hstack([b_ub3])
    return A_eq, b_eq, A_ub, b_ub


def get_vehicle_routes(solution, depot=0):
    for k in range(V):
        costo = 0
        route = f"k={k} : "
        for i in range(N):
            for j in range(N):
                if solution.x[idx(k, N, i, j )] == 1:
                    route += f"{i} → "
                    costo += cost_matrix[i][j]
        route += f"0 costo={costo}"
        print(route)
    print(f"costo total {solution.fun}")

# ====== Main Function ======
def milp2a2_solver(): # carriers: list, shipments: list, sol:list = None 
    #empiezo con V=N y hasta que me de una solucion(result.solve) y no empeore el costo hago V-1

    c, bounds = build_cost_vector(cost_matrix, N, V)
    c.flatten()
    
    A_eq, b_eq, A_ub, b_ub = restrictions()

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs', options={"disp": True})
    get_vehicle_routes(result)
