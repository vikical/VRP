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


    def calculate_cost(self,node_distances:NodeDistances)->int:
        """
        Calculate the cost of the solution as the sum of all the journeys between nodes.
        """
        vehicle_routes=self.solution.vehicle_routes
        all_performed_journeys=np.sum(a=vehicle_routes,axis=0)


        all_travelled_distances=node_distances.distances*all_performed_journeys
        return np.sum(a=all_travelled_distances)