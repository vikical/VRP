import csv
import pandas as pd
import numpy as np
import os

import src.file_management.files_nomenclature as fn

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
            file_id=filein_name.split("_")[-1]
            path_fileoutput=os.sep.join([path_to_directory,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES+file_id])
            np.savetxt(fname=path_fileoutput, X=veh_distances, fmt='%i', delimiter='\t', newline='\n')


