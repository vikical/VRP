import numpy as np

class VehicleAllowedDistances(object):
    """
    Wrap the distance restrinctions for vehicles.
    """
    def __init__(self, distances:np.ndarray):
        self.distances=distances

    def get_number_of_vehicles(self)->int:
        return np.size(self.distances)
