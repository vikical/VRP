import numpy as np

class Solution(object):
    """
    Wrap the numpy.ndarray linked to the solution. In the end, it will be a np.ndarray with dimensions [num_nodes, num_nodes, num_vehicles].
    This way, axis x reflect the route of vehicle i. Axis y and z reflect whether a travel from y_j to z_k has been made.
    First row/column is the depot.
    """
    def __init__(self, vehicle_routes:np.ndarray):
        self.vehicle_routes=vehicle_routes



    
