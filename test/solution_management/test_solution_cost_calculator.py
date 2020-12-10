import pytest
import numpy as np
import random

from src.solution_management.solution_cost_calculator import SolutionCostCalculator
from src.models.solution import Solution
from src.models.node_distances import NodeDistances


def test_solution_cost_calculator():
    solution=Solution(vehicle_routes=np.array([[[0, 0, 1],[0, 0, 0],[1, 0, 0]],[[0, 1, 0],[1, 0, 0],[0, 0, 0]]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2],[3, 0, 5],[6, 7, 0]]))

    calculator=SolutionCostCalculator(solution=solution)
    cost=calculator.calculate_cost(node_distances=node_distances)

    assert 12==cost , "Depot is visited three times (by each car) and customers once (one per car)"
    

