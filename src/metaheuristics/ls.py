from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.metaheuristics.metaheuristic import Metaheuristic
from src.neighborhoods.neighborhood_factory import NeighborhoodFactory
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class LS(Metaheuristic):
    """
    Perform a local search.
    """

    def __init__(self,neighborhood_name:str,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search)
        self.neighborhood=NeighborhoodFactory.create_neighborhood(neighborhood_name=neighborhood_name, \
            solution_restrictions_calculator=self.solution_restrictions_calculator)



    def run(self)->Solution:
        """        
        Run local search
        """
        while True:
            old_cost=self.solution.cost

            new_solution=self.search()
            if old_cost<=new_solution.cost:
                return self.solution
                
            self.solution=new_solution


        return self.solution


    def search(self)->Solution:
        """
        Look for a solution in the environment of the current solution. It uses greedy or anxious search depending on the paramerters ingested during the instantiation.
        By default, anxious search is performed.
        Only VALID solutions are returned.
        """
        if self.search_type==self.GREEDY_SEARCH:
            return self.__greedy_search()

        return self.__anxious_search()


    def __greedy_search(self)->Solution: 
        """
        We look for an improvement in "num_iteration_per_search" solutions. If none is found, we return the old one.
        We only consider VALID solutions.
        """
        new_solution=self.solution      
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=self.solution)
            if solution_in_loop.is_valid==True and solution_in_loop.cost< new_solution.cost:
                new_solution=solution_in_loop
            
        return new_solution


    def __anxious_search(self):
        """
        We return the first improvement we find. If after "num_iteration_per_search", we don't improve, then, we return the old solution.
        We only consider VALID solutions.
        """
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=self.solution)
            if solution_in_loop.is_valid==True and solution_in_loop.cost< self.solution.cost:
                return solution_in_loop
            
        return self.solution