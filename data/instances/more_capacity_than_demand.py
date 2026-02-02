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
feasible_cause_capacity = ProblemInstance(
    name="Feasible cause there's more capacity than demand",
    V=1,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[0, 0] + [0 for _ in range(V + RETURNS)],
    li=[30, 30] + [100 for _ in range(V + RETURNS)],
    F=[5 for _ in range(V)],
    demands=[],
    Q=[2]
)



CUSTOMERS2 = 3
cij2 = np.array([
# 0   1   2   3   4   5   6   7   8   9
[99,  1,  1,  1,  1,  1,  1,  1,  1,  1],  # 0 depot v0
[ 1, 99,  1,  1,  1,  1,  1,  1,  1,  1],  # 1 depot v1
[ 1,  1, 99,  1,  1,  1,  1,  1,  1,  1],  # 2 customer 0
[ 1,  1,  1, 99,  1,  1,  1,  1,  1,  1],  # 3 customer 1
[ 1,  1,  1,  1, 99,  1,  1,  1,  1,  1],  # 4 customer 2
[ 1,  1,  1,  1,  1, 99,  1,  1,  1,  1],  # 5 customer 3
[ 1,  1,  1,  1,  1,  1, 99,  1,  1,  1],  # 6 customer 4
[ 1,  1,  1,  1,  1,  1,  1, 99,  1,  1],  # 7 customer 5
[ 1,  1,  1,  1,  1,  1,  1,  1, 99,  1],  # 8 return v0
[ 1,  1,  1,  1,  1,  1,  1,  1,  1, 99],  # 9 return v1
])

tij2 = np.array([
# 0   1   2   3   4   5   6   7   8   
[99,  5,  5,  5,  5,  5,  5,  5,  5],  
[ 5, 99,  5,  5,  5,  5,  5,  5,  5],  
[ 5,  5, 99,  5,  5,  5,  5,  5,  5],  
[ 5,  5,  5, 99,  5,  5,  5,  5,  5],  
[ 5,  5,  5,  5, 99,  5,  5,  5,  5],  
[ 5,  5,  5,  5,  5, 99,  5,  5,  5],  
[ 5,  5,  5,  5,  5,  5, 99,  5,  5],  
[ 5,  5,  5,  5,  5,  5,  5, 99,  5],  
[ 5,  5,  5,  5,  5,  5,  5,  5, 99],
])

feasible_cause_capacity2 = ProblemInstance(
    name="Feasible cause there's more capacity than demand (more vehicles)",
    V=2,
    CUSTOMERS=CUSTOMERS2,
    cost_matrix=cij2,
    tij=tij2,
    ei=[0, 0, 5] + [0 for _ in range(5)],
    li=[5, 5, 11] + [100 for _ in range(5)],
    F=[5 for _ in range(2)],
    demands=[],
    Q=[1, 2]
)