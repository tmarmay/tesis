import numpy as np
from models.problem_instance import ProblemInstance

class SyntheticGenerator:
    def __init__(self, *, cfg_experiment: dict, cfg_generator: dict):
        
        cost_range=cfg_generator['cost_range'] 
        cost_ranges=cfg_generator['matrix_costs_ranges']
        tw_tightness=cfg_generator['tw_tightness']
        time_windows_tightness=cfg_generator['time_windows_tightness']
        self.num_customers = cfg_experiment['num_customers']
        self.num_vehicles = cfg_experiment['num_vehicles']
        self.capacity = list(cfg_experiment['capacity']) * self.num_vehicles
        self.vehicle_penalty = cfg_experiment['vehicle_penalty']
        self.customer_demand = cfg_experiment['customer_demand']
        self.cost_low, self.cost_high = cost_ranges[cost_range]
        self.tw_low, self.tw_high = time_windows_tightness[tw_tightness] #Representa el ancho de las ventanas; no el inicio/fin
        self.tw_min_value, self.tw_max_value = cfg_generator['time_windows_values']
        self.seed = cfg_experiment['seed']
        self.T_MAX = np.inf

        self.rng = np.random.default_rng(self.seed)
        
    def _generate_tmax(self, tij, routes, DEPOTS, RETURNS) -> None:
        """
        T_MAX basado en la ruta más larga de la solución constructiva,
        con un margen del 50% para garantizar factibilidad.
        
        ANTES: se calculaba como el promedio de la suma de filas de tij,
        lo que podía ser insuficiente para rutas largas con muchos clientes
        y producía ventanas de tiempo infactibles (li < ei tras clipear con T_MAX).
        """
        max_route_time = 0
        for v in range(self.num_vehicles):
            depot = DEPOTS[v]
            ret = RETURNS[v]
            route = routes[v]
            
            time = 0
            current = depot
            for c in route:
                time += tij[current][c]
                current = c
            time += tij[current][ret]
            max_route_time = max(max_route_time, time)

        # margen del 50% sobre la ruta más costosa en tiempo
        self.T_MAX = int(max_route_time * 1.5) + 1

    def _generate_feasible_time_windows(self, tij) -> tuple[list,list]:
        """
        Genera ventanas garantizando al menos una solución factible.
        Usa construcción greedy por capacidad.
        """
        TW_DIM = self.num_customers + 2 * self.num_vehicles
        C = [i for i in range(self.num_customers)] #CUSTOMERS
        DEPOTS = [i for i in range(C[-1] + 1, C[-1] + 1 + self.num_vehicles)]
        RETURNS = [i for i in range(C[-1] + self.num_vehicles + 1, TW_DIM)]
        
        routes = [[] for _ in range(self.num_vehicles)]
        remaining_capacity = self.capacity.copy()

        customers = [i for i in range(self.num_customers)]
        self.rng.shuffle(customers)

        # Asignación de rutas greedy
        v = 0
        for c in customers:
            demand = self.customer_demand
            while v < self.num_vehicles and remaining_capacity[v] < demand:
                v += 1
            if v == self.num_vehicles:
                raise ValueError("Instancia base infactible por capacidad.")
            routes[v].append(c)
            remaining_capacity[v] -= demand

        # T_MAX calculado sobre las rutas reales
        self._generate_tmax(tij=tij, routes=routes, DEPOTS=DEPOTS, RETURNS=RETURNS)
        # Guardamos la solución constructiva para calcular real_cost en generate()
        self._reference_routes = routes
        self._reference_depots = DEPOTS
        self._reference_returns = RETURNS

        ei = [0] * TW_DIM
        li = [self.T_MAX] * TW_DIM

        # Simulación de recorrido para obtener arrival_times
        arrival_times = {}
        for v in range(self.num_vehicles):
            depot = DEPOTS[v]
            current = depot
            time = 0
            for c in routes[v]:
                travel = tij[current][c]
                time += travel
                arrival_times[c] = time
                #time += service_time
                current = c
            return_node = RETURNS[v]
            time += tij[current][return_node]

        # Ventanas centradas en arrival_time con ancho controlado por tw_low/tw_high
        for c in range(self.num_customers):
            arrival = arrival_times[c]
            # slack depende de ancho permitido
            base_width = self.rng.integers(self.tw_low, self.tw_high)
            left_slack = self.rng.uniform(0.3, 0.7) * base_width
            right_slack = base_width - left_slack
            ei[c] = max(0, int(arrival - left_slack))
            li[c] = min(self.T_MAX, int(arrival + right_slack))

            # Garantía mínima de ancho de ventana
            if li[c] <= ei[c]:
                li[c] = ei[c] + 5

        for d in DEPOTS + RETURNS:
            ei[d] = 0
            li[d] = self.T_MAX

        return ei, li


    def generate(self) -> ProblemInstance:
        """
        Genera una instancia MD-VRP-TW sintética
        """
        n = self.num_customers
        V = self.num_vehicles

        # nodos: [customers] [depots] [returns]
        N = n + 2 * V

        # matriz de costos / tiempos (simétrica)
        M = self.rng.integers(self.cost_low, self.cost_high, size=(N, N))
        cost_matrix = (M + M.T) // 2
        np.fill_diagonal(cost_matrix, 99)

        tij = self.rng.integers(5, 10, size=(N, N))

        ei, li = self._generate_feasible_time_windows(tij=tij)

        real_cost = 0
        for v in range(V):
            if not self._reference_routes[v]:
                continue
            route = [self._reference_depots[v]] + self._reference_routes[v] + [self._reference_returns[v]]
            for a, b in zip(route[:-1], route[1:]):
                real_cost += int(cost_matrix[a][b])
            real_cost += self.vehicle_penalty

        pi = ProblemInstance(
            name=f"synthetic_n{n}_v{V}_seed{self.seed}",
            V=V,
            CUSTOMERS=n,
            cost_matrix=cost_matrix,
            tij=tij,
            ei=ei,
            li=li,
            F=[self.vehicle_penalty for _ in range(V)],
            demands=[1 for _ in range(n)],
            Q=self.capacity,
            reference_cost=real_cost,
        )
        self._validate_instance(instance=pi, verbose=True)
        return pi 
    
    def _validate_instance(self, instance: ProblemInstance, verbose: bool = True) -> bool:
        """
        Verifica si una ProblemInstance es potencialmente factible chequeando
        todas las restricciones del MILP (sin resolverlo).

        Restricciones verificadas:
          [C1]  Capacidad total: suma de demandas <= capacidad total de la flota.
          [C2]  Capacidad por vehículo: al menos un vehículo puede atender a cada cliente.
          [C3]  Ventanas de tiempo no degeneradas: ei[i] < li[i] para todo nodo i.
          [C4]  T_MAX coherente: li[i] <= T_MAX para todo i.
          [C5]  Alcanzabilidad temporal: para cada cliente c existe al menos un depot d
                tal que ei[d] + tij[d][c] <= li[c]  (se puede llegar a tiempo).
          [C6]  Retorno posible: para cada cliente c existe al menos un return r tal que
                ei[c] + tij[c][r] <= li[r]  (se puede volver a tiempo).
          [C7]  Conectividad temporal entre clientes consecutivos: para cada par (i, j)
                que podría ser consecutivo, se verifica que ei[i] + tij[i][j] <= li[j].
                Se reporta qué fracción de pares son alcanzables.
          [C8]  Número de vehículos suficiente: ceil(demanda_total / Q_max) <= V.

        Retorna True si todas las restricciones se cumplen, False en caso contrario.
        """
        errors = []
        warnings = []

        tij = instance.tij
        ei = instance.ei
        li = instance.li
        C = instance.C
        DEPOTS = instance.DEPOTS
        RETURNS = instance.RETURNS_milp
        V = instance.V
        Q = instance.Q
        demands = instance.demands
        N = instance.N
        T_MAX = max(li)  # T_MAX implícito de la instancia

        # ----------------------------------------------------------
        # [C1] Capacidad total de la flota
        # ----------------------------------------------------------
        total_demand = sum(demands)
        total_capacity = sum(Q)
        if total_demand > total_capacity:
            errors.append(
                f"[C1] INFACTIBLE: demanda total ({total_demand}) > "
                f"capacidad total de la flota ({total_capacity})."
            )
        else:
            if verbose:
                print(f"[C1] OK — demanda total={total_demand}, capacidad flota={total_capacity}.")

        # ----------------------------------------------------------
        # [C2] Capacidad individual: ¿algún vehículo puede atender a cada cliente?
        # ----------------------------------------------------------
        max_q = max(Q)
        if any(d > max_q for d in demands):
            bad = [i for i, d in enumerate(demands) if d > max_q]
            errors.append(
                f"[C2] INFACTIBLE: clientes {bad} tienen demanda > capacidad máxima "
                f"de cualquier vehículo ({max_q})."
            )
        else:
            if verbose:
                print(f"[C2] OK — demanda por cliente={set(demands)}, Q_max={max_q}.")

        # ----------------------------------------------------------
        # [C3] Ventanas no degeneradas
        # ----------------------------------------------------------
        degenerate = [i for i in range(N) if ei[i] >= li[i]]
        if degenerate:
            errors.append(
                f"[C3] INFACTIBLE: nodos {degenerate} tienen ei >= li "
                f"(ventana de tiempo degenerada o invertida)."
            )
        else:
            if verbose:
                print(f"[C3] OK — todas las ventanas tienen ei < li.")

        # ----------------------------------------------------------
        # [C4] T_MAX coherente
        # ----------------------------------------------------------
        over_tmax = [i for i in range(N) if li[i] > T_MAX]
        if over_tmax:
            warnings.append(
                f"[C4] ADVERTENCIA: nodos {over_tmax} tienen li > T_MAX={T_MAX} "
                f"(inconsistencia interna)."
            )
        else:
            if verbose:
                print(f"[C4] OK — todos li <= T_MAX={T_MAX}.")

        # ----------------------------------------------------------
        # [C5] Alcanzabilidad: depot -> cliente
        # ----------------------------------------------------------
        unreachable_customers = []
        for c in C:
            reachable = False
            for k, depot in enumerate(DEPOTS):
                # El vehículo k sale de depot no antes de ei[depot]=0
                earliest_arrival = ei[depot] + tij[depot][c]
                if earliest_arrival <= li[c]:
                    reachable = True
                    break
            if not reachable:
                unreachable_customers.append(c)

        if unreachable_customers:
            errors.append(
                f"[C5] INFACTIBLE: clientes {unreachable_customers} no son alcanzables "
                f"desde ningún depot dentro de su ventana de tiempo."
            )
        else:
            if verbose:
                print(f"[C5] OK — todos los clientes son alcanzables desde al menos un depot.")

        # ----------------------------------------------------------
        # [C6] Retorno posible: cliente -> return node
        # ----------------------------------------------------------
        no_return_customers = []
        for c in C:
            can_return = False
            for k, ret in enumerate(RETURNS):
                earliest_return = ei[c] + tij[c][ret]
                if earliest_return <= li[ret]:
                    can_return = True
                    break
            if not can_return:
                no_return_customers.append(c)

        if no_return_customers:
            errors.append(
                f"[C6] INFACTIBLE: clientes {no_return_customers} no pueden regresar "
                f"a ningún nodo de retorno dentro de su ventana."
            )
        else:
            if verbose:
                print(f"[C6] OK — todos los clientes pueden retornar a algún nodo de retorno.")

        # ----------------------------------------------------------
        # [C7] Fracción de pares cliente-cliente alcanzables en tiempo
        # ----------------------------------------------------------
        total_pairs = 0
        reachable_pairs = 0
        for i in C:
            for j in C:
                if i == j:
                    continue
                total_pairs += 1
                if ei[i] + tij[i][j] <= li[j]:
                    reachable_pairs += 1

        if total_pairs > 0:
            frac = reachable_pairs / total_pairs
            msg = (
                f"[C7] Pares cliente-cliente alcanzables en tiempo: "
                f"{reachable_pairs}/{total_pairs} ({frac:.1%})."
            )
            if frac < 0.1:
                warnings.append(msg + " — MUY POCOS pares alcanzables, instancia probablemente infactible.")
            elif verbose:
                print(msg)

        # ----------------------------------------------------------
        # [C8] Número de vehículos suficiente
        # ----------------------------------------------------------
        import math
        min_vehicles_needed = math.ceil(total_demand / max_q)
        if min_vehicles_needed > V:
            errors.append(
                f"[C8] INFACTIBLE: se necesitan al menos {min_vehicles_needed} vehículos "
                f"pero solo hay {V}."
            )
        else:
            if verbose:
                print(f"[C8] OK — vehículos disponibles={V}, mínimo necesario={min_vehicles_needed}.")

        # ----------------------------------------------------------
        # Resumen
        # ----------------------------------------------------------
        print()
        if warnings:
            for w in warnings:
                print(f"  ⚠  {w}")
        if errors:
            for e in errors:
                print(f"  ✗  {e}")
            print(f"\n  → Instancia '{instance.name}': POTENCIALMENTE INFACTIBLE "
                  f"({len(errors)} error(es) encontrado(s)).\n")
            return False
        else:
            print(f"  ✓  Instancia '{instance.name}': pasa todas las verificaciones de factibilidad.\n")
            return True
        
    def __str__(self) -> str:
        lines = []

        lines.append("SyntheticGenerator")
        lines.append("-" * 18)

        lines.append(f"Vehicles: {self.num_vehicles}")
        lines.append(f"Customers: {self.num_customers}")
        lines.append(f"Total nodes: {self.num_customers + 2 * self.num_vehicles}")

        lines.append("")
        lines.append("Cost matrix:")
        lines.append(f"  range: [{self.cost_low}, {self.cost_high}]")
        lines.append("  symmetric: True")

        lines.append("")
        lines.append("Time windows:")
        lines.append(f"  T_MAX: {self.T_MAX}")
        lines.append(f"  width range: [{self.tw_low}, {self.tw_high}]")

        lines.append("")
        lines.append("Vehicle capacity:")
        lines.append(f"  Q per vehicle: {self.capacity}")

        if hasattr(self, "seed"):
            lines.append("")
            lines.append(f"Random seed: {self.seed}")

        return "\n".join(lines)