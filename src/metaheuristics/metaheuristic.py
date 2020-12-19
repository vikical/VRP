from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.neighborhoods.neighborhood import Neighborhood
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class Metaheuristic(object):
    """
    Perform a local search.
    """
    GREEDY_SEARCH="greedy"
    ANXIOUS_SEARCH="anxious"

    def __init__(self,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int):        
        """
        Init the search. When solution is None, then a initialization is performed.        
        """
        self.search_type=search_type
        self.num_iteration_per_search=num_iteration_per_search
        self.solution_restrictions_calculator=solution_restrictions_calculator
        
        self.solution=solution
        if solution is None:
            initializer=SolutionInitializer(node_distances=solution_restrictions_calculator.node_distances, \
                vehicle_allowed_distances=solution_restrictions_calculator.vehicle_allowed_distances)
            self.solution=initializer.init_vehicles_with_nodes_sequentially()

    
    def run(self)->Solution:
        raise NotImplementedError



