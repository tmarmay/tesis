class SolutionChecker:
    """
    Verifica la correctitud de una solución para el MD-VRP-TW.
    """

    def __init__(self, insta):
        self.insta = insta

    def check(self, solution: dict) -> bool:
        """
        Verifica que la solución sea factible respecto a todas las restricciones.

        Args:
            solution: dict {vehicle: [route]} donde route es lista de nodos
                      comenzando en DEPOTS[k] y terminando en RETURNS_milp[k].

        Returns:
            True si la solución es factible, False en caso contrario.
        """
        checks = [
            self._check_depot_and_return,
            self._check_customers_visited_once,
            self._check_capacity,
            self._check_time_windows,
            self._check_valid_vehicle_keys,
            self._check_no_intra_route_duplicates
        ]
        return all(check(solution) for check in checks)

    # -- Restricción: salida del depot y regreso al return (constraints 34, 36) --

    def _check_depot_and_return(self, solution: dict) -> bool:
        for k, route in solution.items():
            v = k - self.insta.DEPOTS[0]
            depot = self.insta.DEPOTS[v]
            ret = self.insta.RETURNS_milp[v]
            if route[0] != depot:
                print(f"[FAIL] constraint_34 - Vehículo {k}: la ruta no comienza en su depot "
                      f"(esperado {depot}, encontrado {route[0]}).")
                return False
            if route[-1] != ret:
                print(f"[FAIL] constraint_36 - Vehículo {k}: la ruta no termina en su return "
                      f"(esperado {ret}, encontrado {route[-1]}).")
                return False
        return True

    # -- Restricción: cada cliente visitado exactamente una vez (constraint_32) --

    def _check_customers_visited_once(self, solution: dict) -> bool:
        visited = []
        for k, route in solution.items():
            for node in route[1:-1]:
                if node in self.insta.C:
                    visited.append(node)

        customers_set = set(self.insta.C)
        visited_set = set(visited)
        

        if visited_set != customers_set:
            missing = customers_set - visited_set
            extra = visited_set - customers_set
            if missing:
                print(f"[FAIL] constraint_32 - Clientes no visitados: {missing}.")
            if extra:
                print(f"[FAIL] constraint_32 - Nodos no válidos visitados como clientes: {extra}.")
            return False

        if len(visited) != len(visited_set):
            duplicates = [n for n in visited_set if visited.count(n) > 1]
            print(f"[FAIL] constraint_32 - Clientes visitados más de una vez: {duplicates}.")
            return False

        return True

    # -- Restricción: capacidad del vehículo (constraint_33) --

    def _check_capacity(self, solution: dict) -> bool:
        for k, route in solution.items():
            v = self.insta.DEPOTS.index(k)
            load = sum(
                self.insta.demands[i]
                for i in route[1:-1]
                if i in self.insta.C
            )
            if load > self.insta.Q[v]:
                print(f"[FAIL] constraint_33 - Vehículo {k}: capacidad excedida "
                    f"(carga={load}, Q[{v}]={self.insta.Q[v]}).")
                return False
        return True

    # -- Restricción: ventanas de tiempo (constraint_37 + s_bounds) --

    def _check_time_windows(self, solution: dict) -> bool:
        for k, route in solution.items():
            current_time = self.insta.ei[route[0]]

            for idx in range(len(route) - 1):
                i = route[idx]
                j = route[idx + 1]

                arrival = current_time + self.insta.tij[i][j]

                # Violación de la ventana superior (s_bounds upper)
                if arrival > self.insta.li[j]:
                    print(f"[FAIL] constraint_37/s_bounds - Vehículo {k}: llegada al nodo {j} "
                          f"en t={arrival:.2f} excede li[{j}]={self.insta.li[j]}.")
                    return False

                # Espera si se llega antes de la ventana (wait at j)
                current_time = max(arrival, self.insta.ei[j])

                # Tiempo de servicio
                # if j in self.insta.C:
                #     current_time += self.insta.service_time[j]

        return True

    # -- Restricción: claves de vehículo válidas --

    def _check_valid_vehicle_keys(self, solution: dict) -> bool:
        valid_keys = set(range(self.insta.C[-1] + 1, self.insta.C[-1] + self.insta.V + 1))
        solution_keys = set(solution.keys())

        invalid = solution_keys - valid_keys
        if invalid:
            print(f"[FAIL] vehicle_keys - Índices de vehículo inválidos: {invalid} "
                f"(válidos: {range(self.insta.C[-1] + 1, self.insta.C[-1] + self.insta.V)}).")
            return False
        return True

    # -- Restricción: cliente visitado dos veces por el mismo vehículo --

    def _check_no_intra_route_duplicates(self, solution: dict) -> bool:
        for k, route in solution.items():
            customers_in_route = [n for n in route[1:-1] if n in self.insta.C]
            seen = set()
            for node in customers_in_route:
                if node in seen:
                    print(f"[FAIL] intra_route_duplicate - Vehículo {k}: "
                        f"el cliente {node} aparece más de una vez en su ruta.")
                    return False
                seen.add(node)
        return True