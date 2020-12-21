import numpy as np
import random

from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances
from src.models.solution import Solution

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class SolutionInitializer(object):
    """
    Initializes a solution. 
    """
    def __init__(self,node_distances:NodeDistances, vehicle_allowed_distances:VehicleAllowedDistances):
        self.node_distances=node_distances
        self.vehicle_allowed_distances=vehicle_allowed_distances
        self.solution_restrictions_calculator=SolutionRestrictionsCalculator(node_distances=node_distances, \
            vehicle_allowed_distances=vehicle_allowed_distances)
    


    def init_randomly(self)->Solution:
        """
        For each customer we randomly select a vehicle. If the fleet contains vehicles which cannot performe a certain
        trip, it may lead to unfeasible solutions.
        We reject invalid solutions, so we will try till a valid ones is obtained randomly.
        """
        return self.__init_solution(initializing_function=self.__assign_nodes_randomly)

    def init_one_node_to_one_vehicle(self)->Solution:
        """
        We assign randomly one node to one vehicle.
        This should lead to a valid solution. However we will check it and look for another solution in case we found 
        a no-valid one.
        """
        return self.__init_solution(initializing_function=self.__assign_one_node_to_one_vehicle)

    def init_vehicles_with_group_nodes_sequentially(self)->Solution:
        """
        We assign nodes sequeantially to vehicles till they reach their restriction.
        This should lead to a valid solution. However we will check it and look for another solution in case we found 
        a no-valid one.
        """
        return self.__init_solution(initializing_function=self.__assign_group_nodes_sequentially_to_vehicles)


    def __init_solution(self,initializing_function)->Solution:
        """
        Initializing the solution, using the function passed as parameter to create the vehicle routes.
        After 100 attempts we consider an error must be happening and a exception is raised.
        """
        attempt=0
        solution_is_valid=False
        while solution_is_valid==False:
            if attempt>=100:
                raise Exception("Initial VALID solution not found after "+str(attempt)+" attempts.")
            attempt=attempt+1
            vehicle_routes=initializing_function()
            solution=Solution(vehicle_routes=vehicle_routes)
            solution_is_valid=self.solution_restrictions_calculator.check_if_solution_is_valid(solution=solution)

        solution.is_valid=True
        solution.cost=self.solution_restrictions_calculator.calculate_cost(solution=solution)

        return solution
        
        
    def __assign_nodes_randomly(self)->np.ndarray:
        """
        Assign nodes randomly
        """
        num_vehicles=self.vehicle_allowed_distances.get_number_of_vehicles()
        num_nodes=self.node_distances.get_number_of_nodes()
        vehicle_routes=np.zeros([num_vehicles,num_nodes],dtype=int)

        for node in range(1,num_nodes):
            vehicle=random.randint(0,num_vehicles-1)
            route=vehicle_routes[vehicle]
            available_indexes=np.where(route==0)[0]
            index=available_indexes[0]
            vehicle_routes[vehicle][index]=node 

        return vehicle_routes


    def __assign_group_nodes_sequentially_to_vehicles(self)->np.ndarray:
        """
        We assign nodes sequeantially to vehicles till they reach their restriction.
        This will lead to a valid solution.
        """
        allowed_distances=self.vehicle_allowed_distances.distances
        num_nodes=self.node_distances.get_number_of_nodes()
        vehicle_routes=np.zeros([len(allowed_distances),num_nodes],dtype=int)

        vehicle=0
        index_node=0
        node_list=list(range(1,num_nodes))
        random.shuffle(node_list)
        for node in node_list: #we suffle from 1 in order to ignore depot (=0)
            #Asign and check if valid
            vehicle_routes[vehicle][index_node]=node 
            remaining_distance=self.solution_restrictions_calculator.get_remaining_distance(route=vehicle_routes[vehicle], \
                node_distances=self.node_distances, allowed_distance=allowed_distances[vehicle])
            
            #If no valid, undo the assignmment and move to next vehicle.
            if remaining_distance<0:
                vehicle_routes[vehicle][index_node]=0
                vehicle=vehicle+1
                index_node=0
                vehicle_routes[vehicle][index_node]=node

            #Move to next index.
            index_node=index_node+1
        
        return vehicle_routes

    def __assign_one_node_to_one_vehicle(self)->np.ndarray:
        """
        As Clark and Wright, we assign one node to one vehicle.
        """
        num_vehicles=self.vehicle_allowed_distances.get_number_of_vehicles()
        num_nodes=self.node_distances.get_number_of_nodes()
        vehicle_routes=np.zeros([num_vehicles,num_nodes],dtype=int)
        suffled_customers=np.array(range(1,num_nodes),dtype=int)
        random.shuffle(suffled_customers)

        for index in range(0,num_vehicles):            
            vehicle_routes[index][0]=suffled_customers[index] 

        return vehicle_routes
