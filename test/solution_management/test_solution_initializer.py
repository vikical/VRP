import pytest
import numpy as np
import random

from src.solution_management.solution_initializer import SolutionInitializer
from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

@pytest.fixture
def init_random_seed():
    random.seed(a=1)
    

def test_init_randomly_all_customes_are_visited(init_random_seed):
    init_random_seed
    node_distances=NodeDistances(distances=np.array([[0, 1, 1, 1],[1, 0, 1,1],[1, 1, 0,1],[1,1,1,0]]))
    vehicle_distances=VehicleAllowedDistances(distances=np.array([2, 2,2]))

    initializer=SolutionInitializer(node_distances=node_distances,vehicle_allowed_distances=vehicle_distances)
    solution=initializer.init_randomly()
    
    vehicle_routes=solution.vehicle_routes
    num_node1=np.where(vehicle_routes==1)[0]
    num_node2=np.where(vehicle_routes==2)[0]
    num_node3=np.where(vehicle_routes==3)[0]

    assert len(num_node1)==1, "Node 1 should be only once"
    assert len(num_node2)==1, "Node 2 should be only once"
    assert len(num_node3)==1, "Node 3 should be only once"
    

def test_init_group_sequentially_all_customes_are_visited(init_random_seed):
    init_random_seed
    node_distances=NodeDistances(distances=np.array([[0, 1, 1, 1],[1, 0, 1,1],[1, 1, 0,1],[1,1,1,0]]))
    vehicle_distances=VehicleAllowedDistances(distances=np.array([2, 2,2]))

    initializer=SolutionInitializer(node_distances=node_distances,vehicle_allowed_distances=vehicle_distances)
    solution=initializer.init_vehicles_with_group_nodes_sequentially()
    
    vehicle_routes=solution.vehicle_routes
    num_node1=np.where(vehicle_routes==1)[0]
    num_node2=np.where(vehicle_routes==2)[0]
    num_node3=np.where(vehicle_routes==3)[0]

    assert len(num_node1)==1, "Node 1 should be only once"
    assert len(num_node2)==1, "Node 2 should be only once"
    assert len(num_node3)==1, "Node 3 should be only once"

def test_init_one2one_all_customes_are_visited(init_random_seed):
    init_random_seed
    node_distances=NodeDistances(distances=np.array([[0, 1, 1, 1],[1, 0, 1,1],[1, 1, 0,1],[1,1,1,0]]))
    vehicle_distances=VehicleAllowedDistances(distances=np.array([2, 2,2]))

    initializer=SolutionInitializer(node_distances=node_distances,vehicle_allowed_distances=vehicle_distances)
    solution=initializer.init_one_node_to_one_vehicle()
    
    vehicle_routes=solution.vehicle_routes
    num_node1=np.where(vehicle_routes==1)[0]
    num_node2=np.where(vehicle_routes==2)[0]
    num_node3=np.where(vehicle_routes==3)[0]

    assert len(num_node1)==1, "Node 1 should be only once"
    assert len(num_node2)==1, "Node 2 should be only once"
    assert len(num_node3)==1, "Node 3 should be only once"