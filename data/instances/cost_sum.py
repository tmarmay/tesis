from models.problem_instance import ProblemInstance

import numpy as np

CUSTOMERS = 4
cij = np.array([
# 0   1   2   3   4   5   6   7   8   9
[99,  7,  5,  5,  12,  5],  
[ 7, 99,  9,  5,  5,  5],  
[ 9,  5, 99,  3,  5,  5],  
[ 5,  5,  3, 99,  5,  5],  
[ 12,  5,  5,  5, 99,  5],  
[ 5,  5,  5,  5,  5, 99],  
])

tij = np.array([
# 0   1   2   3   4   5   6   7   8   
[99,  5,  5,  5,  5,  5],  
[ 5, 99,  5,  5,  5,  5],  
[ 5,  5, 99,  5,  5,  5],  
[ 5,  5,  5, 99,  5,  5],  
[ 5,  5,  5,  5, 99,  5],  
[ 5,  5,  5,  5,  5, 99],  
])

#DIM(ei/li) = customers +  v + returns
V = 1
RETURNS = V
cost_sum = ProblemInstance(
    name="Cost sum check",
    V=1,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[0, 5, 10, 15] + [0 for _ in range(V + RETURNS)],
    li=[5, 10, 15, 20] + [100 for _ in range(V + RETURNS)],
    F=[5 for _ in range(V)],
    demands=[],
    Q=[]
)