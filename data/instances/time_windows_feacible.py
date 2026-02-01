from models.problem_instance import ProblemInstance

import numpy as np

CUSTOMERS = 3
cij = np.array([
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

tij = np.array([
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

#DIM(ei/li) = customers + returns
feacible = ProblemInstance(
    name="feacible",
    V=2,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[0, 0, 5] + [0 for _ in range(4)],
    li=[5, 5, 11] + [100 for _ in range(4)],
    F=[5 for _ in range(2)],
    demands=[],
    Q=[CUSTOMERS for _ in range(2)]
)