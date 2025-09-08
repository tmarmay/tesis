from sim_settings import DISTANCES_MATRIX_PATH, TIMES_MATRIX_PATH

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"


'''
La diferencia entre distance_matriz.csv y la instancia de VirtualGraph
Es que VirtualGraph representa exacatamente un contexto a resolver
'''

class VirtualGraph:
    def __init__(self):
        self.nodes: list = []
        self.carriers: list = []
        self.shipments: list = []
        self.distances: pd.DataFrame = None
        self.times: pd.DataFrame = None

    def build_node(self, carriers, shipments):
        # primer filtro que se puede mejorar (ej por zona)
        self.carriers = carriers
        self.shipments = shipments
        self.nodes = [carrier.location.place for carrier in carriers]
        self.nodes + [shipment.start.place for shipment in self.shipments]
        self.nodes + [shipment.end.place for shipment in self.shipments]
        self._build_submatrices()
        

    def _build_submatrices(self):
        if not self.nodes:
            return
        '''
        Podria construir una submatriz
        self.distances = self._filter_matrix(self.nodes, 'distances')
        self.times = self._filter_matrix(self.nodes, 'times')
        '''
        self.distances = pd.read_csv(DISTANCES_MATRIX_PATH, index_col=0)
        self.times = pd.read_csv(TIMES_MATRIX_PATH, index_col=0)

    def _filter_matrix(self, node_indexes, matrix_type):
        if matrix_type == 'distances':
                df = pd.read_csv(DISTANCES_MATRIX_PATH, index_col=0)
                missing = set(node_indexes) - set(df.index)
                if missing:
                    raise ValueError(f"Estas ciudades no están en la matriz: {missing}")
                return df.loc[node_indexes, node_indexes]

        elif matrix_type == 'times':
                df = pd.read_csv(TIMES_MATRIX_PATH, index_col=0)
                missing = set(node_indexes) - set(df.index)
                if missing:
                    raise ValueError(f"Estas ciudades no están en la matriz: {missing}")
                return df.loc[node_indexes, node_indexes]
        else:
            raise ValueError("Tipo de matriz desconocido")

    def get_distance(self, node1, node2):
        node1_idx = self.nodes.index(node1)
        node2_idx = self.nodes.index(node2)
        return self.distances[node1_idx, node2_idx]

    def get_time(self, node1, node2):
        node1_idx = self.nodes.index(node1)
        node2_idx = self.nodes.index(node2)
        return self.times[node1_idx, node2_idx]

    def show_problem(self, shipments: bool = True, distance: bool = True, carriers: bool = True, 
                    connections: bool = True, solution: list = [], routes: dict = {}):
        carrier_nodes = []
        shipments_nodes = []

        for c in self.carriers:
            lat, lon = c.location.get_coordinates()
            carrier_nodes.append({'id': c.id, 'lat': float(lat), 'lon': float(lon)})

        for s in self.shipments:
            slat, slon = s.start.get_coordinates()
            elat, elon = s.end.get_coordinates()
            shipments_nodes.append(({'id': s.id, 'lat': float(slat), 'lon': float(slon), 'distance': s.distance},
                                {'id': s.id, 'lat': float(elat), 'lon': float(elon)}))

        fig = go.Figure()

        # Transportistas (círculos azules)
        if carriers:
            fig.add_trace(go.Scattergeo(
                lon=[c["lon"] for c in carrier_nodes],
                lat=[c["lat"] for c in carrier_nodes],
                text=[c["id"] for c in carrier_nodes],
                mode="markers+text",
                marker=dict(size=12, color="blue", symbol="circle"),
                name="Carriers"
            ))

        # Shipments (triángulos)
        if shipments:
            fig.add_trace(go.Scattergeo(
                lon=[s[0]["lon"] for s in shipments_nodes],
                lat=[s[0]["lat"] for s in shipments_nodes],
                text=[s[0]["id"] for s in shipments_nodes],
                mode="markers+text",
                marker=dict(size=12, color="green", symbol="triangle-up"),
                name="Shipments Start"
            ))
            fig.add_trace(go.Scattergeo(
                lon=[s[1]["lon"] for s in shipments_nodes],
                lat=[s[1]["lat"] for s in shipments_nodes],
                text=[s[1]["id"] for s in shipments_nodes],
                mode="markers+text",
                marker=dict(size=12, color="red", symbol="triangle-up"),
                name="Shipments End"
            ))

        # Conexiones entre start y end
        if connections and not solution:
            for s in shipments_nodes:
                fig.add_trace(go.Scattergeo(
                    lon=[s[0]["lon"], s[1]["lon"]],
                    lat=[s[0]["lat"], s[1]["lat"]],
                    mode="lines",
                    line=dict(width=2, dash="dot", color="gray"),
                    opacity=0.5,
                    showlegend=False
                ))

                # Texto en el medio de la línea
                lon_pair = [s[0]["lon"], s[1]["lon"]]
                lat_pair = [s[0]["lat"], s[1]["lat"]]
                mid_lon = sum(lon_pair) / 2
                mid_lat = sum(lat_pair) / 2

                fig.add_trace(go.Scattergeo(
                    lon=[mid_lon],
                    lat=[mid_lat],
                    mode="text",
                    text=[f"{s[0]['distance']}km"],
                    textfont=dict(color="black", size=10),
                    showlegend=False
                ))

        # Graficar las rutas: A y B
        if routes:
            for route_key, route_data in routes.items():
                # A) Línea entre start y end de la misma orden
                for start_end in route_data['route']:
                    start_lat, start_lon = start_end[0].get_coordinates()
                    end_lat, end_lon = start_end[1].get_coordinates()

                    fig.add_trace(go.Scattergeo(
                        lon=[start_lon, end_lon],
                        lat=[start_lat, end_lat],
                        mode="lines",
                        line=dict(width=3, color="blue"),
                        opacity=0.7,
                        name=f"Route {route_key} Segment"
                    ))

                # B) Línea entre end de una orden y start de la siguiente
                for i in range(len(route_data['route']) - 1):
                    current_end_lat, current_end_lon = route_data['route'][i][1].get_coordinates()
                    next_start_lat, next_start_lon = route_data['route'][i+1][0].get_coordinates()

                    fig.add_trace(go.Scattergeo(
                        lon=[current_end_lon, next_start_lon],
                        lat=[current_end_lat, next_start_lat],
                        mode="lines",
                        line=dict(width=3, dash="dash", color="orange"),
                        opacity=0.7,
                        name=f"Route {route_key} Connection"
                    ))

        # Layout
        fig.update_layout(
            geo=dict(
                scope="south america",
                center=dict(lat=-38.4161, lon=-63.6167),
                projection_scale=3,
                showland=True,
                landcolor="rgb(240,240,240)",
                countrycolor="black"
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        fig.show()
