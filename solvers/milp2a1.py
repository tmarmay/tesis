"""
milp2a1.py
Solver Milp for MD-VRP-TW.
2a1 version.
"""

# from solvers.utils_vrp import check_tw_feasibility
# from solvers.aux.milp_constraints import *
import numpy as np
import pyomo.environ as pyo

N = 3 # Nodos incluye depot y customers
V = 2 # Vehiculos 
cost_matrix = np.array([[0,1000,1200],
                        [1000,0,8],
                        [1200,8,0]])

F = [5 for _ in range(V)] # penalizacion por usar auto
Q = [1,2] #[1 for _ in range(V)] # capacidad máxima del vehículo.
demands = [0] + [1 for _ in range(N-1)] #Demenda de cada customer i
C = [i for i in range(1,N)] # Customers sin los depots


DIM = (V * N * N) #+ (V * N) + (V)
DIM_XIJK = V * N * N
DIM_SIK = V * N
DIM_UK = V


tij = np.array([[0,10,10],
                [10,0,10],
                [10,10,0]])

ei = [0, 10, 20]
li = [100, 20, 30]

def objective_rule(model):
    #return sum(cost_matrix[i][j] * model.x[k, i, j] for k in range(V) for i in range(N) for j in range(N))

    # Costo de los viajes
    travel_cost = sum(cost_matrix[i][j] * model.x[k, i, j] for k in range(V) for i in range(N) for j in range(N))
    
    # Costo de los vehículos (F_k) basado en las variables u_k
    vehicle_cost = sum(F[k] * model.u[k] for k in range(V))  # F[k] es el costo del vehículo k
    
    #time_cost = sum(model.s[k, i] for k in range(V) for i in range(N))
    
    # La función objetivo es la suma de ambos costos
    return travel_cost + vehicle_cost #+ time_cost

#Cada nodo debe ser visitado exactamente una vez
def constraint_32_eq(model, i):
    if i != 0:  # El depósito (nodo 0) no se cuenta
        return sum(model.x[k, i, j] for k in range(V) for j in range(N) if i != j) == 1
    else:
        return pyo.Constraint.Skip  # El depósito no tiene restricción de visita

#Tiene que salir del depot
def constraint_34_eq(model, k):
    return sum(model.x[k, 0, j] for j in range(1, N)) == model.u[k]

#Tiene que volver al depot
def constraint_36_eq(model, k):
    return sum(model.x[k, j, 0] for j in range(1, N)) == model.u[k]

#Conservascion flujo
def constraint_35_eq(model, h, k):
    inpt = (model.x[k, i, h] for i in range(N) if i != h)
    outpt = (model.x[k, h, j] for j in range(N) if j != h)
    return sum(inpt) - sum(outpt) == 0

#Variables para los vehiculos
def constraint_min_vehicle(model):
    return sum(model.u[k] for k in range(V)) >= 1

#Restriccion de capacidad
def constraint_33_ub(model, k):
    return sum(model.x[k, i, j] * demands[i] for i in C for j in range(N) if i != j) <= Q[k]

#Restriccion de tiempo 
def constraint_37_ub(model, k, i, j):
    if i == j or j == 0:
        return pyo.Constraint.Skip
    Mij = li[i] + tij[i][j] - ei[j]  # Big-M calculado como parámetro
    return model.s[k,i] + tij[i][j] - Mij * (1 - model.x[k,i,j]) <= model.s[k,j]

def s_bounds(model, k, i):
    return (ei[i], li[i])  # ventana de tiempo para el nodo i

# ====== Main Function ======
def milp2a2_solver():
    # Crear el modelo de optimización
    model = pyo.ConcreteModel()

    # Definir las variables
    model.x = pyo.Var(range(V), range(N), range(N), domain=pyo.Binary)  # xijk binaria
    model.u = pyo.Var(range(V), domain=pyo.Binary)  # uk binaria
    model.s = pyo.Var(range(V), range(N), domain=pyo.Reals, bounds=s_bounds)  # sik

    # Inicializar x[i, j, k] = 0 para las combinaciones donde i == j
    for k in range(V):
        for i in range(N):
            for j in range(N):
                if i == j:
                    model.x[k, i, j].fix(0)  # Fijar x[i, j, k] a 0 cuando i == j

    # Función objetivo: Minimizar los costos de los viajes
    model.obj = pyo.Objective(rule=objective_rule, sense=pyo.minimize)
    
    model.visit_once = pyo.Constraint(range(1, N), rule=constraint_32_eq)
    model.from_depot = pyo.Constraint(range(V), rule=constraint_34_eq)
    model.back2_depot = pyo.Constraint(range(V), rule=constraint_36_eq)
    model.flow = pyo.Constraint(range(1, N), range(V), rule=constraint_35_eq)
    model.uk = pyo.Constraint(rule=constraint_min_vehicle)
    model.capacity = pyo.Constraint(range(V), rule=constraint_33_ub)
    model.time_windows = pyo.Constraint(range(V), range(N), range(N), rule=constraint_37_ub)
    
    
    # Resolver el modelo
    solver = pyo.SolverFactory('glpk')
    results = solver.solve(model, tee=False)
    
    # Verificar el estado de la solución
    print("Estado de la solución:", results.solver.status)
    print("Condición de terminación:", results.solver.termination_condition)

    # Verificar el estado de la solución
    # if results.solver.status == pyo.SolverStatus.ok:
    #     print("La solución fue encontrada con éxito.")
    # elif results.solver.status == pyo.SolverStatus.error:
    #     print("Hubo un error al resolver el problema.")
    # else:
    #     print("Estado del solver:", results.solver.status)

    if results.solver.termination_condition != "infeasible":
        # Imprimir las variables de decisión (xijk)
        print("\nVariables de decisión (xijk):")
        for k in range(V):
            for i in range(N):
                for j in range(N):
                    if model.x[k, i, j].value:  # Solo imprimir si xijk es 1 (viaje hecho)
                        print(f"x[{k},{i},{j}] = {model.x[k, i, j].value}")
        # Imprimir las variables u (carga de los vehículos)
        print("\nCarga de los vehículos (uk):")
        for k in range(V):
            print(f"u[{k}] = {model.u[k].value}")

        print("\nTiempos de servicio (sik):")
        for k in range(V):
            for i in range(N):
                print(f"s[{k},{i}] = {model.s[k,i].value}")

        #Imprimir el valor objetivo (costo total)
        print("\nValor objetivo (costo total):", model.obj())
    else:
        for k in range(V):
            for i in range(N):
                var = model.s[k,i]
                print(f"s[{k},{i}] : bounds={var.lb, var.ub}, value={pyo.value(var, exception=False)}")
        for idx in model.time_windows:
            print(f"time_windows[{idx}] : {model.time_windows[idx].expr}")

milp2a2_solver()