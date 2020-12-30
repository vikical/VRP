# VRP
Metaheuristics for a variant of VRP problem where vehicles are limited by a max. allowed distance, different among vehicles.

# GENERAL CONSIDERATIONS
Num. vehicles = num. customers = nodes - 1 (the depot)
All vehicles can reach at least the farthest node. That means that at worst solution 1 vehicle can serve 1 customer.

# REQUIREMENTS
Before running the programm, install requirements.txt file to meet python required libraries.
~~~
pip install -f requirements.txt
~~~

# DATA GENERATION
Distances between nodes were obtained from the samples provided by: https://www.mech.kuleuven.be/en/cib/op
Particularly, for the original dataset used to solve VRPCD: http://web.ntust.edu.tw/~vincent/ovrpcd/

To generate the max. distance that a vehicle can travel, a file with the same format as the ones used to set distances (dist_X.txt) is needed.
Placing that kind of files in one directory, to obtain the distances for vehicles, the following command has to be run:
~~~
python app.py veh --din ${PATH_TO_DISTANCE_FILES}
~~~

# RUNNING ONE INSTANCE
To run the problem getting on one single instance, use the following command:
~~~
python app.py solve --din *path_to_directory* --problem *problem_number* --metaheu *type_of_metaheuristic* --niter *iterations_per_search* --init *type_initialization* --memory *memory_size_for_tabu_search* --maxs *max_running_seconds*
~~~

The result of this execution will show the solution **cost** and the solution **routes**.

Example:
~~~
python app.py solve --din ./my_data --problem 0 --metaheu bvns --niter 1000 --init random 
~~~

# RUNNING TEST BENCH
To run a set of problems and obtain a .csv the following command should be executed:
~~~
python app.py testbench --din *path_to_directory* --metaheu *comma_separated_list_of_metaheu* *iterations_per_search* --init *type_initialization* --memory *memory_size_for_tabu_search* --log *type_of_logging*  --times4ave *time_for_average* --maxs *max_running_seconds*
~~~

Example:
~~~
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search greedy --log CRITICAL  --times4ave 100 --maxs 1
~~~

The result of this execution will be a .csv, stored in *path_to_directory* where each column will be the values obtained after *time_for_average* executions of each metaheuristic:
~~~
LS_average_execution_time ; LS_average_cost ; LS_best_cost ; VND_average_execution_time ; VND_average_cost ; VND_best_cost ; ...
... BVNS_average_execution_time; BVNS_average_cost; BVNS_best_cost; Tabu_average_execution_time; Tabu_average_cost ; Tabu_best_cost 
~~~

In the directory ./results the output files of the execution of **test_bench.sh**. Apart from that, individual .ods files have been added, where graphs based on the obtained data are displayed. A **Summary.ods** gathers all this information and add new graphs comparing results between executions with different parameters.

# TEST
From VRP root folder invoke:
python -m pytest test
