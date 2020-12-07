import pytest
import numpy as np

from src.data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator

def test_get_minimum_allowed_distance_returns_max_of_go_and_return_path():
    distances=np.ndarray(shape=(3,3), dtype="int", buffer=np.array([[0, 1, 3], [4, 0, 1], [4,1,0]]))
    minimun_allowed=VehicleRestrictionsGenerator.get_minimun_allowed_distance(distances_between_nodes=distances)
    assert 7==minimun_allowed, "The max of go-and-return paths is 7"