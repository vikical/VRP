import pytest
import numpy as np
import random

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

def test_calculate_cost_with_two_cars():
    solution=Solution(vehicle_routes=np.array([[2, 0 , 0],[1, 0, 0]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2],[3, 0, 5],[6, 7, 0]]))

    calculator=SolutionRestrictionsCalculator(solution=solution,node_distances=node_distances,vehicle_allowed_distances=None)
    cost=calculator.calculate_cost()

    assert 12==cost , "All the routes should sum 12"

def test_calculate_cost_calculator_with_one_cars():
    solution=Solution(vehicle_routes=np.array([[2, 1 , 0],[0, 0, 0]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2],[3, 0, 5],[6, 7, 0]]))

    calculator=SolutionRestrictionsCalculator(solution=solution,node_distances=node_distances,vehicle_allowed_distances=None)
    cost=calculator.calculate_cost()

    assert 12==cost , "All only one route should sum 12"    
    
def test_get_vehicle_consumed_distance():
    solution=Solution(vehicle_routes=np.array([[2, 1 , 3, 0],[0,0,0,0]]))
    node_distances=NodeDistances(distances=np.array([[0,7,3,1],[2,0,4,6],[3,6,0,9],[5,10,15,0]]))

    calculator=SolutionRestrictionsCalculator(solution=solution,node_distances=node_distances,vehicle_allowed_distances=None)
    cost=calculator.get_vehicle_consumed_distance(vehicle=0)

    assert 20==cost , "All only one route should sum 20"

def test_remaining_distance_for_vehicle_returns_positive():
    solution=Solution(vehicle_routes=np.array([[2, 1 , 0],[0, 0, 0]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2],[3, 0, 5],[6, 7, 0]]))
    vehicle_allowed_distances=VehicleAllowedDistances(distances=[14, 7, 0])

    calculator=SolutionRestrictionsCalculator(solution=solution,node_distances=node_distances,vehicle_allowed_distances=vehicle_allowed_distances)
    remaining_distance=calculator.get_vehicle_remaining_distance(vehicle=0)

    assert 2==remaining_distance , "2 should be the remaining distance"  

def test_remaining_distance_for_vehicle_returns_negative():
    solution=Solution(vehicle_routes=np.array([[2, 1 , 0],[0, 0, 0]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2],[3, 0, 5],[6, 7, 0]]))
    vehicle_allowed_distances=VehicleAllowedDistances(distances=[10, 7, 0])

    calculator=SolutionRestrictionsCalculator(solution=solution,node_distances=node_distances,vehicle_allowed_distances=vehicle_allowed_distances)
    remaining_distance=calculator.get_vehicle_remaining_distance(vehicle=0)

    assert -2==remaining_distance , "-2 should be the remaining distance"  
