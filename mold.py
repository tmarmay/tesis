from sim_settings import N, M
from solvers import dummy_nnp, vns, milp2a1
from models.carrier import Carrier
from models.shipment import Shipment
from models.network_representation import VirtualGraph
from solvers.utils_vrp import cost

from matplotlib import pyplot as plt
import pprint

class Simulation():
    def __init__(self):
        self.shipments = []
        self.available_carriers = []
        self.unavailable_carriers = []
        self.graph = VirtualGraph()

    def init_sim(self):
        self.generate_carriers()
        self.generate_shipments()
        self.graph.build_node(self.available_carriers, self.shipments)

    def generate_carriers(self):
        for _ in range(N):
            carrier = Carrier()
            if carrier.available:
                self.available_carriers.append(carrier)
            else:
                self.unavailable_carriers.append(carrier)
    
    def generate_shipments(self):
        for _ in range(M):
            shipment = Shipment()
            self.shipments.append(shipment)

    def available_carriers_coords(self) -> list:
        carriers_coords = []
        for carrier in self.available_carriers:
            carriers_coords.append(carrier.get_coordinates())
        return carriers_coords

    def unavailable_carriers_coords(self) -> list:
        carriers_coords = []
        for carrier in self.unavailable_carriers:
            carriers_coords.append(carrier.get_coordinates())
        return carriers_coords

    def start_shipments_coords(self) -> list:
        shipments = []
        for ship in self.shipments:
            shipments.append(ship.get_start_coordinates())
        return shipments

    def end_shipments_coords(self) -> list:
        shipments = []
        for ship in self.shipments:
            shipments.append(ship.get_end_coordinates())
        return shipments

    def shipments_coords(self) -> list:
        start = self.start_shipments_coords()
        end = self.end_shipments_coords()
        return [elem for pair in zip(start, end) for elem in pair]
    
    def prprint(self, sol):
        pprint.pprint(sol)

    def plot_cost(self, vns: list):
        xs, ys, zs = [], [], []
        it = 0
        for x,y in vns:
            if it == 0:
                plt.scatter(it, x, marker="o", label=f"solucion inicial km (nnp)", color='blue')
                plt.scatter(it, y, marker="o", label=f"solucion inicial $ (nnp)", color='blue')
            else:
                xs.append(it)
                ys.append(x)
                zs.append(y)
            it += 1
        plt.plot(xs, ys, marker="o", label=f"vns km", color='green')
        plt.plot(xs, zs, marker="o", label=f"vns $", color='orange')

        plt.xlabel("Iteraciones")
        plt.ylabel("km")
        plt.title("Mejora sobre iteraciones en km")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_target(self, vns: list):
        xs, ys, it = [], [], 0
        for x, y in vns:
            if it == 0:
                plt.scatter(x, y, marker="o", label=f"solucion inicial (nnp)", color='blue')
            else:
                xs.append(x)
                ys.append(y)
            it += 1
        plt.plot(xs, ys, marker="o", label=f"vns", color='green')

        plt.xlabel("Iteraciones")
        plt.ylabel("α * km + β cost")
        plt.title("Mejora sobre iteraciones en funcion costo")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_grant(self, sol):
        data = []
        for key, value in sol.items():
            if not 'carrier' in key:
                continue
            route_obj = value['route_obj']

            for idx, shipment in enumerate(route_obj.route):
                earliest = shipment.earliest_time
                latest = shipment.latest_time
                start = route_obj.start_times[idx]
                end = route_obj.end_times[idx]
                data.append((key, shipment.id, earliest, latest, start, end))

        fig, ax = plt.subplots()

        # Paleta con muchos colores
        colors = ["skyblue", "lightgreen", "lightcoral", "plum",
                "khaki", "salmon", "turquoise", "orange"]

        y_labels = list(set(carrier for carrier, _, _, _, _, _ in data))
        y_pos = {carrier: i * 10 for i, carrier in enumerate(y_labels)}

        for carrier in y_labels:
            carrier_data = [(p, e, l, s, t) for c, p, e, l, s, t in data if c == carrier]
            carrier_data.sort(key=lambda x: x[1])  # ordenar por ID de pedido

            active_intervals = []  # [(latest, color_idx)]
            for pedido, earliest, latest, start, end in carrier_data:
                # liberar colores de intervalos que ya terminaron
                active_intervals = [(l, ci) for l, ci in active_intervals if l > earliest]

                # buscar el primer color libre
                used_colors = {ci for _, ci in active_intervals}
                for ci in range(len(colors)):
                    if ci not in used_colors:
                        color_idx = ci
                        break

                active_intervals.append((latest, color_idx))

                # Dibujar la barra con earliest/latest
                ax.broken_barh([(earliest, latest - earliest)], (y_pos[carrier], 9),
                            facecolors=colors[color_idx])
                ax.text(earliest + (latest - earliest) / 2, y_pos[carrier] + 4,
                        pedido, ha="center", va="center", fontsize=8)

                # Círculo en start_time real
                ax.scatter(start, y_pos[carrier] + 4, color="black", marker="o", zorder=5, label='Start')

                # Triángulo en end_time real
                ax.scatter(end, y_pos[carrier] + 4, color="red", marker="^", zorder=5, label='End')

        ax.set_xlabel("Tiempo (dias)")
        ax.set_ylabel("Transportistas")
        ax.set_yticks([y_pos[c] + 5 for c in y_labels])
        ax.set_yticklabels(y_labels)
        ax.grid(True)
        plt.title("Solucion")
        plt.show()

    def solve(self, solver="dummy_nnp"):
        for s in self.shipments:
            print(f"De {s.start.place} a {s.end.place} tw: [{s.earliest_time}, {s.latest_time}]")

        #if solver == "dummy_nnp":
        # nnp_sol = dummy_nnp.mdvrptw_solver(self.available_carriers+self.unavailable_carriers, self.shipments)
        # self.prprint(nnp_sol)
        # print('------')

        #if solver == "vns":
        #self.graph.show_problem(carriers=False)
        # solution = vns.mdvrptw_solver(self.available_carriers + self.unavailable_carriers, self.shipments)
        # self.prprint(solution)
        # from visualizations import graph
        
        # if solution['solved']:
        #     self.plot_cost(solution['target_history'])
        #     self.plot_target(solution['target_history'])
        #     self.plot_grant(solution)

        milp2a1.milp2a2_solver()
        


s = Simulation()
s.init_sim()
s.solve(solver="dummy_nnp")
#s.graph.show_problem(carriers=False)