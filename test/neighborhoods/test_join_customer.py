import pytest
import numpy as np
import random

from src.neighborhoods.join_customers import JoinCustomers
from src.models.solution import Solution
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

def test_join_customers_from_one_route_to_another():
    vehicle_routes=np.array([[1, 2, 3, 4, 5, 0, 0, 0], [11, 12, 13, 14, 15, 0, 0, 0]])
    vehicle_allowed_distances=VehicleAllowedDistances(distances=np.array([300,200]))

    solution=Solution(vehicle_routes=vehicle_routes)
    solution_restrictions_calculator=SolutionRestrictionsCalculator(node_distances=None,vehicle_allowed_distances=vehicle_allowed_distances)
    
    join_customer=JoinCustomers(solution_restrictions_calculator=solution_restrictions_calculator)
    new_solution=join_customer._operation_between_vehicle_routes(solution=solution,vehicle1=0, vehicle2=1)

    route1=new_solution.vehicle_routes[0]
    route2=new_solution.vehicle_routes[1]

    assert route1[0]==1 , "r1: 1st element should be 1"
    assert route1[1]==2 , "r1: 2nd element should be 2"
    assert route1[2]==3 , "r1: 3rd element should be 3"
    assert route1[3]==4 , "r1: 4th element should be 4"
    assert route1[4]==5 , "r1: 5th element should be 5"
    assert route1[5]==11 , "r1: 6th element should be 11"
    assert route1[6]==12 , "r1: 7th element should be 12"
    assert route1[7]==13 , "r1: 8th element should be 13"

    assert route2[0]==0 , "r2: 1st element should be 0"
    assert route2[1]==0 , "r2: 2nd element should be 0"
    assert route2[2]==0 , "r2: 3rd element should be 0"
    assert route2[3]==14 , "r2: 4th element should be 14"
    assert route2[4]==15 , "r2: 5th element should be 15"
    assert route2[5]==0 , "r2: 6th element should be 0"
    assert route2[6]==0 , "r2: 7th element should be 0"
    assert route2[7]==0 , "r2: 8th element should be 0"