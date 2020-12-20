from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.metaheuristics.bvns import BVNS
from src.neighborhoods.neighborhood import Neighborhood

from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class VND(BVNS):
    """
    Perform a local search.
    """

    def __init__(self,neighborhood_names:[str],solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str):
        super().__init__(neighborhood_names=neighborhood_names,solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type)


    def _shake_solution(self,solution: Solution, neighborhood: Neighborhood)->Solution:
        return solution


