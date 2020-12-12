from src.models.solution import Solution
from src.neighborhoods.neighborhood import Neighborhood
import numpy as np

class MoveCustomer(Neighborhood):
    """
    Move customer from one route to another one.
    """


    def get_neighbor(self)->Solution:
        """
        Choose two routes randomly and move customer one customer from the first route to the second.
        """        
        solution=self.solution
        num_vehicles=solution.vehicle_routes.shape[0]
        if num_vehicles<2:
            return solution

        #Get vehicles involved in the movement.
        vehicles_involved=self.get_different_instances(available_instances=num_vehicles,how_many=2)
        veh1=vehicles_involved[0]
        veh2=vehicles_involved[1]
      
        #Get customer who are to be moved.
        node_index_in1=self.__get_node_from_route(solution.vehicle_routes[veh1])
        node_index_in2=self.__get_node_from_route(solution.vehicle_routes[veh2])

        #Move nodes
        solution=self.move_nodes(vehicle1=veh1, vehicle2=veh2, node_index_in1=node_index_in1, node_index_in2=node_index_in2)
        solution.vehicle_routes[veh1]=self._move_depot_to_the_end(route=solution.vehicle_routes[veh1])
        solution.vehicle_routes[veh2]=self._move_depot_to_the_end(route=solution.vehicle_routes[veh2])

        return solution

    def __get_node_from_route(self,route:np.ndarray)->int:
        """
        We prioritize customer nodes, but if no one is feasible, we return the depot.
        """
        index_customers_in_route=np.where(route>0)
        num_customers=len(index_customers_in_route)

        #If the route has no customers, we return the 1st index (= depot)
        if num_customers<=0:
            return 0

        node_index= self.get_different_instances(available_instances=num_customers,how_many=1)[0]
        
        return node_index

    def move_nodes(self, vehicle1:int, vehicle2:int, node_index_in1:int,node_index_in2)->Solution:
        solution=self.solution

        node_value_in1=solution.vehicle_routes[vehicle1][node_index_in1]
        node_value_in2=solution.vehicle_routes[vehicle2][node_index_in2]

        #Both nodes are the same (= depot)
        if node_value_in1==node_value_in2:
            return solution

        #We change it.
        solution.vehicle_routes[vehicle1][node_index_in1]=node_value_in2
        solution.vehicle_routes[vehicle2][node_index_in2]=node_value_in1

        return solution