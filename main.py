from sim_settings import N, M
from solvers import dummy_nnp, vns
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


    def plot(self, vns: list):
        xs, ys = [], []
        it = 0
        for x,y in vns:
            if it == 0 :
                # x por cost(x,y)
                plt.scatter(it, x, marker="o", label=f"nnp isol", color='blue')
            else:
                xs.append(it)
                ys.append(x)
            it += 1
        plt.plot(xs, ys, marker="o", label=f"vns", color='green')

        plt.xlabel("iteracion")
        plt.ylabel("km")
        plt.title("Mejora")
        plt.legend()
        plt.grid(True)
        plt.show()

        # plt.scatter(xs,ys)
        # plt.xlabel("km")
        # plt.ylabel("cost")
        # plt.legend()
        # plt.show()
    def solve(self, solver="dummy_nnp"):
        for s in self.shipments:
            print(f"De {s.start.place} a {s.end.place} tw: [{s.earliest_time}, {s.latest_time}]")

        #if solver == "dummy_nnp":
        # nnp_sol = dummy_nnp.mdvrptw_solver(self.available_carriers+self.unavailable_carriers, self.shipments)
        # self.prprint(nnp_sol)
        # print('------')

        #if solver == "vns":
        # #self.graph.show_problem(carriers=False)
        solution = vns.mdvrptw_solver(self.available_carriers + self.unavailable_carriers, self.shipments)
        self.prprint(solution)

        if solution['solved']:
            self.plot(solution['target_history'])
        


s = Simulation()
s.init_sim()
s.solve(solver="dummy_nnp")
#s.graph.show_problem(carriers=False)