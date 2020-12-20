import copy

from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

from src.metaheuristics.metaheuristic import Metaheuristic
from src.metaheuristics.ls import LS

from src.neighborhoods.neighborhood import Neighborhood
from src.neighborhoods.neighborhood_factory import NeighborhoodFactory


class BVNS(Metaheuristic):
    """
    Perform a local search.
    """

    def __init__(self, neighborhood_names:[str], solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type)

        self.neighborhood_names=neighborhood_names


    def run(self)->Solution:
        """        
        Run BVNS
        """    
        for neighborhood_name in self.neighborhood_names:
            self.solution=self.exploration_in_neighborhood(neighborhood_name=neighborhood_name)

        return self.solution

    def exploration_in_neighborhood(self, neighborhood_name)->Solution:
        print("************* APPLYING "+neighborhood_name+" *************")
        neighborhood=NeighborhoodFactory.create_neighborhood(neighborhood_name=neighborhood_name, \
            solution_restrictions_calculator= self.solution_restrictions_calculator)

        proposed_solution=copy.deepcopy(self.solution)
        while True:
            #Shake solution.
            print("SHAKE in "+neighborhood_name)
            new_solution=self._shake_solution(neighborhood=neighborhood,solution=proposed_solution)

            #Local Search
            ls=LS(solution=new_solution, neighborhood_name=neighborhood_name, solution_restrictions_calculator=self.solution_restrictions_calculator, \
            search_type=self.search_type,num_iteration_per_search=self.num_iteration_per_search, initialization_type=self.initialization_type)
            new_solution=ls.run()                        

            #Compare with previous proposed solution. If we don't improve anymore, we leave.
            print("Proposed cost in "+neighborhood_name+ ": "+str(new_solution.cost))
            if new_solution.cost>=proposed_solution.cost:
                print("*************LOCAL MINIMUN FOUND")
                return proposed_solution
            proposed_solution=new_solution


    def _shake_solution(self,solution: Solution, neighborhood: Neighborhood)->Solution:
        """
        Shake the solution
        """
        return neighborhood.get_neighbor(solution=solution)
    



