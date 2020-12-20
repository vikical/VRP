from src.models.solution import Solution
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.neighborhoods.neighborhood import Neighborhood

import numpy as np
import random
import copy

class OneCustomerNeighborhood(Neighborhood):
    """
    Abstract class for neighborhoods where the solution evolves to the optimal solution, or at least to a local minimum.
    """
    def __init__(self, solution_restrictions_calculator:SolutionRestrictionsCalculator):
        super().__init__(solution_restrictions_calculator=solution_restrictions_calculator)

    
    def get_neighbor(self,solution:Solution)->Solution:
        #Vehicles with non-empty routes.
        non_empty_vehicle_routes=self.solution_restrictions_calculator.get_not_empty_vehicle_routes(solution=solution)

        #Get vehicle_involved.
        non_empty_route_index=self.get_different_instances(available_instances=len(non_empty_vehicle_routes),needed_instances=1)[0]
        vehicle_involved=non_empty_vehicle_routes[non_empty_route_index]

        #Get nodes involved.
        num_nodes=len(np.where(solution.vehicle_routes[vehicle_involved]>0)[0])
        if num_nodes<2:
            return solution
        nodes_involved=self.get_different_instances(available_instances=num_nodes,needed_instances=2)
        index_node1=nodes_involved[0]
        index_node2=nodes_involved[1]

        #Reverse route and update it.
        new_solution=copy.deepcopy(solution)
        new_route=self._operation_inside_vehicle_route(route=new_solution.vehicle_routes[vehicle_involved],index_node1=index_node1, index_node2=index_node2)
        new_solution.vehicle_routes[vehicle_involved]=self._move_depot_to_the_end(route=new_route) #This shouldn't be necessary. We put in here as a precaution.

        #Verify movements.
        valid=self._check_valid_modifications(new_solution=new_solution,vehicles_involved=[vehicle_involved])
        if valid==False:
            new_solution.is_valid=False

        #Set new cost.
        new_solution.cost=self._update_solution_cost(old_solution=solution,new_solution=new_solution,vehicles_involved=[vehicle_involved])
        #print("proposed solution.cost="+str(new_solution.cost))

        return new_solution


    def _operation_inside_vehicle_route(self,route:np.ndarray,index_node1:int, index_node2:int)->np.ndarray:
        raise NotImplementedError