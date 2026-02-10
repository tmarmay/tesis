from models.solutions import Solution
import numpy as np 

class BaseSolver:
    def get_solver_name(self) -> str:
        raise NotImplementedError
    
    def is_stochastic(self) -> bool:
        raise NotImplementedError
    
    def solve(self, instance) -> Solution:
        raise NotImplementedError
