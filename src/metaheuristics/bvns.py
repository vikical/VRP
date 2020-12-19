import copy

from src.models.solution import Solution
from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

from src.metaheuristics.metaheuristic import Metaheuristic
from src.metaheuristics.ls import LS

from src.neighborhoods.neighborhood_factory import NeighborhoodFactory


class BVNS(Metaheuristic):
    """
    Perform a local search.
    """

    def __init__(self, neighborhood_names:[str], shaking_intensity:int,solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator, \
                search_type:str, num_iteration_per_search:int):
        super().__init__(solution=solution, solution_restrictions_calculator=solution_restrictions_calculator, \
            search_type=search_type,num_iteration_per_search=num_iteration_per_search)

        self.neighborhood_names=neighborhood_names
        self.shaking_intensity=shaking_intensity


    def run(self)->Solution:
        """        
        Run BVNS
        """    
        for neighborhood_name in self.neighborhood_names:
            #Shake solution.
            new_solution=self.shake_solution(neighborhood_name=neighborhood_name)

            #Local Search
            print("Applying "+neighborhood_name+" ....................")
            ls=LS(solution=new_solution, neighborhood_name=neighborhood_name, solution_restrictions_calculator=self.solution_restrictions_calculator, \
            search_type=self.search_type,num_iteration_per_search=self.num_iteration_per_search)
            
            #Update general solution
            self.solution=ls.run()
            print("Current cost: "+str(self.solution.cost))

        return self.solution


    def shake_solution(self,neighborhood_name:str)->Solution:
        """
        Shake the solution
        """
        new_solution=copy.deepcopy(self.solution)

        #Create neighborhood.
        neighborhood=NeighborhoodFactory.create_neighborhood(neighborhood_name=neighborhood_name, \
            solution_restrictions_calculator= self.solution_restrictions_calculator)

        #Shaking
        for item in range(0,self.shaking_intensity):
            new_solution=neighborhood.get_neighbor(solution=new_solution)

        return new_solution



