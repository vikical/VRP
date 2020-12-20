from src.models.solution import Solution
from src.neighborhoods.two_vehicles_neighborhood import TwoVehiclesNeighborhood
import numpy as np
import copy

class JoinCustomers(TwoVehiclesNeighborhood):
    """
    Get the vehicle with max allowed distances (receptor). Moves customers from the giver vehicle till there's no more empty
    space in "receptor".
    """

    def _operation_between_vehicle_routes(self, solution:Solution,vehicle1:int, vehicle2:int)->Solution:
        """
        Move as many customers as
        """
        #Get the vehicle with max allowed distance.
        max_allowed_distance1=self.solution_restrictions_calculator.vehicle_allowed_distances.distances[vehicle1]
        max_allowed_distance2=self.solution_restrictions_calculator.vehicle_allowed_distances.distances[vehicle2]
        
        #Set who give and receives customers.
        receptor_vehicle=vehicle1
        giver_vehicle=vehicle2
        if max_allowed_distance1<max_allowed_distance2:
            receptor_vehicle=vehicle2
            giver_vehicle=vehicle1

        #Find depot position in receptor and how many indexes are still empty
        receptor_route=solution.vehicle_routes[receptor_vehicle]
        depot_index=np.where(receptor_route<=0)[0][0]
        num_empty_indexes_in_receptor=receptor_route.shape[0]-depot_index


        #Copy the customers in charge of "giver" vehicle to "receptor" vehicle.
        for index in range(0,num_empty_indexes_in_receptor):
            solution.vehicle_routes[receptor_vehicle][depot_index+index]=solution.vehicle_routes[giver_vehicle][index]
            solution.vehicle_routes[giver_vehicle][index]=0


        return solution