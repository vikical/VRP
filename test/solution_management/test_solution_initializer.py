import pytest
import numpy as np
import random

from src.solution_management.solution_initializer import SolutionInitializer
from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

@pytest.fixture
def init_random_seed():
    random.seed(a=0)
    

def test_init_randomly_all_customes_are_visited_and_depot_visited_2(init_random_seed):
    init_random_seed
    node_distances=NodeDistances(distances=np.array([[0, 1, 1, 1],[1, 0, 1,1],[1, 1, 0,1],[1,1,1,0]]))
    vehicle_distances=VehicleAllowedDistances(distances=np.array([1, 1,1]))

    initializer=SolutionInitializer(node_distances=node_distances,vehicles_allowed_distances=vehicle_distances)
    solution=initializer.init_randomly()

    go_and_back_trips=np.sum(a=solution.vehicle_routes,axis=0)
    nodes_visited=np.sum(a=go_and_back_trips,axis=1)

    assert (nodes_visited[0]==3 and nodes_visited[1]==1 and nodes_visited[2]==1 and nodes_visited[3]==1) , "Depot is visited three times (by each car) and customers once (one per car)"
    

