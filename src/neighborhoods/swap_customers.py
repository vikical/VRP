from src.models.solution import Solution
from src.neighborhoods.one_customer_neighborhood import OneCustomerNeighborhood
import numpy as np
import copy

class SwapCustomers(OneCustomerNeighborhood):
    """
    Pick randomly a route and two customers in it. Swap them.
    """

    def _operation_inside_vehicle_route(self,route:np.ndarray, index_node1:int, index_node2:int)->np.ndarray:
        if index_node1==index_node2:
            return route
        
        new_route=np.copy(route)
        new_route[index_node1]=route[index_node2]
        new_route[index_node2]=route[index_node1]

        return new_route

