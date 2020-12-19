import numpy as np
import random

class VehicleRestrictionsGenerator():
    """
    Generates restrictions for the vehicles involved in the route.
    """
    def __init__(self, distances_between_nodes:np.ndarray):
        self.distances_between_nodes=distances_between_nodes
    
    @staticmethod
    def get_minimun_allowed_distance(distances_between_nodes:np.ndarray):
        """
        Get the minimun distance a vehicle should possess to be considered in the problem.
        This distance should be the length to go to a node and back from it.
        """
        go_and_back_distances:np.ndarray=distances_between_nodes+distances_between_nodes.transpose()
        return go_and_back_distances.max()

    @staticmethod
    def get_maximum_allowed_distance(distances_between_nodes:np.ndarray):
        """
        Get the maximum distance a vehicle will possess. In this case, the longer distance between nodes * 
        the number of nodes.
        """
        min_distance_to_one_node=distances_between_nodes.max()
        num_nodes=np.size(distances_between_nodes, axis=0)
        return num_nodes*min_distance_to_one_node


    def get_allowed_distances(self)->np.ndarray:
        """
        Get a range of distances for vehicles allowed for vehicles
        """
        min_distance=self.get_minimun_allowed_distance(distances_between_nodes=self.distances_between_nodes)
        max_distance=self.get_maximum_allowed_distance(distances_between_nodes=self.distances_between_nodes)
        
        distances=[]
        for i in range(0,np.size(self.distances_between_nodes,axis=0)-1):
            d = random.randint(min_distance,max_distance)
            distances.append(d)

        return distances