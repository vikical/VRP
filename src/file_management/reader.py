import csv
import pandas as pd
import numpy as np
import os

import src.file_management.files_nomenclature as fn

class Reader(object):
    """
    Class for reading input files.
    """

    @staticmethod
    def read_vehicle_allowed_distances_in_file(path_to_file:str)->np.ndarray:
        """
        Given an input path file, it reads the distance file. A matrix where d_ij is the distance between nodes i-j.
        Note that d_ij!=d_ji, for generalization purposes.
        """
        df=pd.read_csv(filepath_or_buffer=path_to_file,delimiter="\n",header=None).dropna(axis=1)
        return df.to_numpy()

    @staticmethod
    def read_vehicle_allowed_distances_in_directory(path_to_directory:str)->{}:
        """
        docstring
        """
        #TODO: HACER FUNCIÓN.
        pass


    @staticmethod
    def read_distances_between_nodes_in_file(path_to_file:str)->np.ndarray:
        """
        Given an input path file, it reads the distance file. A matrix where d_ij is the distance between nodes i-j.
        Note that d_ij!=d_ji, for generalization purposes.
        """
        df=pd.read_csv(filepath_or_buffer=path_to_file,delimiter="\t",header=None).dropna(axis=1)
        return df.to_numpy()


    @staticmethod
    def read_distances_between_nodes_in_directory(path_to_directory:str)->{}:
        """
        Given an input path file, it reads the distance file. A matrix where d_ij is the distance between nodes i-j.
        Note that d_ij!=d_ji, for generalization purposes.
        return: A dictionary where "key" is the filein_name and "value" is a numpy.ndarray with all the values.
        """
        files_contents={}
        for root, dirnames, filein_names in os.walk(path_to_directory):
            for filein_name in filein_names:
                if not filein_name.startswith(fn.PREFFIX_DISTANCE_BETWEEN_NODES):
                    continue

                path_filein=os.sep.join([path_to_directory,filein_name])
                distances_array=Reader.read_distances_between_nodes_in_file(path_to_file=path_filein)
                files_contents[filein_name]=distances_array

        return files_contents