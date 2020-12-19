from src.models.solution import Solution
from src.neighborhoods.neighborhood import Neighborhood
import numpy as np
import copy

class ReverseOrder(Neighborhood):
    """
    Pick randomly a route and two customers in it. Reverse the order between the customers between those customers.
    """


    def get_neighbor(self,solution:Solution)->Solution:
        #Get vehicle_involved.
        num_vehicles=solution.vehicle_routes.shape[0]
        vehicle_involved=self.get_different_instances(available_instances=num_vehicles,needed_instances=1)[0]

        #Get nodes to be reversed.
        num_nodes=len(np.where(solution.vehicle_routes.shape[1]>0)[0])
        if num_nodes<2:
            return solution
        nodes_involved=self.get_different_instances(available_instances=num_nodes,needed_instances=2)
        index_node1=nodes_involved[0]
        index_node2=nodes_involved[1]

        #Reverse route and update it.
        new_solution=copy.deepcopy(solution)
        new_route=self.reverse_from_node1_to_node2(route=new_solution.vehicle_routes[vehicle_involved],index_node1=index_node1, index_node2=index_node2)
        new_solution.vehicle_routes[vehicle_involved]=self._move_depot_to_the_end(route=new_route) #This shouldn't be necessary. We put in here as a precaution.

        #Verify movements.
        valid=self._check_valid_modifications(new_solution=new_solution,vehicles_involved=[vehicle_involved])
        if valid==False:
            new_solution.is_valid=False

        #Set new cost.
        new_solution.cost=self._update_solution_cost(old_solution=solution,new_solution=new_solution,vehicles_involved=[vehicle_involved])

        return new_solution

    def reverse_from_node1_to_node2(self,route:np.ndarray, index_node1:int, index_node2:int)->np.ndarray:
        """
        Reverse a route from node i to j (both inclusive).
        """
        #If nodes are the same, we return.
        if index_node1==index_node2:
            return route

        #Set beginning and end nodes.
        from_node=index_node1
        to_node=index_node2
        if index_node2<index_node1:
            from_node=index_node2
            to_node=index_node1
        
        #Get subarray and reverse it
        flipped_subarray=np.flip(route[from_node:to_node+1])
        
        #Create and populate a new route.
        new_route=np.copy(route)
        for index in range(0,len(flipped_subarray)):
            new_route[from_node+index]=flipped_subarray[index]

        return new_route





