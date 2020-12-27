import logging
import copy

from src.models.solution import Solution

from src.metaheuristics.metaheuristic import Metaheuristic
from src.neighborhoods.neighborhood_factory import NeighborhoodFactory
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class LS(Metaheuristic):
    """
    Perform a local search.
    """

    def __init__(self,neighborhood_name:str,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str,max_running_secs:float):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type, \
            max_running_secs=max_running_secs)
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
                
            self._update_solution(new_solution=new_solution)
        return self.solution


    def _update_solution(self, new_solution:Solution):
        """
        Update solution in the class field.
        If memory is set, append the new feature into the memory.
        """
        self.solution=new_solution
        logging.debug("Updated solution. New cost:" + str(new_solution.cost))

    def search(self)->Solution:
        """
        Look for a solution in the environment of the current solution. It uses greedy or anxious search depending on the paramerters ingested during the instantiation.
        By default, greedy search is performed.
        Only VALID solutions are returned.
        """
        starting_solution=copy.deepcopy(self.solution)

        proposed_solution=starting_solution        
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=starting_solution)
            if self._new_solution_can_be_accepted(old_solution=proposed_solution, new_solution=solution_in_loop):
                if self.search_type==self.ANXIOUS_SEARCH:
                    return solution_in_loop
                proposed_solution=solution_in_loop #GREEDY_SEARCH.
            
            #If we reach the emergency counter, we leave with the best solution.
            if self._emergency_situation_reached()==True:
                break

        return proposed_solution



    def _new_solution_can_be_accepted(self, old_solution:Solution,new_solution:Solution)->bool:
        """
        Check whether we can accept a new solution:
              > is it valid?
              > has it a better cost?
        """       
        if new_solution.is_valid==True and new_solution.cost<old_solution.cost:
            return True

        return False


