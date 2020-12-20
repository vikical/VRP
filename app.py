import click, os

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




def get_metaheuristic(metaheu:str, solution_restrictions_calculator:SolutionRestrictionsCalculator,\
    search_type:str, init:str, number_iterations:int)-> Metaheuristic:
    metaheu_obj=None
    if metaheu=="tabu":
        metaheu_obj=Tabu(solution=None,neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations, memory_size=25)

    if metaheu=="ls":
        metaheu_obj=LS(solution=None, neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=100)

    if metaheu=="bvns":
        metaheu_obj=BVNS(solution=None, \
                neighborhood_names=[NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
                solution_restrictions_calculator=solution_restrictions_calculator, \
                search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations)

    if metaheu=="vnd":
        metaheu_obj=VND(solution=None, \
                neighborhood_names=[NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
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
@click.option("--problem", default="all", help="Number of the problem instance to be solved, i.e. the NUMBER in the dist_NUMBER.txt files")
@click.option("--metaheu", help="Type of metaheuristic: ls-local search; bvns-basic VNS")
@click.option("--niter", default=1000, help="Number of iters per each LS")
@click.option("--search", default=Metaheuristic.GREEDY_SEARCH, help="Decides between greedy search ('greedy') or anxious search ('anxious')")
@click.option("--init", default=Metaheuristic.RANDOM_INIT, help="Dedices whether to init randomly ('random') or sequentially ('sequential')")
def solve(din,problem,metaheu,niter,search,init):
    path_to_file=os.sep.join([din,fn.PREFFIX_DISTANCE_BETWEEN_NODES+str(problem)+".txt"])
    node_distances=NodeDistances(distances=Reader.read_distances_between_nodes_in_file(path_to_file=path_to_file))
    path_to_file=os.sep.join([din,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES+str(problem)+".txt"])
    vehicle_allowed_distances=VehicleAllowedDistances(distances=Reader.read_vehicle_allowed_distances_in_file(path_to_file=path_to_file))

    solution_restrictions_calculator=SolutionRestrictionsCalculator(node_distances=node_distances, vehicle_allowed_distances=vehicle_allowed_distances)
    metaheu_obj=get_metaheuristic(metaheu=metaheu, solution_restrictions_calculator=solution_restrictions_calculator, \
        init=init, search_type=search, number_iterations=niter)
    
    solution=metaheu_obj.run()
    print("solution cost:"+str(solution.cost)+"\n")
    print("vehicle_routes:\n"+solution.to_string())


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