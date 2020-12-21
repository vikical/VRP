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

    RANDOM_INIT="random"
    ONE2ONE_INIT="one2one"
    GROUP_SEQUENTIAL_INIT="group"

    def __init__(self,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str):        
        """
        Init the search. When solution is None, then a initialization is performed.        
        """
        self.search_type=search_type
        self.num_iteration_per_search=num_iteration_per_search
        self.solution_restrictions_calculator=solution_restrictions_calculator
        self.initializer=SolutionInitializer(node_distances=solution_restrictions_calculator.node_distances, \
                vehicle_allowed_distances=solution_restrictions_calculator.vehicle_allowed_distances)       
        self.initialization_type=initialization_type

        self.solution=solution
        if solution is None:            
            self.solution=self.init_solution()

    
    def run(self)->Solution:
        raise NotImplementedError

    def init_solution(self)->Solution:
        if self.initialization_type==Metaheuristic.ONE2ONE_INIT:
            return self.initializer.init_one_node_to_one_vehicle()

        if self.initialization_type==Metaheuristic.RANDOM_INIT:
            return self.initializer.init_randomly()

        if self.initialization_type==Metaheuristic.GROUP_SEQUENTIAL_INIT:
            return self.initializer.init_vehicles_with_group_nodes_sequentially()

        return self.initializer.init_randomly()
        



