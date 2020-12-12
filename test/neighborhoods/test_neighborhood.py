import pytest
import numpy as np
import random

from src.neighborhoods.neighborhood import Neighborhood

def test_move_depot_to_the_end_when_it_is_in_4th_position():
    route=np.array([1, 2, 3, 0, 4, 5, 0, 0])

    result=Neighborhood(solution=None)._move_depot_to_the_end(route=route)
    

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

    result=Neighborhood(solution=None)._move_depot_to_the_end(route=route)
    

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

    result=Neighborhood(solution=None)._move_depot_to_the_end(route=route)
    

    assert result[0]==1 , "1st element should be 1"
    assert result[1]==2 , "2nd element should be 2"
    assert result[2]==3 , "3rd element should be 3"
    assert result[3]==4 , "4th element should be 4"
    assert result[4]==5 , "5th element should be 5"
    assert result[5]==0 , "6th element should be 0"
    assert result[6]==0 , "7th element should be 0"
    assert result[7]==0 , "8th element should be 0"    