import copy, math, random

class CIH:

    def __init__(self, sol, order):

        self.solution = sol
        self.order = order

    def find_loc(self):

        n_crew = len(self.solution.crews)
        places = [len(crew.route) for crew in self.solution.crews]

        c, p, tmp = -1, -1, math.inf
        for i in range(n_crew):
            for j in range(places[i]):
                _sol_ = copy.deepcopy(self.solution)
                _sol_.crews[i].route.insert(j, self.order)
                _sol_.update()
                if _sol_.get_obj_val() < tmp and _sol_.is_feasible():
                    c, p, tmp = i, j, _sol_.get_obj_val()

        _sol_ = copy.deepcopy(self.solution)
        _sol_.outs.append(self.order)
        _sol_.update()
        if _sol_.get_obj_val() < tmp and _sol_.is_feasible():
            c = None

        return c, p  # which crew, which place

    def insert(self):

        which_crew, which_place = self.find_loc()
        if which_crew is None:
            self.solution.outs.append(self.order)
        else:
            self.solution.crews[which_crew].route.insert(which_place, self.order)
            self.order.is_outsource = None
        self.solution.update()

class PIH:

    def __init__(self, sol, orders):

        self.solution = sol
        self.new_orders = orders

    def insert(self):

        sorted_list = sorted(self.new_orders, key=lambda x: x.weight, reverse=True)
        for order in sorted_list:
            _ = CIH(self.solution, order)
            _.insert()


class ALNS:

    def __init__(self, sol, new_orders, d_min, d_max, max_iter, t_0, t_n):

        self.solution = sol
        self.new_orders = new_orders
        self.d_min = d_min
        self.d_max = d_max
        self.max_iter = max_iter
        self.t_0 = t_0
        self.t_n = t_n

        initializer = PIH(self.solution, self.new_orders)
        initializer.insert()

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

            if random.uniform(0,1) < 0.1:
                if len(sol.outs) > 0:
                    wh = random.randint(0, len(sol.outs)-1)
                    removed_or = sol.outs[wh]
                    sol.outs.remove(removed_or)
                    removed_orders.append(removed_or)
                    count += 1
            else:
                which_crew = random.randint(0, len(sol.crews) - 1)
                if len(sol.crews[which_crew].route) == 0:
                    continue
                which_pose = random.randint(0, len(sol.crews[which_crew].route) - 1)
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
                    if __sol__.get_obj_val() < tmp:
                        which_crew, which_pose, tmp = c, p, __sol__.get_obj_val()

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

        mod = PIH(sol, removed_order_)
        mod.insert()

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
            if candidate_sol.get_obj_val() < current_sol.get_obj_val():
                current_sol = candidate_sol
                # weight updates
                destroy_weights[which_destroy] += 0.05
                if which_destroy == 0:
                    destroy_weights[1] -= 0.05
                else:
                    destroy_weights[0] -= 0.05
            else:
                diff = candidate_sol.get_obj_val() - current_sol.get_obj_val()
                if random.uniform(0, 1) < math.exp((-diff) / temperature):
                    current_sol = candidate_sol

            # incumbent solution update
            if candidate_sol.get_obj_val() < self.solution.get_obj_val():
                self.solution = candidate_sol

            # algorithm parameter update
            print(self.solution.get_obj_val())
            temperature = self.cooling(count, self.max_iter)
            count += 1
        return self.solution