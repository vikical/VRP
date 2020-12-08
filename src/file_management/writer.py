import csv
import pandas as pd
import numpy as np
import os

class Writer(object):
    """
    Class for writing files.
    """

    @staticmethod
    def save_max_allowed_vehicle_distances(path_to_directory,files_vehdistances:{}):
        """
        Given a directory and a dict (key=file_input, value=numpy.ndarray), a new output file (name="veh_{$file_input}")
        containing the ndarray is stored
        """
        for filein_name, veh_distances in files_vehdistances.items():
            path_fileoutput=os.sep.join([path_to_directory,"veh_"+filein_name])
            np.savetxt(fname=path_fileoutput, X=veh_distances, fmt='%i', delimiter='\t', newline='\n')
