from src.models.solution import Solution
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

import numpy as np
import random

class Neighborhood(object):
    """
    Abstract class for neighborhoods where the solution evolves to the optimal solution, or at least to a local minimum.
    """
    def __init__(self, solution_restrictions_calculator:SolutionRestrictionsCalculator):
        self.solution_restrictions_calculator=solution_restrictions_calculator


    def get_neighbor(self, solution:Solution)->Solution:
        """
        Calculate neighbor, analysing the cost and whether the obtained solution is a valid one.
        """
        raise NotImplementedError


    def get_different_instances(self,available_instances:int,needed_instances:int)->np.ndarray:
        """
        Get "some" instances. They are returned into an array.
        If available<needed, None is returned.
        """
        if available_instances<needed_instances:
            return None
            
        instances_involved=range(0,available_instances)

        instances=np.random.choice(a=instances_involved,size=needed_instances,replace=False)

        return instances


    def _move_depot_to_the_end(self, route:np.ndarray)->np.ndarray:
        """
        If depot (=0) is in the middle of the route, we move it to the end.
        """
        customer_indexes=np.where(route > 0)[0]
        num_customers=len(customer_indexes)

        #If there's no customer => nothing to do.
        if num_customers<=0:
            return route

        #If customers are at the beginning => nothing to do.
        if (num_customers-1)==customer_indexes[num_customers-1]:
            return route
        
        #Move to the end.
        new_route=np.zeros(shape=route.shape)
        new_route_index=0
        for index in customer_indexes:
            new_route[new_route_index]=route[index]
            new_route_index=new_route_index+1

        return new_route

    def _update_solution_cost(self,old_solution:Solution,new_solution:Solution,vehicles_involved:np.ndarray)->int:
        """
        Based on previous cost, we substract the cost of involved routes and add the new costs.
        """
        if old_solution.cost<0:
            old_solution.cost=self.solution_restrictions_calculator.calculate_cost(old_solution)

        new_cost=old_solution.cost
        for vehicle in vehicles_involved:
            old_vehicle_consumed_distance=self.solution_restrictions_calculator.get_vehicle_consumed_distance(solution=old_solution, vehicle=vehicle)
            new_vehicle_consumed_distance=self.solution_restrictions_calculator.get_vehicle_consumed_distance(solution=new_solution, vehicle=vehicle)
            new_cost=new_cost-old_vehicle_consumed_distance+new_vehicle_consumed_distance

        return new_cost

    def _check_valid_modifications(self,new_solution:Solution, vehicles_involved:np.ndarray)->bool:
        """
        Check whether the modifications in the involved vehicles are valid.
        """
        for vehicle in vehicles_involved:
            remaining_distance=self.solution_restrictions_calculator.get_vehicle_remaining_distance(solution=new_solution,vehicle=vehicle)
            if remaining_distance<0:
                return False
        
        return True
