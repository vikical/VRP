import csv
import pandas as pd
import numpy as np

class Reader(object):
    """
    Class for reading input files.
    """

    def __init__(self):
        pass

    @staticmethod
    def read_distances_between_nodes(path_to_file:path)->np.ndarray:
        """
        Given an input path file, it reads the distance file. A matrix where d_ij is the distance between nodes i-j.
        Note that d_ij!=d_ji, for generalization purposes.
        """
        df=pd.read_csv(url=path_to_file,delimiter="\t")
        return df.to_numpy()


