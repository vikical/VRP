import pytest
import numpy as np
import random

from src.neighborhoods.reverse_order import ReverseOrder

def test_reverse_nodes_from_5_to_2():
    route=np.array([0, 1, 2, 3, 4, 5, 6, 7])

    result=ReverseOrder(solution_restrictions_calculator=None).reverse_from_node1_to_node2(route=route,index_node1=5, index_node2=2)
    

    assert result[0]==0 , "1st element should be 0"
    assert result[1]==1 , "2nd element should be 1"
    assert result[2]==5 , "3rd element should be 5"
    assert result[3]==4 , "4th element should be 4"
    assert result[4]==3 , "5th element should be 3"
    assert result[5]==2 , "6th element should be 2"
    assert result[6]==6 , "7th element should be 6"
    assert result[7]==7 , "8th element should be 7"