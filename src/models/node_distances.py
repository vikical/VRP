import numpy as np

class NodeDistances(object):
    """
    Wrap numpy.ndarray (NxN) for distances between nodes.
    """
    def __init__(self, distances:np.ndarray):
        self.distances=distances

    def get_number_of_nodes(self)->int:
        return np.size(self.distances,axis=0)    