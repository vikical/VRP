import click
from file_management.reader import Reader
from file_management.writer import Writer
from data_generation.vehicle_restrictions_generator import VehicleRestrictionsGenerator

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
           solve: solve an instance of a problem. It is identified by an integer. The correspondent files are needed (distances_*.txt and vehicles_*.txt).
           man: show the manual""")


# @vrp.command()
# @click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes are located. This files should follow reg. exp. dist_NUMBER.txt")
# def veh(din):
#     """Given a text file containing a NxN matrix, where each cell is separated by tabs, 
#     this command returns a file with N values (allowed distances for a vehicle).
#     This file will be named veh_{$file_in} and stored in the same directory as file_in"""
#     files_nodedistances=Reader.read_distances_between_nodes_in_directory(din)

#     files_vehdistances={}
#     for filein_name, node_distances in files_nodedistances:
#         generator=VehicleRestrictionsGenerator(distances_between_nodes=node_distances)
#         files_vehdistances[filein_name]=generator.get_allowed_distances(distances_between_nodes=node_distances)
    
#     Writer.save_max_allowed_vehicle_distances(din,files_vehdistances)

@vrp.command()
@click.option("--din", type=click.Path(exists=True), help="Path to the directory where files with distances between nodes are located. This files should follow reg. exp. dist_NUMBER.txt")
def veh(din):
    '''
    Given a text file containing a NxN matrix, where each cell is separated by tabs, 
    this command returns a file with N values (allowed distances for a vehicle).
    This file will be named veh_{$file_in} and stored in the same directory as file_in
    '''   
    files_nodedistances=Reader.read_distances_between_nodes_in_directory(din)
    files_vehdistances={}
    for filein_name, node_distances in files_nodedistances.items():
        generator=VehicleRestrictionsGenerator(distances_between_nodes=node_distances)
        files_vehdistances[filein_name]=generator.get_allowed_distances()
    
    Writer.save_max_allowed_vehicle_distances(din,files_vehdistances)


if __name__ == '__main__':
    vrp()