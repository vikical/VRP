from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator
from src.solution_management.solution_initializer import SolutionInitializer

from src.metaheuristics.ls import LS
from src.metaheuristics.vnd import VND
from src.metaheuristics.bvns import BVNS
from src.metaheuristics.ts import TS
from src.metaheuristics.metaheuristic import Metaheuristic

from src.neighborhoods.neighborhood_factory import NeighborhoodFactory

class MetaheuristicFactory(object):
    """
    Creates Metaheuristic objects.
    """
    TABU_SEARCH="ts"
    LOCAL_SEARCH="ls"
    VND="vnd"
    BVNS="bvns"


    @staticmethod
    def create_metaheuristic(metaheuristic:str, solution_restrictions_calculator:SolutionRestrictionsCalculator,\
        search_type:str, init:str, number_iterations:int, memory_size:int,max_running_secs:float)-> Metaheuristic:
        metaheu_obj=None
        if metaheuristic==MetaheuristicFactory.TABU_SEARCH:
            metaheu_obj=TS(solution=None,neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                    solution_restrictions_calculator=solution_restrictions_calculator, \
                    search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations,\
                    max_running_secs=max_running_secs, memory_size=memory_size)

        if metaheuristic==MetaheuristicFactory.LOCAL_SEARCH:
            metaheu_obj=LS(solution=None, neighborhood_name=NeighborhoodFactory.MOVE_CUSTOMER, \
                    solution_restrictions_calculator=solution_restrictions_calculator, \
                    search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations,\
                    max_running_secs=max_running_secs)

        if metaheuristic==MetaheuristicFactory.BVNS:
            metaheu_obj=BVNS(solution=None, \
                    neighborhood_names=[NeighborhoodFactory.JOIN_CUSTOMERS,NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
                    solution_restrictions_calculator=solution_restrictions_calculator, \
                    search_type=search_type, initialization_type=init, num_iteration_per_search=number_iterations,\
                    max_running_secs=max_running_secs)

        if metaheuristic==MetaheuristicFactory.VND:
            metaheu_obj=VND(solution=None, \
                    neighborhood_names=[NeighborhoodFactory.JOIN_CUSTOMERS,NeighborhoodFactory.MOVE_CUSTOMER, NeighborhoodFactory.SWAP_CUSTOMERS, NeighborhoodFactory.REVERSE_ORDER], \
                    solution_restrictions_calculator=solution_restrictions_calculator, \
                    initialization_type=init,num_iteration_per_search=number_iterations,\
                    max_running_secs=max_running_secs)


        return metaheu_obj