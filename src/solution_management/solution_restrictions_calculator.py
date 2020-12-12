import numpy as np
import random

from src.models.vehicle_allowed_distances import VehicleAllowedDistances
from src.models.node_distances import NodeDistances
from src.models.solution import Solution


class SolutionRestrictionsCalculator(object):
    """
    Compute the cost of a solution. 
    """
    def __init__(self,solution:Solution, node_distances:NodeDistances, vehicle_allowed_distances:VehicleAllowedDistances):
        self.solution=solution
        self.node_distances=node_distances
        self.vehicle_allowed_distances=vehicle_allowed_distances


    def calculate_cost(self)->int:
        """
        It returns a 3d matrix, where we store vehicles in X (index i).
        Y (index j) x Z (index k) means that the vehicle travels from node j to k.
        """
        total_distance=0
        num_vehicles=self.solution.vehicle_routes.shape[0]

        for vehicle in range(0,num_vehicles):
            vehicle_distance=self.get_vehicle_consumed_distance(vehicle=vehicle)
            total_distance=total_distance+vehicle_distance
        
        return total_distance

    def get_vehicle_consumed_distance(self, vehicle:int)->int:
        """
        Return consumed distance for a certain vehicle.
        """
        return SolutionRestrictionsCalculator.get_consumed_distance(route=self.solution.vehicle_routes[vehicle], \
            node_distances=self.node_distances)

    def get_vehicles_remaining_distances(self)->np.ndarray:
        """
        Get vehicles how much distance remain for each vehicle. If the distance has been exceeded, then the value is a negative one.
        """
        num_vehicles=self.solution.vehicle_routes.shape[0]
        vehicles_remaining_distances=np.zeros(shape=(1,num_vehicles),dtype=int)
        for vehicle in range(0,num_vehicles):
            vehicles_remaining_distances[vehicle]=self.get_vehicle_remaining_distance(vehicle=vehicle)
        
        return vehicles_remaining_distances

    def get_vehicle_remaining_distance(self, vehicle:int)->int:
        """
        Return remaining distances. If the distance has been exceeded, then the value is a negative one.
        """
        return SolutionRestrictionsCalculator.get_remaining_distance(route=self.solution.vehicle_routes[vehicle], \
                                            node_distances=self.node_distances, 
                                            allowed_distance=self.vehicle_allowed_distances.distances[vehicle])
    
    @staticmethod
    def get_consumed_distance(route:np.ndarray,node_distances:NodeDistances)->int:
        """
        Calculate the distance consumed in a certain route.
        """
        vehicle_distance=0
        previous_node=0
        for node in route:
            vehicle_distance=vehicle_distance+node_distances.distances[previous_node][node]
            previous_node=node
        return vehicle_distance  

    @staticmethod
    def get_remaining_distance(route:np.ndarray,node_distances:NodeDistances,allowed_distance:int)->int:
        """
        Calculate the remaining distance, given a route and an allowed distance
        """
        consumed_distance=SolutionRestrictionsCalculator.get_consumed_distance(route=route,node_distances=node_distances)
        return allowed_distance-consumed_distance



