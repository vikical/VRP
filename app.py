import click, os, time

from src.file_management.reader import Reader
from src.file_management.writer import Writer
from src.file_management import files_nomenclature as fn


from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator
from src.metaheuristics.metaheuristic import Metaheuristic
from src.test_bench.execution import Execution

import logging, sys

def set_logging(log:str):
    log_level=logging.getLevelName(log)
    logging.basicConfig(stream=sys.stderr, level=log_level)

@click.group()
def vrp():
    pass

@vrp.command()
def man():
    '''
    Shows man
    '''
    click.echo("""To invoke the app the following commands can be used (without --):
           veh: create a file for distance restriction for vehicles
           solve: solve an instance of a problem. It is identified by an integer. The correspondent files are needed (dist_*.txt and veh_dist_*.txt).
           man: show the manual""")


@vrp.command()
@click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes and for vehicles are located. This files should follow reg. exp. dist_NUMBER.txt and veh_dist_NUMBER.txt")
@click.option("--metaheu", default="" , help="Comma-separed list of metaheuristics which are going to be compare. Options: ls (local search); ts (tabu search); vnd; bvns")
@click.option("--niter", default=10, help="Number of iters per each local search.")
@click.option("--search", default=Metaheuristic.GREEDY_SEARCH, help="Decides between greedy search ('greedy') or anxious search ('anxious')")
@click.option("--init", default=Metaheuristic.RANDOM_INIT, help="Dedices whether to init randomly ('random'), one customer to one client ('one2one'), a group of nodes ('group') ")
@click.option("--memory", default=0, help="For tabú search: size of the memory where solutions are stored.")
@click.option("--log", default='CRITICAL', help="Log level: 'DEBUG', 'INFO', 'CRITICAL")
@click.option("--maxs", default=3.0, help="Max seconds an algorithm will run")
@click.option("--times4ave",default=100, help="Number of times a problem instances is solved, to get an average of the solutions")
def testbench(din,metaheu,niter,search,init,memory,times4ave,log,maxs):
    set_logging(log=log)

    logging.info("STARTING TEST BENCH...")

    filename="TESTBENCH_metaheu_"+metaheu.replace(",","_")+"__niter_"+str(niter)+"_search_"+str(search)+"_init_"+str(init)+"_memory_"+str(memory)+"_times4ave_"+str(times4ave)+"_maxs_"+str(maxs)+".csv"
    path_to_result_file=os.sep.join([din,filename])
    logging.info("The results will stored in:"+str(path_to_result_file))

    problem_instances_files=Reader.read_all_node_and_vehicle_distances_files(path_to_directory=din)
    logging.info("Files where problem instances are stored... READ.")

    logging.info("Starging test bench. It may last several minutes depending on the parameters chosen.")
    execution=Execution(number_iterations=niter,search_type=search,init=init,memory_size=memory,max_running_secs=maxs)
    df_result=execution.testbench(problem_instances_files=problem_instances_files,metaheuristics=metaheu.split(","),ntimes_for_average=times4ave)
    logging.info("FINISHED")
    
    logging.info("Saving results...")
    df_result.to_csv(path_or_buf=path_to_result_file)

    print("TEST BENCH DONE AND SAVED!!!")



@vrp.command()
@click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes and for vehicles are located. This files should follow reg. exp. dist_NUMBER.txt and veh_dist_NUMBER.txt")
@click.option("--problem", default="0", help="Number of the problem instance to be solved, i.e. the NUMBER in the dist_NUMBER.txt files")
@click.option("--metaheu", help="Type of metaheuristic: ls (local search); ts (tabu search); vnd; bvns")
@click.option("--niter", default=10, help="Number of iters per each local search")
@click.option("--search", default=Metaheuristic.GREEDY_SEARCH, help="Decides between greedy search ('greedy') or anxious search ('anxious')")
@click.option("--init", default=Metaheuristic.RANDOM_INIT, help="Dedices whether to init randomly ('random'), one customer to one client ('one2one'), a group of nodes ('group') ")
@click.option("--memory", default=0, help="For tabú search: size of the memory where solutions are stored.")
@click.option("--log", default='CRITICAL', help="Log level: 'DEBUG', 'INFO', 'CRITICAL")
@click.option("--maxs", default=3.0, help="Max seconds an algorithm will run")
def solve(din,problem,metaheu,niter,search,init,memory,log,maxs):
    set_logging(log=log)

    path_to_node_distances=os.sep.join([din,fn.PREFFIX_DISTANCE_BETWEEN_NODES+str(problem)+".txt"])
    path_to_max_vehicle_distances=os.sep.join([din,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES+str(problem)+".txt"])
    execution=Execution(number_iterations=niter,search_type=search,init=init,memory_size=memory,max_running_secs=maxs)
    (solution,elapsed_time)=execution.execute_single_instance_once(path_to_node_distances=path_to_node_distances, \
        path_to_max_vehicle_distances=path_to_max_vehicle_distances, metaheuristic=metaheu)
    

    print("\n\n ---------SOLUTION---------")
    print(solution.to_string())
    print("Cost:"+str(solution.cost))
    print("Consumed time:"+str(elapsed_time) +" s")


@vrp.command()
@click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes are located. This files should follow reg. exp. dist_NUMBER.txt")
def veh(din):
    '''
    Given a text file containing a NxN matrix (N=depot + (N-1)customers), where each cell is separated by tabs, 
    this command returns a file with N-1 values (allowed distances for a vehicle).
    This file will be named veh_{$file_in} and stored in the same directory as file_in.
    '''   
    files_nodedistances=Reader.read_distances_between_nodes_in_directory(din)
    files_vehdistances={}
    for filein_name, node_distances in files_nodedistances.items():
        generator=VehicleRestrictionsGenerator(distances_between_nodes=node_distances)
        files_vehdistances[filein_name]=generator.get_allowed_distances()
    
    Writer.save_max_allowed_vehicle_distances(din,files_vehdistances)


if __name__ == '__main__':
    vrp()