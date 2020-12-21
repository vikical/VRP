# VRP
Metaheuristics for a variant of VRP problem where vehicle are limited by a max. allowed distance, different among vehicles.

# GENERAL CONSIDERATIONS
Num. vehicles = num. customers = nodes - 1 (the depot)
All vehicles can reach at least the farthest node. That means that at worst solution 1 vehicle can serve 1 customer.

# DATA GENERATION
Distances between nodes were obtained from the samples provided by: https://www.mech.kuleuven.be/en/cib/op
Particularly, for the original dataset used to solve VRPCD: http://web.ntust.edu.tw/~vincent/ovrpcd/

To generate the max. distance that a vehicle can travel, a file with the same format as the ones used to set distances (dist_X.txt) is needed.
Placing that kind of files in one directory, to obtain the distances for vehicles, the following command has to be run:
python app.py veh --din ${PATH_TO_DISTANCE_FILES}

# RUNNING ONE INSTANCE
To run the problem getting on one single instance, use the following command:

python app.py solve --din _path_to_directory_ --problem *problem_number* --metaheu *type_of_metaheuristic* --niter *iterations_per_search* --init *type_initialization* --memory *memory_size_for_tabu_search*

The result of this execution will show the solution **cost** and the solution **routes**.

Example:
~~~
python app.py solve --din ./my_data --problem 0 --metaheu bvns --niter 1000 --init random 
~~~

# RUNNING TEST BENCH
To run a set of problems and obtain a .csv the following command should be executed:


The result of this execution will be a .csv where each column will be the values obtained after 100 running of each metaheuristic:
~~~
LS_average_execution_time ; LS_average_cost ; LS_best_cost ; Tabu_average_execution_time; Tabu_average_cost ; Tabu_best_cost ; ...
... VND_average_execution_time ; VND_average_cost ; VND_best_cost ; BVNS_average_execution_time; BVNS_average_cost; BVNS_best_cost
~~~

# TEST
From VRP root folder invoke:
python -m pytest test
