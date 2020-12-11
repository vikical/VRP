import numpy as np
import random

from src.models.node_distances import NodeDistances
from src.models.solution import Solution


class SolutionCostCalculator(object):
    """
    Compute the cost of a solution. 
    """
    def __init__(self,solution:Solution):
        self.solution=solution


    def calculate_cost_old(self,node_distances:NodeDistances)->int:
        """
        Calculate the cost of the solution as the sum of all the journeys between nodes.
        """
        vehicle_routes=self.solution.get_vehicle_routes_as_matrix()
        all_performed_journeys=np.sum(a=vehicle_routes,axis=0)


        all_travelled_distances=node_distances.distances*all_performed_journeys
        return np.sum(a=all_travelled_distances)

    def calculate_cost(self,node_distances:NodeDistances)->int:
        """
        It returns a 3d matrix, where we store vehicles in X (index i).
        Y (index j) x Z (index k) means that the vehicle travels from node j to k.
        """
        total_distance=0
        num_vehicles=self.solution.vehicle_routes.shape[0]

        for vehicle in range(0,num_vehicles):
            vehicle_distance=0
            previous_node=0
            for node in self.solution.vehicle_routes[vehicle]:
                vehicle_distance=vehicle_distance+node_distances.distances[previous_node][node]
                previous_node=node            
            total_distance=total_distance+vehicle_distance
        
        return total_distance

