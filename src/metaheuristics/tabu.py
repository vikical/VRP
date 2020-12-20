from collections import deque

from src.models.solution import Solution

from src.metaheuristics.metaheuristic import Metaheuristic

from src.neighborhoods.neighborhood_factory import NeighborhoodFactory
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class Tabu(Metaheuristic):
    """
    Performs tabu search
    """

    def __init__(self,neighborhood_name:str,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int, initialization_type:str, memory_size:int=10):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search, initialization_type=initialization_type)

        self.neighborhood=NeighborhoodFactory.create_neighborhood(neighborhood_name=neighborhood_name, \
            solution_restrictions_calculator=self.solution_restrictions_calculator)
        self.memory=deque(maxlen=memory_size)


    def run(self)->Solution:
        """        
        Run local search with memory
        """
        while True:
            old_cost=self.solution.cost

            new_solution=self.search()
            if old_cost<=new_solution.cost:
                return self.solution
                
            self.__update_solution(new_solution=new_solution)


        return self.solution


    def __update_solution(self, new_solution:Solution):
        """
        Update solution in the class field.
        If memory is set, append the new feature into the memory.
        """
        self.solution=new_solution

        if self.memory.maxlen>0:
            new_solution_feature=self._get_feature(solution=new_solution)
            self.memory.append(new_solution_feature)

        print("Updated solution. New cost:", str(new_solution.cost))

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
        proposed_solution=self.solution      
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=self.solution)
            if self._new_solution_can_be_accepted(old_solution=proposed_solution, new_solution=solution_in_loop):
                proposed_solution=solution_in_loop
            
        return proposed_solution


    def __anxious_search(self):
        """
        We return the first improvement we find. If after "num_iteration_per_search", we don't improve, then, we return the old solution.
        We only consider VALID s"""  """olutions.
        """
        for index in range(0,self.num_iteration_per_search):
            solution_in_loop=self.neighborhood.get_neighbor(solution=self.solution)
            if self._new_solution_can_be_accepted(old_solution=self.solution,new_solution=solution_in_loop):
                return solution_in_loop
            
        return self.solution


    def _new_solution_can_be_accepted(self, old_solution:Solution,new_solution:Solution)->bool:
        """
        Check whether we can accept a new solution:
              > is it valid?
              > has it a better cost?
              > has it not been repeated?
        """       
        if self.memory.maxlen>0:
            new_solution_feature=self._get_feature(new_solution)
            if new_solution_feature in self.memory:
                return False

        if new_solution.is_valid==True and new_solution.cost< old_solution.cost:
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



