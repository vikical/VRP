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

import logging

class BVNS(Metaheuristic):
    """
    Perform a local search.
    """

    def __init__(self, neighborhood_names:[str], solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str,max_running_secs:float):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type, \
            max_running_secs=max_running_secs)

        self.neighborhood_names=neighborhood_names
        self.neighborhood_len=len(self.neighborhood_names)

    def run(self)->Solution:
        """        
        Run BVNS
        """    
        neighborhood_index=0

        while not self._emergency_situation_reached() and neighborhood_index<self.neighborhood_len:
            neighborhood_name=self.neighborhood_names[neighborhood_index]
            proposed_solution=self.exploration_in_neighborhood(neighborhood_name=neighborhood_name)

            #Update solution and index.
            if self.solution.cost>proposed_solution.cost:
                self.solution=proposed_solution
                neighborhood_index=0
            else:
                neighborhood_index=self._update_next_neighborhood_index_when_no_improvement(current_index=neighborhood_index)
           

        return self.solution

    def _update_next_neighborhood_index_when_no_improvement(self,current_index:int)->int:
        """
        Return next neighborhood_index when there's no improvmeente
        """
        return (current_index+1) % self.neighborhood_len


    def exploration_in_neighborhood(self, neighborhood_name)->Solution:
        logging.info("************* APPLYING "+neighborhood_name+" *************")
        neighborhood=NeighborhoodFactory.create_neighborhood(neighborhood_name=neighborhood_name, \
            solution_restrictions_calculator= self.solution_restrictions_calculator)

        proposed_solution=copy.deepcopy(self.solution)
        while True:
            #Shake solution.
            new_solution=self._shake_solution(neighborhood=neighborhood,solution=proposed_solution)

            #Local Search
            ls=LS(solution=new_solution, neighborhood_name=neighborhood_name, solution_restrictions_calculator=self.solution_restrictions_calculator, \
            search_type=self.search_type,num_iteration_per_search=self.num_iteration_per_search, initialization_type=self.initialization_type, \
            max_running_secs=self.max_running_secs)
            new_solution=ls.run()                        

            #Compare with previous proposed solution. If we don't improve anymore, we leave.
            logging.info("Proposed cost in "+neighborhood_name+ ": "+str(new_solution.cost))
            if new_solution.cost>=proposed_solution.cost:
                logging.info("LOCAL MINIMUN FOUND!")
                return proposed_solution
            proposed_solution=new_solution


    def _shake_solution(self,solution: Solution, neighborhood: Neighborhood)->Solution:
        """
        Shake the solution. We only return a VALID solution.
        """
        proposed_solution=solution
        for index in range(0,10):
            solution_in_loop=neighborhood.get_neighbor(solution=solution)
            if solution_in_loop.is_valid:
                proposed_solution=solution_in_loop
                break

        logging.info("SHAKED cost:"+str(proposed_solution.cost))
        return proposed_solution
    



