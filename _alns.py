from src._insertion import PIH
import random
import math
import copy


class ALNS:

    # This class performs Adaptive Large Neighborhood Search

    def __init__(self, init_solution, d_min, d_max, max_iter, t_0, t_n):

        """

        :param init_solution: Solution object
        :param d_min: int
        :param d_max: int
        :param max_iter: int
        :param t_0: float
        :param t_n: float
        """

        """
        Attributes
        ----------
        --> init_solution: Solution, initial solution to ALNS constructed by PIH
        --> d_min: int, minimum possible degree of destroy
        --> d_max: int, maximum possible degree of destroy
        --> max_iter: int, maximum number of iteration
        --> t_0: float, initial temperature
        --> t_n: float, final temperature
        """

        self.solution = init_solution
        self.d_min = d_min
        self.d_max = d_max
        self.max_iter = max_iter
        self.t_0 = t_0
        self.t_n = t_n

    def cooling(self, i, n):

        """Returns new temperature value by using cooling schedule

        :param i: int, current iteration
        :param n: int, maximum iteration
        :return: float, new temperature
        """

        return 0.5 * (self.t_0 - self.t_n) * (1 - math.tanh((10 * i) / n) - 5) + self.t_n

    @staticmethod
    def random_removal(sol, dod):

        """Removed dod number of orders randomly from the solution
        and then returns the list of the removed orders.

        :param sol: Solution, given solution
        :param dod: int, degree of destroy
        :return: list, list of removed orders
        """
        count = 0
        removed_orders = []
        while count < dod:

            which_crew = random.randint(0, len(sol.crews)-1)
            if len(sol.crews[which_crew].route) == 0:
                continue
            which_pose = random.randint(0, len(sol.crews[which_crew].route)-1)
            removed_or = sol.crews[which_crew].route[which_pose]
            sol.crews[which_crew].route.remove(removed_or)
            removed_orders.append(removed_or)
            count += 1
        sol.update()

        return removed_orders

    @staticmethod
    def worst_removal(sol, dod):

        """Removed worst dod number of orders from the solution
           and then returns the list of the removed orders.

            :param sol: Solution, given solution
            :param dod: int, degree of destroy
            :return: list, list of removed orders
        """

        count = 0
        removed_order = []
        while count < dod:

            which_crew, which_pose, tmp = -1, -1, math.inf
            for c in range(len(sol.crews)):
                for p in range(len(sol.crews[c].route)):
                    __sol__ = copy.deepcopy(sol)
                    __sol__.crews[c].route.remove(__sol__.crews[c].route[p])
                    if __sol__.objective_function_value() < tmp:
                        which_crew, which_pose, tmp = c, p, __sol__.objective_function_value()

            the_order = sol.crews[which_crew].route[which_pose]
            sol.crews[which_crew].route.remove(the_order)
            removed_order.append(the_order)
            count += 1
        sol.update()

        return removed_order

    @staticmethod
    def repair(sol, removed_order_):

        """This method performs repair operation by using
        periodic insertion heuristic for the removed orders

        :param sol:  Solution, given solution
        :param removed_order_:list, list of removed orders (now they will be added again)
        :return: %INPLACE%
        """

        inserter = PIH(sol, removed_order_)
        inserter.insert()

    def run(self):

        """This function runs the ALNS algorithm
        and updates the solution attribute of the
        class as an incumbent solution

        :return: %INPLACE%
        """
        current_sol, temperature, count = copy.deepcopy(self.solution), self.t_0, 0
        destroy_weights = [0.5, 0.5]  # w_1: random removal, w_2: worst_removal
        while count < self.max_iter:  # Stopping criteria --> reaching maximum number of iterations

            dod = random.randint(self.d_min, self.d_max)  # randomly selected degree of destroy
            candidate_sol = copy.deepcopy(current_sol)

            # select which destruction method will be employed
            if random.uniform(0, 1) < destroy_weights[0]:
                removed = ALNS.random_removal(candidate_sol, dod)
                which_destroy = 0
            else:
                removed = ALNS.worst_removal(candidate_sol, dod)
                which_destroy = 1

            # repair operation
            ALNS.repair(candidate_sol, removed)

            # acceptance criteria --> Simulated Annealing (SA) with the aim of further exploration
            if candidate_sol.objective_function_value() < current_sol.objective_function_value():
                current_sol = candidate_sol
                # weight updates
                destroy_weights[which_destroy] += 0.05
                if which_destroy == 0:
                    destroy_weights[1] -= 0.05
                else:
                    destroy_weights[0] -= 0.05
            else:
                diff = candidate_sol.objective_function_value() - current_sol.objective_function_value()
                if random.uniform(0, 1) < math.exp((-diff) / temperature):
                    current_sol = candidate_sol

            # incumbent solution update
            if candidate_sol.objective_function_value() < self.solution.objective_function_value():
                self.solution = candidate_sol

            # algorithm parameter update
            print(self.solution.objective_function_value())
            temperature = self.cooling(count, self.max_iter)
            count += 1
