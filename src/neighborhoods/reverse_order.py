from src.models.solution import Solution
from src.neighborhoods.one_vehicle_neighborhood import OneVehicleNeighborhood
import numpy as np
import copy

class ReverseOrder(OneVehicleNeighborhood):
    """
    Pick randomly a route and two customers in it. Reverse the order between the customers between those customers.
    """

    def _operation_inside_vehicle_route(self,route:np.ndarray, index_node1:int, index_node2:int)->np.ndarray:
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





