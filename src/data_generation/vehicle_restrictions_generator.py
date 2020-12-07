import numpy as np

class VehicleRestrictionsGenerator():
    """
    Generates restrictions for the vehicles involved in the route.
    """
    
    @staticmethod
    def get_minimun_allowed_distance(distances_between_nodes:np.ndarray):
        """
        Get the minimun distance a vehicle should possess to be considered in the problem.
        This distance should be the length to go to a node and back from it.
        """
        go_and_back_distances:np.ndarray=distances_between_nodes+distances_between_nodes.transpose()
        return go_and_back_distances.max()
