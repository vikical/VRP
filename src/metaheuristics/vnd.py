from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.metaheuristics.bvns import BVNS
from src.metaheuristics.metaheuristic import Metaheuristic
from src.neighborhoods.neighborhood import Neighborhood

from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class VND(BVNS):
    """
    Perform a VND. By definition the internal local search has to be greedy.
    """

    def __init__(self,neighborhood_names:[str],solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                num_iteration_per_search:int, initialization_type:str,max_running_secs:float):
        super().__init__(neighborhood_names=neighborhood_names,solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=Metaheuristic.GREEDY_SEARCH,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type,\
            max_running_secs=max_running_secs)


    def _shake_solution(self,solution: Solution, neighborhood: Neighborhood)->Solution:
        return solution


    def _update_next_neighborhood_index_when_no_improvement(self,current_index:int)->int:
        """
        Return next neighborhood_index when there's no improvmeente
        """
        return current_index+1