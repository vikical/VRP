# VRP
Metaheuristics for a variant of VRP problem

# GENERAL CONSIDERATIONS
Num. vehicles = num. customers = nodes - 1 (the depot)
All vehicles can reach at least the farthest node. That means that at worst solution 1 vehicle can serve 1 customer.


# DATA GENERATION
Distances between nodes were obtained from the samples provided by: https://www.mech.kuleuven.be/en/cib/op
Particularly, for the original dataset used to solve VRPCD: http://web.ntust.edu.tw/~vincent/ovrpcd/

To generate the max. distance that a vehicle can travel, a file with the same format as the ones used to set distances (dist_X.txt) is needed.
Placing that kind of files in one directory, to obtain the distances for vehicles, the following command has to be run:
python app.py veh --din ${PATH_TO_DISTANCE_FILES}

# TEST
From VRP root folder invoke:
python -m pytest test
