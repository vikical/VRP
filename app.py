import click, os

from src.file_management.reader import Reader
from src.file_management.writer import Writer
from src.file_management import files_nomenclature as fn

from src.models.node_distances import NodeDistances
from src.models.vehicle_allowed_distances import VehicleAllowedDistances

from src.solution_management.solution_cost_calculator import SolutionCostCalculator
from src.solution_management.solution_initializer import SolutionInitializer
from src.solution_management.solution_printer import SolutionPrinter

from src.data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator
from src.solution_management.solution_initializer import SolutionInitializer

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
@click.option("--single", help="Number of the problem instance to be solved, i.e. the NUMBER in the dist_NUMBER.txt files")
@click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes and for vehicles are located. This files should follow reg. exp. dist_NUMBER.txt and veh_dist_NUMBER.txt")
def solve(single,din):
    path_to_file=os.sep.join([din,fn.PREFFIX_DISTANCE_BETWEEN_NODES+str(single)+".txt"])
    node_distances=NodeDistances(distances=Reader.read_distances_between_nodes_in_file(path_to_file=path_to_file))
    path_to_file=os.sep.join([din,fn.PREFFIX_ALLOWED_DISTANCE_VEHICLES+str(single)+".txt"])
    vehicle_allowed_distances=VehicleAllowedDistances(distances=Reader.read_vehicle_allowed_distances_in_file(path_to_file=path_to_file))

    initializer=SolutionInitializer(node_distances=node_distances,vehicle_allowed_distances=vehicle_allowed_distances)
    solution=initializer.init_randomly()
    cost_calculator=SolutionCostCalculator(solution=solution)
    cost=cost_calculator.calculate_cost(node_distances=node_distances)
    print("***************" + str(cost))
    print(SolutionPrinter.to_string_as_list_nodes(solution=solution))



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