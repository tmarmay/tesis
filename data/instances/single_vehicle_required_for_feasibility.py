from models.problem_instance import ProblemInstance

import numpy as np

CUSTOMERS = 2
cij = np.array([
# 0  1  2  3  4  5
[99, 3, 3, 3, 50, 50],  
[3, 99, 3, 3, 3, 3],  
[3, 3, 99, 3, 3, 3],
[3, 3, 3, 99, 3, 3],  
[50, 3, 3, 3, 99, 3],
[50, 3, 3, 3, 3, 99],  
])

tij = np.array([
# 0  1  2  3  4  5
[99, 3, 3, 3, 50, 50],  
[3, 99, 3, 3, 3, 3],  
[3, 3, 99, 3, 3, 3],
[3, 3, 3, 99, 3, 3],  
[50, 3, 3, 3, 99, 3],
[50, 3, 3, 3, 3, 99],  
])

#DIM(ei/li) = customers +  v + returns
V = 2
RETURNS = V
single_vehicle_required = ProblemInstance(
    name="Using more vehicules make solution infeasible",
    V=V,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[0, 5, 0, 0, 10, 10],
    li=[5, 10, 100, 100, 14, 14],
    F=[5 for _ in range(V)],
    demands=[],
    Q=[]
)