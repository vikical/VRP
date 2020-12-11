import numpy as np

from src.models.solution import Solution

class SolutionPrinter(object):
    """
    Manage different form to translate a Solution to string.
    """

    @staticmethod
    def to_string_as_route_matrixes(solution:Solution)->str:
        """
        Transforms matrix vehicle routes to string
        """
        string_solution=""
        for v_index in range(0,solution.vehicle_routes.shape[0]):
            string_solution=string_solution+"\n"+"VEHICLE:"+str(v_index)+"\n"
            string_solution=string_solution+np.array_str(a=solution.vehicle_routes[v_index])
        
        return string_solution

    @staticmethod
    def to_string_as_list_nodes(solution:Solution)->str:
        """
        Transform vehicles routes as matrix into vehicle list of nodes
        """
        string_solution=""
        for v_index in range(0,solution.vehicle_routes.shape[0]):
            string_solution=string_solution+"\n"+"VEHICLE:"+str(v_index)+"\n"
            route_as_1darray=SolutionPrinter.__get_route_as_1darray_of_nodes(route=solution.vehicle_routes[v_index])
            string_solution=string_solution+np.array_str(a=route_as_1darray)

        return string_solution
        
    @staticmethod
    def __get_route_as_1darray_of_nodes(route:np.ndarray)->np.ndarray:
        """
        Get a matrix route as a list of nodes.
        """
        route_1d=np.zeros(shape=route.shape[0])
        from_node=0
        for i in range(0,len(route_1d)):
            to_node=SolutionPrinter.__get_to_node(from_node=from_node,route=route)
            route_1d[i]=to_node
            if to_node==0:
                break
            from_node=to_node
        
        return route_1d

    @staticmethod
    def __get_to_node(from_node:int,route:np.ndarray)->int:
        from_node_row=route[from_node]

        likely_to_nodes=np.where(from_node_row==1)        
        if len(likely_to_nodes)<1:
            return 0

        return likely_to_nodes[0]
        