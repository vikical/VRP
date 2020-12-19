import numpy as np

class Solution(object):
    """
    Wrap the numpy.ndarray linked to the solution. In the end, it will be a np.ndarray with dimensions [num_vehicles,num_nodes].
    Each row means the nodes a vehicle visits. The row has num_nodes, but as soon we reach 0 node, it means we arrive at depot :[5 2 3 0 ... 0 0]    
    """
    def __init__(self, vehicle_routes:np.ndarray):
        self.vehicle_routes=vehicle_routes
        self.cost=-1
        self.is_valid=None

    def to_string(self)->str:
        """
        Transforms matrix vehicle routes to string
        """
        string_solution=""
        for v_index in range(0,self.vehicle_routes.shape[0]):
            string_solution=string_solution+"\n"+"VEHICLE:"+str(v_index)+"\n"
            string_solution=string_solution+self.route_to_string(vehicle_route=self.vehicle_routes[v_index])
        
        return string_solution

    def route_to_string(self,vehicle_route:np.ndarray)->str:
        return np.array_str(a=vehicle_route)



    
