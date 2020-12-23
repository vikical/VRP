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

    @staticmethod
    def read_all_node_and_vehicle_distances_files(path_to_directory:str)->[{}]:
        """
        Return a list of dictionary where the value of key:
           'node_distances': is the name of the file containing node distances.
           'vehicle_distances': is the name of the file containing vehicle distances.
        We ignore node_distance files which don't have a vehicle_distance one.
        """
        files_for_processing=[]
        for root, dirnames, filein_names in os.walk(path_to_directory):
            for filein_name in filein_names:
                #If file is not node_distances file, we continue.
                if not filein_name.startswith(fn.PREFFIX_DISTANCE_BETWEEN_NODES):
                    continue

                #Check if correspondent vehicle file exists.
                vehicle_file_name=filein_name.replace(fn.PREFFIX_DISTANCE_BETWEEN_NODES,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES)
                path_vehicle_file=os.sep.join([path_to_directory,vehicle_file_name])
                if os.path.isfile(path=path_vehicle_file)==False:
                    continue

                #If both files exists, we store them.
                path_node_file=os.sep.join([path_to_directory,filein_name])
                files_for_processing.append({"node_distances": path_node_file, "vehicle_distances": path_vehicle_file})

        return files_for_processing
