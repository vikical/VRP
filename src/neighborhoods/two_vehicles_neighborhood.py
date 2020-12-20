from src.models.solution import Solution
from src.neighborhoods.neighborhood import Neighborhood
import numpy as np
import copy

class TwoVehiclesNeighborhood(Neighborhood):
    """
    Move customer from one route to another one.
    """


    def get_neighbor(self,solution:Solution)->Solution:
        """
        Choose two routes randomly and move customer one customer from the first route to the second.
        """        
        num_vehicles=solution.vehicle_routes.shape[0]
        if num_vehicles<2:
            return solution

        #Get vehicles involved in the movement.
        vehicles_involved=self._get_vehicles_involved_in_the_movement(solution=solution) #self.get_different_instances(available_instances=num_vehicles,needed_instances=2)
        veh1=vehicles_involved[0]
        veh2=vehicles_involved[1]
     

        #Move nodes
        new_solution=copy.deepcopy(solution)        
        new_solution=self._operation_between_vehicle_routes(solution=new_solution, vehicle1=veh1, vehicle2=veh2)
        new_solution.vehicle_routes[veh1]=self._move_depot_to_the_end(route=new_solution.vehicle_routes[veh1])
        new_solution.vehicle_routes[veh2]=self._move_depot_to_the_end(route=new_solution.vehicle_routes[veh2])

        #Verify movements.
        valid=self._check_valid_modifications(new_solution=new_solution,vehicles_involved=vehicles_involved)
        if valid==False:
            new_solution.is_valid=False

        #Set new cost.
        new_solution.cost=self._update_solution_cost(old_solution=solution,new_solution=new_solution,vehicles_involved=vehicles_involved)

        return new_solution

    def _operation_between_vehicle_routes(self,solution:Solution, vehicle1:int, vehicle2:int)->np.ndarray:
        raise NotImplementedError


    def _get_vehicles_involved_in_the_movement(self,solution:Solution)->np.ndarray:
            """
            To avoid empty movements, we decide randomly whether to move from non-empty to non-empty routes (NE-NE) or
            to move between empty and non-empty routes.
            """
            #Vehicles with non-empty routes.
            non_empty_vehicle_routes=self.solution_restrictions_calculator.get_not_empty_vehicle_routes(solution=solution)        
            empty_routes=np.delete(np.array(range(0,solution.vehicle_routes.shape[0])),non_empty_vehicle_routes)

            choices=["NONEMPTY-NONEMPTY","NONEMPTY-EMPTY"]
            type_of_movement=np.random.choice(a=choices,size=1,replace=False)[0]

            if type_of_movement=="NONEMPTY-EMPTY" or len(non_empty_vehicle_routes)<2:
                veh1=np.random.choice(a=non_empty_vehicle_routes,size=1)[0]
                veh2=np.random.choice(a=empty_routes,size=1)[0]
                return np.array([veh1,veh2],dtype=int)

            return np.random.choice(a=non_empty_vehicle_routes,size=2,replace=False)



    def _get_node_index_from_route(self,route:np.ndarray)->int:
        """
        We prioritize customer nodes, but if no one is feasible, we return the depot.
        """
        index_customers_in_route=np.where(route>0)[0]
        num_customers=len(index_customers_in_route)

        #If the route has no customers, we return the 1st index (= depot)
        if num_customers<=0:
            return 0

        #available instances are=customer and depot. This allows to ingest customers from one route to another.
        node_index= self.get_different_instances(available_instances=num_customers+1,needed_instances=1)[0]
        
        return node_index