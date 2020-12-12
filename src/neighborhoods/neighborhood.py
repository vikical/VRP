from src.models.solution import Solution
import numpy as np

class Neighborhood(object):
    """
    Abstract class for neighborhoods where the solution evolves to the optimal solution, or at least to a local minimum.
    """
    def __init__(self, solution:Solution)->Solution:
        self.solution=solution    

    def get_neighbor(self):
        """
        Get a neighbor solution
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
