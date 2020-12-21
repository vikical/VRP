import click, os, time

from src.file_management.reader import Reader
from src.file_management.writer import Writer
from src.file_management import files_nomenclature as fn

from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.solution_management.solution_initializer import SolutionInitializer

from src.data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator
from src.solution_management.solution_initializer import SolutionInitializer

from src.neighborhoods.neighborhood_factory import NeighborhoodFactory

from src.metaheuristics.ls import LS
from src.metaheuristics.vnd import VND
from src.metaheuristics.bvns import BVNS
from src.metaheuristics.tabu import Tabu
from src.metaheuristics.metaheuristic import Metaheuristic

def execute_single_instance(path_to_nodes_distances:str, path_to_max_vehicle_distances:str, \
    problem,metaheu,niter,search,init,memory)->():
    node_distances=NodeDistances(distances=Reader.read_distances_between_nodes_in_file(path_to_file=path_to_nodes_distances))
    vehicle_allowed_distances=VehicleAllowedDistances(distances=Reader.read_vehicle_allowed_distances_in_file(path_to_file=path_to_max_vehicle_distances))

    solution_restrictions_calculator=SolutionRestrictionsCalculator(node_distances=node_distances, vehicle_allowed_distances=vehicle_allowed_distances)
    metaheu_obj=get_metaheuristic(metaheu=metaheu, solution_restrictions_calculator=solution_restrictions_calculator, \
        init=init, search_type=search, number_iterations=niter, memory_size=memory)
    
    tic=time.time()
    solution=metaheu_obj.run()
    tac=time.time()
    elapsed_time=tac-tic
    return (solution,elapsed_time)
    

def get_metaheuristic(metaheu:str, solution_restrictions_calculator:SolutionRestrictionsCalculator,\
    search_type:str, init:str, number_iterations:int, memory_size:int)-> Metaheuristic:
    metaheu_obj=None
    if metaheu=="tabu":
        metaheu_obj=Tabu(solution=None,neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations, memory_size=memory_size)

    if metaheu=="ls":
        metaheu_obj=LS(solution=None, neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations)

    if metaheu=="bvns":
        metaheu_obj=BVNS(solution=None, \
                neighborhood_names=[NeighborhoodFactory.JOIN_CUSTOMERS,NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations)

    if metaheu=="vnd":
        metaheu_obj=VND(solution=None, \
                neighborhood_names=[NeighborhoodFactory.JOIN_CUSTOMERS,NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init,num_iteration_per_search=number_iterations)


    return metaheu_obj

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
@click.option("--problem", default="0", help="Number of the problem instance to be solved, i.e. the NUMBER in the dist_NUMBER.txt files")
@click.option("--metaheu", help="Type of metaheuristic: ls-local search; bvns-basic VNS")
@click.option("--niter", default=1000, help="Number of iters per each LS")
@click.option("--search", default=Metaheuristic.GREEDY_SEARCH, help="Decides between greedy search ('greedy') or anxious search ('anxious')")
@click.option("--init", default=Metaheuristic.RANDOM_INIT, help="Dedices whether to init randomly ('random'), one customer to one client ('one2one'), a group of nodes ('group') ")
@click.option("--memory", default=0, help="For tabú search: size of the memory where solutions are stored.")
def solve(din,problem,metaheu,niter,search,init,memory):
    path_to_node_distances=os.sep.join([din,fn.PREFFIX_DISTANCE_BETWEEN_NODES+str(problem)+".txt"])
    path_to_max_vehicle_distances=os.sep.join([din,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES+str(problem)+".txt"])
    (solution,elapsed_time)=execute_single_instance(path_to_nodes_distances=path_to_node_distances, path_to_max_vehicle_distances=path_to_max_vehicle_distances, \
    problem=problem,metaheu=metaheu,niter=niter,search=search,init=init,memory=memory)        
    

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