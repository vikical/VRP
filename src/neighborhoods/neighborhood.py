from src.models.solution import Solution

class neighborhood(object):
    """
    Abstract class for neighborhoods where the solution evolves to the optimal solution, or at least to a local minimum.
    """
    
    def get_neighbor(self, solution:Solution):
        """
        Get a neighbor solution
        """
        raise NotImplementedError