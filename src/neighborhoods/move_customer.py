import logging

from src.models.solution import Solution
from src.neighborhoods.two_vehicles_neighborhood import TwoVehiclesNeighborhood
import numpy as np
import copy

class MoveCustomer(TwoVehiclesNeighborhood):
    """
    Move customer from one route to another one.
    """

    def _operation_between_vehicle_routes(self, solution:Solution,vehicle1:int, vehicle2:int)->Solution:
        """
        Choose nodes from vehicles 1 and 2 and change them.
        """
        #Get the index which contain the nodes that will be moved
        node_index_in1=super()._get_node_index_from_route(solution.vehicle_routes[vehicle1])
        node_index_in2=super()._get_node_index_from_route(solution.vehicle_routes[vehicle2])
        
        return self._move_nodes(solution=solution,vehicle1=vehicle1, vehicle2=vehicle2, node_index_in1=node_index_in1, node_index_in2=node_index_in2)


    def _move_nodes(self, solution: Solution, vehicle1:int, vehicle2:int, node_index_in1:int, node_index_in2)->Solution:
        """
        Move node_index_in1 from vehicle1 to node_index_in2 to vehicle2 and viceversa.
        """
        #Get the customer in that nodes.
        node_value_in1=solution.vehicle_routes[vehicle1][node_index_in1]
        node_value_in2=solution.vehicle_routes[vehicle2][node_index_in2]

        #Both nodes are the same (= depot)
        if node_value_in1==node_value_in2:
            return solution

        #We change it.
        logging.debug("change: "+"v"+str(vehicle1)+".n"+str(node_index_in1)+" <-> v"+str(vehicle2)+".n"+str(node_index_in2))
        solution.vehicle_routes[vehicle1][node_index_in1]=node_value_in2
        solution.vehicle_routes[vehicle2][node_index_in2]=node_value_in1

        return solution