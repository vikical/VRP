import numpy as np
import random

from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances
from src.models.solution import Solution

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class SolutionInitializer(object):
    """
    Initializes a solution. 
    """
    def __init__(self,node_distances:NodeDistances, vehicle_allowed_distances:VehicleAllowedDistances):
        self.node_distances=node_distances
        self.vehicle_allowed_distances=vehicle_allowed_distances


    def init_randomly(self)->Solution:
        """
        For each customer we randomly select a vehicle. If the fleet contains vehicles which cannot performe a certain
        trip, it may lead to unfeasible solutions. We allow this since we are in the initial solution.
        """
        num_vehicles=self.vehicle_allowed_distances.get_number_of_vehicles()
        num_nodes=self.node_distances.get_number_of_nodes()
        vehicle_routes=np.zeros([num_vehicles,num_nodes],dtype=int)

        for node in range(1,num_nodes):
            vehicle=random.randint(0,num_vehicles-1)
            route=vehicle_routes[vehicle]
            available_indexes=np.where(route==0)[0]
            index=available_indexes[0]
            vehicle_routes[vehicle][index]=node 

        solution=Solution(vehicle_routes=vehicle_routes)
        return solution
        

