import pytest
import numpy as np
import random

from src.neighborhoods.neighborhood import Neighborhood
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

def test_move_depot_to_the_end_when_it_is_in_4th_position():
    route=np.array([1, 2, 3, 0, 4, 5, 0, 0])

    result=Neighborhood(solution=None,solution_restrictions_calculator=None)._move_depot_to_the_end(route=route)
    

    assert result[0]==1 , "1st element should be 1"
    assert result[1]==2 , "2nd element should be 2"
    assert result[2]==3 , "3rd element should be 3"
    assert result[3]==4 , "4th element should be 4"
    assert result[4]==5 , "5th element should be 5"
    assert result[5]==0 , "6th element should be 0"
    assert result[6]==0 , "7th element should be 0"
    assert result[7]==0 , "8th element should be 0"

def test_move_depot_to_the_end_when_it_is_in_1st_position():
    route=np.array([0, 1, 2, 3, 4, 5, 0, 0])

    result=Neighborhood(solution=None,solution_restrictions_calculator=None)._move_depot_to_the_end(route=route)
    

    assert result[0]==1 , "1st element should be 1"
    assert result[1]==2 , "2nd element should be 2"
    assert result[2]==3 , "3rd element should be 3"
    assert result[3]==4 , "4th element should be 4"
    assert result[4]==5 , "5th element should be 5"
    assert result[5]==0 , "6th element should be 0"
    assert result[6]==0 , "7th element should be 0"
    assert result[7]==0 , "8th element should be 0"

def test_move_depot_to_the_end_when_it_is_in_last_position():
    route=np.array([1, 2, 3, 4, 5, 0, 0, 0])

    result=Neighborhood(solution=None,solution_restrictions_calculator=None)._move_depot_to_the_end(route=route)
    

    assert result[0]==1 , "1st element should be 1"
    assert result[1]==2 , "2nd element should be 2"
    assert result[2]==3 , "3rd element should be 3"
    assert result[3]==4 , "4th element should be 4"
    assert result[4]==5 , "5th element should be 5"
    assert result[5]==0 , "6th element should be 0"
    assert result[6]==0 , "7th element should be 0"
    assert result[7]==0 , "8th element should be 0"    

def test_update_cost_solution_when_2_routes_change():
    solution1=Solution(vehicle_routes=np.array([[2, 0 , 0, 0],[1,3, 0,0],[0,0,0,0]]))
    solution2=Solution(vehicle_routes=np.array([[2, 0 , 0,0],[1, 0, 0,0],[3,0,0,0]]))
    node_distances=NodeDistances(distances=np.array([[0, 1, 2,20],[3, 0, 5,21],[6, 7, 0,22],[9,1,1,0]]))
    vehicle_allowed_distances=VehicleAllowedDistances(distances=[14, 20, 15])
    calculator=SolutionRestrictionsCalculator(node_distances=node_distances,vehicle_allowed_distances=vehicle_allowed_distances)


    cost=Neighborhood(solution=solution1,solution_restrictions_calculator=calculator). \
        _update_solution_cost(new_solution=solution2,vehicles_involved=[1,2])
    

    assert cost==41 , "Update cost should be 41"
