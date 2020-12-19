from src.models.solution import Solution
from src.neighborhoods.neighborhood import Neighborhood
import numpy as np
import copy

class SwapCustomers(Neighborhood):
    """
    Pick randomly a route and two customers in it. Swap them.
    """


    def get_neighbor(self,solution:Solution)->Solution:
        #Get vehicle_involved.
        num_vehicles=solution.vehicle_routes.shape[0]
        vehicle_involved=self.get_different_instances(available_instances=num_vehicles,needed_instances=1)[0]

        #Get nodes to be swapped.
        num_nodes=len(np.where(solution.vehicle_routes.shape[1]>0)[0])
        if num_nodes<2:
            return solution
        nodes_involved=self.get_different_instances(available_instances=num_nodes,needed_instances=2)
        index_node1=nodes_involved[0]
        index_node2=nodes_involved[1]

        #Swap the nodes.
        new_solution=copy.deepcopy(solution)
        new_route=self.swap_nodes(route=new_solution.vehicle_routes[vehicle_involved], index_node1=index_node1, index_node2=index_node2)        
        new_route=self._move_depot_to_the_end(route=new_route) #This shouldn't be necessary. We put in it here as a precaution.
        new_solution.vehicle_routes[vehicle_involved]=new_route

        #Verify movements.
        valid=self._check_valid_modifications(new_solution=new_solution,vehicles_involved=[vehicle_involved])
        if valid==False:
            new_solution.is_valid=False

        #Set new cost.
        new_solution.cost=self._update_solution_cost(old_solution=solution,new_solution=new_solution,vehicles_involved=[vehicle_involved])

        return solution

    def swap_nodes(self,route:np.ndarray,index_node1:int, index_node2:int)->np.ndarray:
        if index_node1==index_node2:
            return route
        
        new_route=np.copy(route)
        new_route[index_node1]=route[index_node2]
        new_route[index_node2]=route[index_node1]

        return new_route

