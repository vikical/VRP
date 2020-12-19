from src.neighborhoods.neighborhood import Neighborhood
from src.neighborhoods.move_customer import MoveCustomer
from src.neighborhoods.reverse_order import ReverseOrder
from src.neighborhoods.swap_customers import SwapCustomers

from src.solution_management.solution_restrictions_calculator import SolutionRestrictionsCalculator

class NeighborhoodFactory(object):
    """
    Creates Neighborhood objects.
    """
    MOVE_CUSTOMER="move_customer"
    REVERSE_ORDER="reverse_order"
    SWAP_CUSTOMERS="swap_customers"

    @staticmethod
    def create_neighborhood(neighborhood_name:str, solution_restrictions_calculator:SolutionRestrictionsCalculator)->Neighborhood:
        if neighborhood_name==NeighborhoodFactory.MOVE_CUSTOMER:
            return MoveCustomer(solution_restrictions_calculator=solution_restrictions_calculator)
        if neighborhood_name==NeighborhoodFactory.REVERSE_ORDER:
            return ReverseOrder(solution_restrictions_calculator=solution_restrictions_calculator)
        if neighborhood_name==NeighborhoodFactory.SWAP_CUSTOMERS:
            return SwapCustomers(solution_restrictions_calculator=solution_restrictions_calculator)
        
        return None
