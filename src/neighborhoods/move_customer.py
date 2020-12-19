from src.models.solution import Solution
from src.neighborhoods.neighborhood import Neighborhood
import numpy as np
import copy

class MoveCustomer(Neighborhood):
    """
    Move customer from one route to another one.
    """


    def get_neighbor(self,solution:Solution)->Solution:
        """
        Choose two routes randomly and move customer one customer from the first route to the second.
        """        
        num_vehicles=solution.vehicle_routes.shape[0]
        if num_vehicles<2:
            return solution

        #Get vehicles involved in the movement.
        vehicles_involved=self.get_different_instances(available_instances=num_vehicles,needed_instances=2)
        veh1=vehicles_involved[0]
        veh2=vehicles_involved[1]
      
        #Get customer who are to be moved.
        node_index_in1=self.__get_node_from_route(solution.vehicle_routes[veh1])
        node_index_in2=self.__get_node_from_route(solution.vehicle_routes[veh2])

        #Move nodes
        new_solution=self.move_nodes(solution=solution,vehicle1=veh1, vehicle2=veh2, node_index_in1=node_index_in1, node_index_in2=node_index_in2)
        new_solution.vehicle_routes[veh1]=self._move_depot_to_the_end(route=new_solution.vehicle_routes[veh1])
        new_solution.vehicle_routes[veh2]=self._move_depot_to_the_end(route=new_solution.vehicle_routes[veh2])

        #Verify movements.
        valid=self._check_valid_modifications(new_solution=new_solution,vehicles_involved=vehicles_involved)
        if valid==False:
            new_solution.is_valid=False

        #Set new cost.
        new_solution.cost=self._update_solution_cost(old_solution=solution,new_solution=new_solution,vehicles_involved=vehicles_involved)

        return new_solution

    def __get_node_from_route(self,route:np.ndarray)->int:
        """
        We prioritize customer nodes, but if no one is feasible, we return the depot.
        """
        index_customers_in_route=np.where(route>0)
        num_customers=len(index_customers_in_route)

        #If the route has no customers, we return the 1st index (= depot)
        if num_customers<=0:
            return 0

        node_index= self.get_different_instances(available_instances=num_customers,needed_instances=1)[0]
        
        return node_index

    def move_nodes(self, solution:Solution,vehicle1:int, vehicle2:int, node_index_in1:int,node_index_in2)->Solution:
        node_value_in1=solution.vehicle_routes[vehicle1][node_index_in1]
        node_value_in2=solution.vehicle_routes[vehicle2][node_index_in2]

        #Both nodes are the same (= depot)
        if node_value_in1==node_value_in2:
            return solution

        #We change it.
        new_solution=copy.deepcopy(solution)
        new_solution.vehicle_routes[vehicle1][node_index_in1]=node_value_in2
        new_solution.vehicle_routes[vehicle2][node_index_in2]=node_value_in1

        return new_solution