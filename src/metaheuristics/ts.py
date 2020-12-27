import logging
import copy
from collections import deque

from src.models.solution import Solution

from src.metaheuristics.ls import LS

from src.neighborhoods.neighborhood_factory import NeighborhoodFactory
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class TS(LS):
    """
    Performs tabu search
    """

    def __init__(self,neighborhood_name:str,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str, max_running_secs:float, memory_size:int=10):
        super().__init__(neighborhood_name=neighborhood_name, solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type, max_running_secs=max_running_secs)

        self.memory=deque(maxlen=memory_size)
        self.aspiration_parameter=85

        self.best_solution=self.solution


    def run(self)->Solution:
        """        
        Run tabu search with memory. The loops stops when we reach a limit of iterations without improving.
        The limit of iterations is related to num_iterations_per_search. More precisely, it is max(5,num_iterations_per_search/20).
        """
        while True:           
            #Find new solution, which may not improve current solution.
            new_solution=self.search()
            
            self.__update_solution(new_solution=new_solution)
                
            #If we reach the emergency counter, we leave with the best solution.
            if self._emergency_situation_reached()==True:
                break

        self.solution=self.best_solution
        return self.solution

        


    def __update_solution(self, new_solution:Solution):
        """
        Update solution in the class field.
        If memory is set, append the new feature into the memory.
        """
        #Always update current solution and store it in memory.
        self.solution=new_solution
        if self.memory.maxlen>0:
            new_solution_feature=self._get_feature(solution=new_solution)
            self.memory.append(new_solution_feature)
        logging.info("Updated solution. New cost:" + str(new_solution.cost))


        #Update best solution if we are improving it.
        if new_solution.cost<self.best_solution.cost:
            logging.info("BEST solution till the moment!!!")
            self.best_solution=new_solution


    def search(self)->Solution: 
        """
        We look for an IMPROVEMENT in "num_iteration_per_search" solutions. If none is found, we return the best (greedy) or the first (anxious) found,
        although it can worsen the "cost". 
        When We return the old one is some acceptance criteria is met. We only consider VALID solutions.
        """
        starting_solution=copy.deepcopy(self.solution)

        proposed_solution=starting_solution      
        best_no_improving_solution=None
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=starting_solution)
            if self._new_solution_can_be_accepted(old_solution=proposed_solution, new_solution=solution_in_loop):
                if solution_in_loop.cost<proposed_solution.cost:
                    logging.debug("In search loop: new improved cost="+str(solution_in_loop.cost))
                    if self.search_type==self.ANXIOUS_SEARCH:
                        return solution_in_loop
                    proposed_solution=solution_in_loop
                else:
                    if best_no_improving_solution is None or solution_in_loop.cost<best_no_improving_solution.cost:
                        logging.debug("In search loop: we update the best no improving solution")
                        best_no_improving_solution=solution_in_loop

        if proposed_solution!=starting_solution:
            return proposed_solution
        
        if best_no_improving_solution is not None:
            return best_no_improving_solution

        return starting_solution




    def _new_solution_can_be_accepted(self, old_solution:Solution,new_solution:Solution)->bool:
        """
        Check whether we can accept a new solution:
              > is it valid?
              > has it a better cost?
              > has it not been repeated?
        """               
        #If invalid, we reject it.
        if new_solution.is_valid==False:
            return False        

        #The solution is valid and it's not in the memory, we accept it. The cost improvement will be check afterwards.
        new_solution_feature=self._get_feature(new_solution)
        if new_solution_feature not in self.memory:
            return True


        #The solution can be accepted, but it's in memory, we check the aspirations: we won't allow to worsen more than 80%.
        if self._check_aspiration_level(best_solution=new_solution,worst_solution=old_solution)==True:
            logging.debug("Repeated solution... Accepted!")
            return True


        return False

    def _check_aspiration_level(self, best_solution:Solution, worst_solution:Solution)->bool:
        """
        The new solution should be 95% less than the old one to be accepted without restrictions.
        """
        logging.debug("Check aspiration level, best.cost="+str(best_solution.cost)+" worst.cost="+str(worst_solution.cost)+". Improvement:"+str(100*best_solution.cost/worst_solution.cost))
        if 100*best_solution.cost/worst_solution.cost < self.aspiration_parameter:
            return True

        return False

    def _get_feature(self,solution:Solution)->str:
        """
        Transforms all routes in string. We don't change the order because it does matter since vehicles has lenght restrinctions.
        Afterwards we concatenate the result.
        """
        vehicle_routes_strings=[]
        for vehicle_route in solution.vehicle_routes:
            vehicle_routes_strings.append(solution.route_to_string(vehicle_route))

        return " ".join(vehicle_routes_strings)



