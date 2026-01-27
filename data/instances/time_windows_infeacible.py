from models.problem_instance import ProblemInstance

import numpy as np

#DIM = V * depot + customers + V * return = 1 + 3 + 1 = 5
tij = np.array([
    [99,  5,  5,  5,  5],
    [ 5, 99,  5,  5,  5],
    [ 5,  5, 99,  5,  5],
    [ 5,  5,  5, 99,  5],
    [ 5,  5,  5,  5, 99],
])

cij = np.array([
    [99,  1,  1,  1,  1],
    [ 1, 99,  1,  1,  1],
    [ 1,  1, 99,  1,  1],
    [ 1,  1,  1, 99,  1],
    [ 1,  1,  1,  1, 99],
])

CUSTOMERS = 3
infeacible = ProblemInstance(
    name="infeacible",
    V=1,
    CUSTOMERS=CUSTOMERS,
    cost_matrix=cij,
    tij=tij,
    ei=[1, 0, 10, 0, 0] + [0 for _ in range(CUSTOMERS)],
    li=[1, 0, 12, 100, 100] + [100 for _ in range(CUSTOMERS)],
    F=[5 for _ in range(1)],
    demands=[],
    Q=[]
)