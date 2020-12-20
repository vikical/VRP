from src.models.solution import Solution

from src.metaheuristics.tabu import Tabu
from src.neighborhoods.neighborhood_factory import NeighborhoodFactory
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class LS(Tabu):
    """
    Perform a local search.
    """

    def __init__(self,neighborhood_name:str,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, \
                neighborhood_name=neighborhood_name, memory_size=0, initialization_type=initialization_type)


