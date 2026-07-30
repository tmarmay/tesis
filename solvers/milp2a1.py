"""
milp2a1.py
Solver Milp for MD-VRP-TW.
2a1 version.
"""
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from models.solutions import Solution

import pyomo.environ as pyo

_TIME_LIMIT_OPTIONS = {
    "highs":  "time_limit",
    "cbc":    "seconds",
    "glpk":   "tmlim",
    "gurobi": "TimeLimit",
}

class MILPSolver(BaseSolver):
    def __init__(self, cfg_milp: dict=None):
        self.solver     = "highs" if cfg_milp is None else cfg_milp['solver']
        self.time_limit = None    if cfg_milp is None else cfg_milp.get('time_limit')

    def objective_rule(self, model):
        # Costo de los viajes
        travel_cost = sum(self.insta.cost_matrix[i][j] * model.x[k, i, j] for k in range(self.insta.V) for i in range(self.insta.N) for j in range(self.insta.N))
        
        # Costo de los vehículos (F_k) basado en las variables u_k
        vehicle_cost = sum(self.insta.F[k] * model.u[k] for k in range(self.insta.V))  # F[k] es el costo del vehículo k
        
        #time_cost = sum(model.s[k, i] for k in range(V) for i in range(N))
        
        # La función objetivo es la suma de ambos costos
        return travel_cost + vehicle_cost #+ time_cost

    #Cada nodo debe ser visitado exactamente una vez
    def constraint_32_eq(self, model, i):
        # i es el cliente
        return sum(model.x[k, i, j] for k in range(self.insta.V) for j in range(self.insta.N) if i != j) == 1

    #Tiene que salir del depot
    def constraint_34_eq(self, model, k):
        depot = self.insta.DEPOTS[k]
        return sum(model.x[k, depot, j] for j in range(self.insta.CUSTOMERS) if j != depot) == model.u[k]

    #Tiene que volver al depot
    def constraint_36_eq(self, model, k):
        ret = self.insta.RETURNS_milp[k]
        return sum(model.x[k, i, ret] for i in range(self.insta.N) if i != ret) == model.u[k]

    #Conservascion flujo
    def constraint_35_eq(self, model, h, k):
        depot = self.insta.DEPOTS[k]
        ret = self.insta.RETURNS_milp[k]
        
        if h == depot or h == ret:
            return pyo.Constraint.Skip
        
        inpt = (model.x[k, i, h] for i in range(self.insta.N) if i != h)
        outpt = (model.x[k, h, j] for j in range(self.insta.N) if j != h)
        return sum(inpt) - sum(outpt) == 0

    #Variables para los vehiculos
    def constraint_min_vehicle(self, model):
        return sum(model.u[k] for k in range(self.insta.V)) >= 1

    #Restriccion de capacidad
    def constraint_33_ub(self, model, k):
        return sum(model.x[k, i, j] * self.insta.demands[i] for i in self.insta.C for j in range(self.insta.N) if i != j) <= self.insta.Q[k]

    #Restriccion de tiempo 
    def constraint_37_ub(self, model, k, i, j):
        if i == j:
            return pyo.Constraint.Skip
        Mij = self.insta.li[i] + self.insta.tij[i][j] - self.insta.ei[j]  # Big-M
        return model.s[k,i] + self.insta.tij[i][j] - Mij * (1 - model.x[k,i,j]) <= model.s[k,j]

    def s_bounds(self, model, k, i):
        return (self.insta.ei[i], self.insta.li[i])  # ventana de tiempo para el nodo i

    # Para cada vehiculo k: si usa algun arco (i,j) entonces u[k] = 1 (Big-M)
    def aux1(self, model, k):
        return sum(model.x[k, i, j] for i in range(self.insta.N) for j in range(self.insta.N) if i != j) <= self.insta.N * model.u[k]

    # ====== Main Function ======
    def milp2a2_solver(self, instance: ProblemInstance):
        self.insta = instance
        # Crear el modelo de optimización
        model = pyo.ConcreteModel()

        # Definir las variables
        model.x = pyo.Var(range(instance.V), range(instance.N), range(instance.N), domain=pyo.Binary)  # xijk binaria
        model.u = pyo.Var(range(instance.V), domain=pyo.Binary)  # uk binaria
        model.s = pyo.Var(range(instance.V), range(instance.N), domain=pyo.Reals, bounds=self.s_bounds)  # sik

        # Inicializar x[k, i, j] = 0 para las combinaciones donde i == j
        for k in range(instance.V):
            for i in range(instance.N):
                model.x[k, i, i].fix(0)  # Fijar x[k, i, j] a 0 cuando i == j

        # Prohibir que el vehículo k pase por el depósito de otro vehículo k'
        for k in range(instance.V):
            for k2 in range(instance.V):
                if k2 == k:
                    continue
                for d in {instance.DEPOTS[k2], instance.RETURNS_milp[k2]}:
                    for i in range(instance.N):
                        if i != d:
                            model.x[k, i, d].fix(0)
                            model.x[k, d, i].fix(0)

        # Función objetivo: Minimizar los costos de los viajes
        model.obj = pyo.Objective(rule=self.objective_rule, sense=pyo.minimize)
        
        model.visit_once = pyo.Constraint(instance.C, rule=self.constraint_32_eq)
        model.from_depot = pyo.Constraint(range(instance.V), rule=self.constraint_34_eq)
        model.back2_return = pyo.Constraint(range(instance.V), rule=self.constraint_36_eq)
        model.flow = pyo.Constraint(range(instance.N), range(instance.V), rule=self.constraint_35_eq)
        model.uk = pyo.Constraint(rule=self.constraint_min_vehicle)
        model.capacity = pyo.Constraint(range(instance.V), rule=self.constraint_33_ub)
        model.time_windows = pyo.Constraint(range(instance.V), range(instance.N), range(instance.N), rule=self.constraint_37_ub)
        
        model.aux_link_x_u = pyo.Constraint(range(instance.V), rule=self.aux1)
        
        # Resolver el modelo
        solver = pyo.SolverFactory(self.solver)
        if self.time_limit is not None:
            opt_key = _TIME_LIMIT_OPTIONS.get(self.solver)
            if opt_key:
                solver.options[opt_key] = self.time_limit

        results = solver.solve(model, tee=False)

        # ===============================
        # EXTRAER SOLUCIÓN
        # ===============================
        _ok = {pyo.TerminationCondition.optimal, pyo.TerminationCondition.feasible, pyo.TerminationCondition.maxTimeLimit}
        # CBC reports intermediateNonInteger when time limit is hit with no MIP incumbent.
        _timed_out_no_incumbent = {pyo.TerminationCondition.intermediateNonInteger}
        if results.solver.termination_condition not in _ok:
            timed_out = results.solver.termination_condition in _timed_out_no_incumbent
            return {}, float("inf"), list(instance.C), timed_out

        if pyo.value(model.obj, exception=False) is None:
            return {}, float("inf"), list(instance.C), False

        # CBC/GLPK may load a trivial or LP-relaxation "solution" when no MIP
        # incumbent was found. Detect this by checking that at least one u[k] ≈ 1.
        timed_out = results.solver.termination_condition == pyo.TerminationCondition.maxTimeLimit
        if not any(
            (v := pyo.value(model.u[k], exception=False)) is not None and v > 1 - 1e-4
            for k in range(instance.V)
        ):
            return {}, float("inf"), list(instance.C), timed_out

        costo_total = pyo.value(model.obj)

        rutas = {}
        visitados = set()

        for k in range(instance.V):

            if pyo.value(model.u[k]) < 0.5:
                continue  # vehículo no usado

            depot = instance.DEPOTS[k]
            ret = instance.RETURNS_milp[k]

            # ===============================
            # Arcos activos del vehículo k
            # ===============================
            arcos_k = [
                (i, j)
                for i in range(instance.N)
                for j in range(instance.N)
                if pyo.value(model.x[k, i, j]) > 0.5
            ]

            if not arcos_k:
                # vehículo marcado como usado pero sin ruta → error del modelo
                continue

            # sucesor único por nodo
            succ = {i: j for i, j in arcos_k}

            # ===============================
            # Reconstrucción de la ruta
            # ===============================
            ruta = [depot]
            actual = depot
            usados = {depot}

            while actual != ret:
                if actual not in succ:
                    raise RuntimeError(
                        f"Ruta rota: no hay sucesor desde {actual} (vehículo {k})"
                    )

                siguiente = succ[actual]

                if siguiente in usados:
                    raise RuntimeError(
                        f"Ciclo detectado en vehículo {k}: {siguiente}"
                    )

                ruta.append(siguiente)
                usados.add(siguiente)
                actual = siguiente

            rutas[depot] = ruta

            # clientes visitados
            visitados |= set(n for n in ruta if n in instance.C)

        # ===============================
        # CLIENTES NO ATENDIDOS
        # ===============================
        no_visitados = [c for c in instance.C if c not in visitados]

        return rutas, costo_total, no_visitados, timed_out

    def solve(self, instance: ProblemInstance) -> Solution:
        rutas, costo, no_visitados, timed_out = self.milp2a2_solver(instance)
        return Solution(routes=rutas, total_cost=costo, feasible=len(no_visitados)==0, unserved_customers=no_visitados, timed_out=timed_out)

    def is_stochastic(self) -> bool:
        return False

    def get_solver_name(self) -> str:
        return self.solver

"""
tengo que boorar pero lo dejo por las dudas para debug
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
            for k in range(instance.V):
                for i in range(instance.N):
                    for j in range(instance.N):
                        if model.x[k, i, j].value:  # Solo imprimir si xijk es 1 (viaje hecho)
                            print(f"x[{k},{i},{j}] = {model.x[k, i, j].value}")
            # Imprimir las variables u (carga de los vehículos)
            print("\nCarga de los vehículos (uk):")
            for k in range(instance.V):
                print(f"u[{k}] = {model.u[k].value}")

            print("\nTiempos de servicio (ski):")
            for k in range(instance.V):
                for i in range(instance.N):
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

"""
