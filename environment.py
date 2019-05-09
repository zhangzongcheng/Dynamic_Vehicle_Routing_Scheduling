from method import *

class SimulationEnvironment:

    def __init__(self, sol, new_orders):

        self.solution = sol
        self.new_orders = new_orders

    def apply_continuous_insertion(self):

        for order in self.new_orders:

            algorithm = CIH(self.solution, order)
            algorithm.insert()

    def apply_periodic_insertion(self):

        algorithm = PIH(self.solution, self.new_orders)
        algorithm.insert()

    def apply_adaptive_large_neighborhood_search(self, d_min, d_max, max_iter, t_0, t_n):

        algorithm = ALNS(self.solution, self.new_orders, d_min, d_max, max_iter, t_0, t_n)

        return algorithm.run()