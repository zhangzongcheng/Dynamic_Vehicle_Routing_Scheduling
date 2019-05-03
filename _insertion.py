import copy
import math


class CIH:

    # This class performs continuous re-optimization heuristics
    def __init__(self, sol_, order_):

        """Construction method

        :param sol_: list
        :param order_: Order object
        """

        """
        Attributes
        ----------
        --> solution : Solution, a solution to the problem
        --> order: Order, the order that will be inserted
        """

        self.solution = sol_
        self.order = order_

    def find_best_place(self):

        """This method finds the best crew and its best position
        to insert the order and returns these two in a tuple

        :return: tuple
        """

        n_crew = len(self.solution.crews)
        places = [len(crew.route) for crew in self.solution.crews]

        c, p, tmp = -1, -1, math.inf
        for i in range(n_crew):
            for j in range(places[i]):
                __sol__ = copy.deepcopy(self.solution)  # deep copy of the solution
                __sol__.crews[i].route.insert(j, self.order)  # scenario of insertion
                __sol__.update()  # imaginary update of the parameters
                if __sol__.objective_function_value() < tmp and __sol__.is_feasible():
                    c, p, tmp = i, j, __sol__.objective_function_value()
        return c, p  # which crew, which place

    def insert(self):

        """This function inserts the order to the best place

        :return: %INPLACE%
        """

        which_crew, which_place = self.find_best_place()
        self.solution.crews[which_crew].route.insert(which_place, self.order)
        self.solution.update()


class PIH:

    # This class performs periodic re-optimization heuristics

    def __init__(self, sol_, orders_):

        """Construction method

        :param sol_: Solution, a solution
        :param orders_: list, list of orders that will be inserted
        """

        self.solution = sol_
        self.new_orders = orders_

    def insert(self):

        """ This method inserts the orders to the solution
        :return: %INPLACE%
        """
        
        sorted_list = sorted(self.new_orders, key=lambda x: x.weight, reverse=True)
        for order in sorted_list:
            _ = CIH(self.solution, order)
            _.insert()
