from models.problem_instance import ProblemInstance

import numpy as np

CUSTOMERS = 2
cij = np.array([
# 0   1   2   3
[99,  1,  99,  5],  
[ 50, 99,  99,  5],  
[ 20,  1, 99,  99],  
[ 5,  5,  5, 99],  
])

tij = np.array([
# 0   1   2   3   4   5   6   7   8   
[99,  5,  5,  5],  
[ 5, 99,  5,  5],  
[ 5,  5, 99,  5],  
[ 5,  5,  5, 99],  
])

#DIM(ei/li) = customers +  v + returns
V = 1
RETURNS = V
cheaper_route = ProblemInstance(
    name="Infeasible cause there's more demand than capacity",
    V=1,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[0, 0] + [0 for _ in range(V + RETURNS)],
    li=[30, 30] + [100 for _ in range(V + RETURNS)],
    F=[5 for _ in range(V)],
    demands=[],
    Q=[]
)