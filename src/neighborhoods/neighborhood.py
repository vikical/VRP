from src.models.solution import Solution
from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

import numpy as np

class Neighborhood(object):
    """
    Abstract class for neighborhoods where the solution evolves to the optimal solution, or at least to a local minimum.
    """
    def __init__(self, solution:Solution, solution_restrictions_calculator:SolutionRestrictionsCalculator):
        self.solution=solution
        self.solution_restrictions_calculator=solution_restrictions_calculator


    def get_neighbor(self)->Solution:
        """
        Calculate neighbor, analysing the cost and whether the obtained solution is a valid one.
        """
        raise NotImplementedError


    def get_different_instances(self,available_instances:int,how_many:int)->np.ndarray:
        """
        Get "some" instances. They are returned into an array.
        """
        instances_involved=range(0,available_instances-1)

        instances=np.random.choice(a=instances_involved,size=how_many,replacement=False)
        if how_many==1:
            return np.ndarray(instances)

        return np.ndarray


    def _move_depot_to_the_end(self, route:np.ndarray)->np.ndarray:
        """
        If depot (=0) is in the middle of the route, we move it to the end.
        """
        customer_indexes=np.where(route > 0)[0]
        num_customers=len(customer_indexes)
        if (num_customers-1)==customer_indexes[num_customers-1]:
            return route
        
        new_route=np.zeros(shape=route.shape)
        new_route_index=0
        for index in customer_indexes:
            new_route[new_route_index]=route[index]
            new_route_index=new_route_index+1

        return new_route

    def _update_solution_cost(self,new_solution:Solution,vehicles_involved:np.ndarray)->int:
        """
        Based on previous cost, we substract the cost of involved routes and add the new costs.
        """
        if self.solution.cost<0:
            self.solution.cost=self.solution_restrictions_calculator.calculate_cost(self.solution)

        new_cost=self.solution.cost
        for vehicle in vehicles_involved:
            old_vehicle_consumed_distance=self.solution_restrictions_calculator.get_vehicle_consumed_distance(solution=self.solution, vehicle=vehicle)
            new_vehicle_consumed_distance=self.solution_restrictions_calculator.get_vehicle_consumed_distance(solution=new_solution, vehicle=vehicle)
            new_cost=new_cost-old_vehicle_consumed_distance+new_vehicle_consumed_distance
        
        return new_cost

    def _check_valid_modifications(self,new_solution:Solution, vehicles_involved:np.ndarray)->bool:
        """
        Check whether the modifications in the involved vehicles are valid.
        """
        for vehicle in vehicles_involved:
            remaining_distance=self.solution_restrictions_calculator.get_remaining_distance(solution=new_solution,vehicle=vehicle)
            if remaining_distance<0:
                return False
        
        return True
