import time
import pandas as pd
import numpy as np
import logging

from src.file_management.reader import Reader

from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.metaheuristics.metaheuristic_factory import MetaheuristicFactory

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator


class Execution(object):
    """
    Support the execution of different metaheuristics on different problems.
    """
    def __init__(self, number_iterations:int,search_type:str,init:str,memory_size:int,max_running_secs:float ):
        self.number_iterations=number_iterations
        self.search_type=search_type
        self.init=init
        self.memory_size=memory_size
        self.max_running_secs=max_running_secs


    def testbench(self,problem_instances_files:[{}], metaheuristics=[str],ntimes_for_average:int=100)->pd.DataFrame:
        """
        Returns de analysis of the given instances, after executing the metaheuristics specified in metaheuristics.
        """
        #Get the analysis of all problem instances
        all_analysis=[]
        for pair_of_files in problem_instances_files:
            path_to_node_distances=pair_of_files["node_distances"]
            path_to_max_vehicle_distances=pair_of_files["vehicle_distances"]

            #Get the analysis done in each metaheuristic.
            problem_analysis=(path_to_node_distances,)
            for metaheuristic in metaheuristics:
                logging.critical("********************* "+metaheuristic+" on file: "+str(path_to_node_distances)+" *********************")
                execution_info=self.execute_single_instance_n_times(path_to_node_distances=path_to_node_distances, \
                    path_to_max_vehicle_distances=path_to_max_vehicle_distances, metaheuristic=metaheuristic,ntimes_for_average=ntimes_for_average)
                problem_analysis=problem_analysis+execution_info

            all_analysis.append(problem_analysis)

        #Build columns
        columns=["distance_file"]
        for metaheu in metaheuristics:
            columns.append(metaheu+"_av_elapsed_time")
            columns.append(metaheu+"_av_cost")
            columns.append(metaheu+"_best_cost")

        all_analysis_df=pd.DataFrame(data=np.array(all_analysis), columns=columns)

        return all_analysis_df

   

    def execute_single_instance_n_times(self, path_to_node_distances:str, path_to_max_vehicle_distances:str, metaheuristic:str, ntimes_for_average:int=100)->():
        """
        Returns and np.ndarray where the positions means:
        [averaged_elapsed_time, averaged_cost, best_cost]
        The parameter number_times indicates how many times the experiment will be done to perform the average.
        """
        total_elapsed_time=0
        total_cost=0
        best_cost=-1
        for iter in range(0,ntimes_for_average):
            logging.critical("exec"+str(iter)+", ")
            (solution,elapsed_time)=self.execute_single_instance_once(path_to_node_distances=path_to_node_distances, \
                path_to_max_vehicle_distances=path_to_max_vehicle_distances, metaheuristic=metaheuristic)

            total_elapsed_time=total_elapsed_time+elapsed_time
            total_cost=total_cost+solution.cost
            if best_cost<0 or best_cost>solution.cost:
                best_cost=solution.cost 

        return (total_elapsed_time/100, total_cost/100, best_cost)


    
    def execute_single_instance_once(self,path_to_node_distances:str, path_to_max_vehicle_distances:str, metaheuristic:str)->():
        """
        Execute a single instance of a problem, just only once.
        The result is a tuple containing:
        (solution, elapsed_time)
        """
        node_distances=NodeDistances(distances=Reader.read_distances_between_nodes_in_file(path_to_file=path_to_node_distances))
        vehicle_allowed_distances=VehicleAllowedDistances(distances=Reader.read_vehicle_allowed_distances_in_file(path_to_file=path_to_max_vehicle_distances))

        solution_restrictions_calculator=SolutionRestrictionsCalculator(node_distances=node_distances, vehicle_allowed_distances=vehicle_allowed_distances)
        metaheu_obj=MetaheuristicFactory.create_metaheuristic(metaheuristic=metaheuristic, solution_restrictions_calculator=solution_restrictions_calculator, \
            init=self.init, search_type=self.search_type, number_iterations=self.number_iterations, memory_size=self.memory_size, max_running_secs=self.max_running_secs)
        
        tic=time.time()
        solution=metaheu_obj.run()
        tac=time.time()
        elapsed_time=tac-tic
        return (solution,elapsed_time)