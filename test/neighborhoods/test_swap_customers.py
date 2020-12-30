import pytest
import numpy as np
import random

from src.neighborhoods.swap_customers import SwapCustomers

def test_swap_node_5_and_2():
    route=np.array([0, 1, 2, 3, 4, 5, 6, 7])

    result=SwapCustomers(solution_restrictions_calculator=None)._operation_inside_vehicle_route(route=route,index_node1=5, index_node2=2)
    

    assert result[0]==0 , "1st element should be 0"
    assert result[1]==1 , "2nd element should be 1"
    assert result[2]==5 , "3rd element should be 5"
    assert result[3]==3 , "4th element should be 3"
    assert result[4]==4 , "5th element should be 4"
    assert result[5]==2 , "6th element should be 2"
    assert result[6]==6 , "7th element should be 6"
    assert result[7]==7 , "8th element should be 7"

def test_swap_node_1_and_1():
    route=np.array([0, 1, 2, 3, 4, 5, 6, 7])

    result=SwapCustomers(solution_restrictions_calculator=None)._operation_inside_vehicle_route(route=route,index_node1=1, index_node2=1)
    

    assert result[0]==0 , "1st element should be 0"
    assert result[1]==1 , "2nd element should be 1"
    assert result[2]==2 , "3rd element should be 5"
    assert result[3]==3 , "4th element should be 3"
    assert result[4]==4 , "5th element should be 4"
    assert result[5]==5 , "6th element should be 2"
    assert result[6]==6 , "7th element should be 6"
    assert result[7]==7 , "8th element should be 7"


def test_swap_node_1st_and_last():
    route=np.array([0, 1, 2, 3, 4, 5, 6, 7])

    result=SwapCustomers(solution_restrictions_calculator=None)._operation_inside_vehicle_route(route=route,index_node1=0, index_node2=7)
    

    assert result[0]==7 , "1st element should be 7"
    assert result[1]==1 , "2nd element should be 1"
    assert result[2]==2 , "3rd element should be 5"
    assert result[3]==3 , "4th element should be 3"
    assert result[4]==4 , "5th element should be 4"
    assert result[5]==5 , "6th element should be 2"
    assert result[6]==6 , "7th element should be 6"
    assert result[7]==0 , "8th element should be 0"    