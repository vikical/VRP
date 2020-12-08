import pytest
import numpy as np

from src.data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator

def test_get_minimum_allowed_distance_returns_max_of_go_and_return_path():
    distances=np.ndarray(shape=(3,3), dtype="int", buffer=np.array([[0, 1, 3], [4, 0, 1], [4,1,0]]))
    minimun_allowed=VehicleRestrictionsGenerator.get_minimun_allowed_distance(distances_between_nodes=distances)
    assert 7==minimun_allowed, "The max of go-and-return paths is 7"


def test_maximum_allowed_distance_returns_longer_distance_times_number_nodes():
    distances=np.ndarray(shape=(3,3), dtype="int", buffer=np.array([[0, 1, 3], [4, 0, 1], [4,1,0]]))
    maximum_allowed=VehicleRestrictionsGenerator.get_maximum_allowed_distance(distances_between_nodes=distances)
    assert 12==maximum_allowed, "The max of distance is 12"

def test_get_distances_return_as_many_vehicles_as_nodes():
    node_distances=np.ndarray(shape=(3,3), dtype="int", buffer=np.array([[0, 1, 3], [4, 0, 1], [4,1,0]]))
    generator= VehicleRestrictionsGenerator(distances_between_nodes=node_distances)
    vehicle_distances=generator.get_allowed_distances()
    assert np.size(node_distances,axis=0)==np.size(vehicle_distances,axis=0), "There should be as many vehicles as nodes"
