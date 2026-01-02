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



# DIM = V * depot + customers + V * return = 1 + 3 + 1 = 5
# tij = np.array([
#     [99,  5,  5,  5,  5],
#     [ 5, 99,  5,  5,  5],
#     [ 5,  5, 99,  5,  5],
#     [ 5,  5,  5, 99,  5],
#     [ 5,  5,  5,  5, 99],
# ])

# cij = np.array([
#     [99,  1,  1,  1,  1],
#     [ 1, 99,  1,  1,  1],
#     [ 1,  1, 99,  1,  1],
#     [ 1,  1,  1, 99,  1],
#     [ 1,  1,  1,  1, 99],
# ])


# loss_one_client = ProblemInstance(
#     name="loss_one_client",
#     V=1,
#     CUSTOMERS=3,
#     cost_matrix=cij,
#     tij=tij,
#     ei=[0, 10, 10, 0, 0],
#     li=[5, 15, 12, 100, 100],
#     F=[5 for _ in range(1)],
#     demands=[],
#     Q=[]
# )
##################################
##################################
# V = 2
# cij = np.array([
# # 0   1   2   3   4   5   6   7   8   9
# [99,  1,  1,  1,  1,  1,  1,  1,  1,  1],  # 0 depot v0
# [ 1, 99,  1,  1,  1,  1,  1,  1,  1,  1],  # 1 depot v1
# [ 1,  1, 99,  1,  1,  1,  1,  1,  1,  1],  # 2 customer 0
# [ 1,  1,  1, 99,  1,  1,  1,  1,  1,  1],  # 3 customer 1
# [ 1,  1,  1,  1, 99,  1,  1,  1,  1,  1],  # 4 customer 2
# [ 1,  1,  1,  1,  1, 99,  1,  1,  1,  1],  # 5 customer 3
# [ 1,  1,  1,  1,  1,  1, 99,  1,  1,  1],  # 6 customer 4
# [ 1,  1,  1,  1,  1,  1,  1, 99,  1,  1],  # 7 customer 5
# [ 1,  1,  1,  1,  1,  1,  1,  1, 99,  1],  # 8 return v0
# [ 1,  1,  1,  1,  1,  1,  1,  1,  1, 99],  # 9 return v1
# ])

# tij = np.array([
# # 0   1   2   3   4   5   6   7   8   9
# [99,  5,  5,  5,  5,  5,  5,  5,  5,  5],  # 0 depot v0
# [ 5, 99,  5,  5,  5,  5,  5,  5,  5,  5],  # 1 depot v1
# [ 5,  5, 99,  5,  5,  5,  5,  5,  5,  5],  # 2 customer 0
# [ 5,  5,  5, 99,  5,  5,  5,  5,  5,  5],  # 3 customer 1
# [ 5,  5,  5,  5, 99,  5,  5,  5,  5,  5],  # 4 customer 2
# [ 5,  5,  5,  5,  5, 99,  5,  5,  5,  5],  # 5 customer 3
# [ 5,  5,  5,  5,  5,  5, 99,  5,  5,  5],  # 6 customer 4
# [ 5,  5,  5,  5,  5,  5,  5, 99,  5,  5],  # 7 customer 5
# [ 5,  5,  5,  5,  5,  5,  5,  5, 99,  5],  # 8 return v0
# [ 5,  5,  5,  5,  5,  5,  5,  5,  5, 99],  # 9 return v1
# ])

# all_in_time = ProblemInstance(
#     name="all_in_time",
#     V=V,
#     CUSTOMERS=6,
#     cost_matrix=cij,
#     tij=tij,
#     ei=[0, 0, 5, 5, 9, 15, 0, 0, 0, 0], #+ [0 for _ in range(V)],
#     li=[5, 5, 11, 12, 20, 30, 100, 100,100,100], #+ [100 for _ in range(V)],
#     F=[5 for _ in range(V)],
#     demands=[],
#     Q=[]
# )