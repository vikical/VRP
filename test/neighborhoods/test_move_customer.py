import pytest
import numpy as np
import random

from src.neighborhoods.move_customer import MoveCustomer
from src.models.solution import Solution

def test_move_customer_from_one_route_to_another():
    vehicle_routes=np.array([[1, 2, 3, 4, 5, 0, 0, 0], [11, 12, 13, 14, 15, 0, 0, 0]])
    solution=Solution(vehicle_routes=vehicle_routes)
    move_customer=MoveCustomer(solution=solution,solution_restrictions_calculator=None)
    new_solution=move_customer.move_nodes(vehicle1=0, vehicle2=1, node_index_in1=3,node_index_in2=0)

    route1=new_solution.vehicle_routes[0]
    route2=new_solution.vehicle_routes[1]

    assert route1[0]==1 , "r1: 1st element should be 1"
    assert route1[1]==2 , "r1: 2nd element should be 2"
    assert route1[2]==3 , "r1: 3rd element should be 3"
    assert route1[3]==11 , "r1: 4th element should be 4"
    assert route1[4]==5 , "r1: 5th element should be 5"
    assert route1[5]==0 , "r1: 6th element should be 0"
    assert route1[6]==0 , "r1: 7th element should be 0"
    assert route1[7]==0 , "r1: 8th element should be 0"

    assert route2[0]==4 , "r2: 1st element should be 4"
    assert route2[1]==12 , "r2: 2nd element should be 12"
    assert route2[2]==13 , "r2: 3rd element should be 13"
    assert route2[3]==14 , "r2: 4th element should be 14"
    assert route2[4]==15 , "r2: 5th element should be 15"
    assert route2[5]==0 , "r2: 6th element should be 0"
    assert route2[6]==0 , "r2: 7th element should be 0"
    assert route2[7]==0 , "r2: 8th element should be 0"