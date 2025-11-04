"""
milp2a1.py
Solver Milp for MD-VRP-TW.
2a1 version.
"""
import numpy as np
import pyomo.environ as pyo


V = 1 # Vehiculos == CARRIERS
CUSTOMERS = 2

N = CUSTOMERS + 2*V # Nodos incluye depot y customers

cost_matrix = np.array([[0,10,1200,1000,1200,1000],
                        [10,0,8,1000,1200,1000],
                        [1200,8,0,1000,1200,1000],
                        [1200,8,10,0,1200,1000],
                        [1200,8,10,1000,0,1000],
                        [1200,8,10,1000,1200,0]])

F = [5 for _ in range(V)] # penalizacion por usar auto

C = [i for i in range(CUSTOMERS)] # Customers sin los depots
DEPOTS = [i for i in range(C[-1] + 1, C[-1] + 1 + V)]
RETURNS = [i for i in range(C[-1] + V + 1, N)]


Q = [2 for _ in range(V)] # capacidad máxima del vehículo.
demands = [1 for _ in range(CUSTOMERS)] #Demenda de cada customer i

DIM = (V * N * N) #+ (V * N) + (V)
DIM_XIJK = V * N * N
DIM_SIK = V * N
DIM_UK = V

tij = np.array([[0,10,10,10,10,10],
                [10,0,10,10,10,10],
                [10,10,0,10,10,10],
                [10,10,10,0,10,10],
                [10,10,10,10,0,10],
                [10,10,10,10,10,0]])

ei = [0, 20, 0, 0, 0, 0]
li = [10, 30, 0,0,200,200]

def objective_rule(model):
    # Costo de los viajes
    travel_cost = sum(cost_matrix[i][j] * model.x[k, i, j] for k in range(V) for i in range(N) for j in range(N))
    
    # Costo de los vehículos (F_k) basado en las variables u_k
    vehicle_cost = sum(F[k] * model.u[k] for k in range(V))  # F[k] es el costo del vehículo k
    
    #time_cost = sum(model.s[k, i] for k in range(V) for i in range(N))
    
    # La función objetivo es la suma de ambos costos
    return travel_cost + vehicle_cost #+ time_cost

#Cada nodo debe ser visitado exactamente una vez
def constraint_32_eq(model, i):
    # i es el cliente
        return sum(model.x[k, i, j] for k in range(V) for j in range(N) if i != j) == 1

#Tiene que salir del depot
def constraint_34_eq(model, k):
    depot = DEPOTS[k]
    return sum(model.x[k, depot, j] for j in range(N) if j != depot) == model.u[k]

#Tiene que volver al depot
def constraint_36_eq(model, k):
    ret = RETURNS[k]
    return sum(model.x[k, i, ret] for i in range(N) if i != ret) == model.u[k]

#Conservascion flujo
def constraint_35_eq(model, h, k):
    depot = DEPOTS[k]
    ret = RETURNS[k]
    
    if h == depot or h == ret:
        return pyo.Constraint.Skip
    
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
    if i == j or j == RETURNS[k]:
        return pyo.Constraint.Skip
    Mij = li[i] + tij[i][j] - ei[j]  # Big-M
    return model.s[k,i] + tij[i][j] - Mij * (1 - model.x[k,i,j]) <= model.s[k,j]

def s_bounds(model, k, i):
    return (ei[i], li[i])  # ventana de tiempo para el nodo i

# Para cada vehiculo k: si usa algun arco (i,j) entonces u[k] = 1 (Big-M)
def aux1(model, k):
    return sum(model.x[k, i, j] for i in range(N) for j in range(N) if i != j) <= N * model.u[k]

# ====== Main Function ======
def milp2a2_solver():
    # Crear el modelo de optimización
    model = pyo.ConcreteModel()

    # Definir las variables
    model.x = pyo.Var(range(V), range(N), range(N), domain=pyo.Binary)  # xijk binaria
    model.u = pyo.Var(range(V), domain=pyo.Binary)  # uk binaria
    model.s = pyo.Var(range(V), range(N), domain=pyo.Reals, bounds=s_bounds)  # sik

    # Inicializar x[k, i, j] = 0 para las combinaciones donde i == j
    for k in range(V):
        for i in range(N):
            model.x[k, i, i].fix(0)  # Fijar x[k, i, j] a 0 cuando i == j

    # Función objetivo: Minimizar los costos de los viajes
    model.obj = pyo.Objective(rule=objective_rule, sense=pyo.minimize)
    
    model.visit_once = pyo.Constraint(C, rule=constraint_32_eq)
    model.from_depot = pyo.Constraint(range(V), rule=constraint_34_eq)
    model.back2_return = pyo.Constraint(range(V), rule=constraint_36_eq)
    model.flow = pyo.Constraint(range(N), range(V), rule=constraint_35_eq)
    model.uk = pyo.Constraint(rule=constraint_min_vehicle)
    model.capacity = pyo.Constraint(range(V), rule=constraint_33_ub)
    model.time_windows = pyo.Constraint(range(V), range(N), range(N), rule=constraint_37_ub)
    
    model.aux_link_x_u = pyo.Constraint(range(V), rule=aux1)
    
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
        print("\nVariables de decisión (xkij):")
        for k in range(V):
            for i in range(N):
                for j in range(N):
                    if model.x[k, i, j].value:  # Solo imprimir si xijk es 1 (viaje hecho)
                        print(f"x[{k},{i},{j}] = {model.x[k, i, j].value}")
        # Imprimir las variables u (carga de los vehículos)
        print("\nCarga de los vehículos (uk):")
        for k in range(V):
            print(f"u[{k}] = {model.u[k].value}")

        print("\nTiempos de servicio (ski):")
        for k in range(V):
            for i in range(N):
                if model.s[k,i].value:
                    print(f"s[{k},{i}] = {model.s[k,i].value}")

        #Imprimir el valor objetivo (costo total)
        print("\nValor objetivo (costo total):", model.obj())
    # else:
        # for k in range(V):
        #     for i in range(N):
        #         var = model.s[k,i]
        #         print(f"s[{k},{i}] : bounds={var.lb, var.ub}, value={pyo.value(var, exception=False)}")
        # for idx in model.time_windows:
        #     print(f"time_windows[{idx}] : {model.time_windows[idx].expr}")

milp2a2_solver()