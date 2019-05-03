import datetime as dt
import src.utils_ as utils_


class Solution:

    """
    This class is for representing a solution as a whole

    Static Variables
    ----------------
    unit_lateness_cost : float : cost of one minute of lateness
    unit_overtime_cost : float : cost of one minute of overtime
    outsourcing_cost : float : cost of outsourcing a task
    budget: float : budget limit
    final_of_day  : datetime : the time after this any crew is allowed for working
    """

    unit_lateness_cost = 4
    unit_overtime_cost = 3
    outsourcing_cost = 100
    budget = 1000
    final_of_day = dt.datetime.strptime('18:35:00', '%H:%M:%S')

    def __init__(self, crews_, orders_):

        """Construction method

        :param crews_: list
        :param orders_: list
        """

        """
        Attributes
        ---------
        
        --> crews : list : list of crews
        --> orders: list : list of orders
        
        """

        self.crews = crews_
        self.orders = orders_
        self.update()

    def update(self):

        """Whenever a change occurs in one of the routes in the system,
        this method has to be called since it re-adjusts the relevant
        attributes of the orders and crews.

        :return: %INPLACE%
        """

        # Let's keep the crews completed by our crews in a list

        orders_in = []
        for crew in self.crews:
            for order in crew.route:
                orders_in.append(order)

        # Now we can label other orders as an outsourced orders

        for order in self.orders:
            if order in orders_in:
                order.is_outsource = False
            else:
                order.is_outsource = True

        # Now let's compute the relevant times appropriately

        for crew in self.crews:
            tmp = crew.starting_time
            for i, order in enumerate(crew.route):
                order_loc = (order.x_coor, order.y_coor)
                if i == 0:  # then goes to the first route from the first available location
                    tmp = tmp + dt.timedelta(minutes=utils_.get_time(crew.starting_loc, order_loc))
                else:  # then goes to the next order from the previous one
                    previous_order = crew.route[i-1]
                    previous_loc = (previous_order.x_coor, previous_order.y_coor)
                    tmp = tmp + dt.timedelta(minutes=utils_.get_time(previous_loc, order_loc))

                # Now we are starting to the corresponding order.
                order.which_crew = crew.id_
                order.starting_time = tmp
                tmp = tmp + dt.timedelta(minutes=order.process_time)
                # Now we are completing the corresponding order.
                order.completion_time = tmp
                order.waiting_time = (order.completion_time - order.arrival_time).seconds / 60.0
                if order.completion_time <= order.deadline:
                    order.lateness = 0
                else:
                    order.lateness = (order.completion_time - order.deadline).seconds / 60.0
            # crew information update
            if len(crew.route) > 0:
                crew.drop_time = crew.route[-1].completion_time
                if crew.drop_time <= crew.last_time:
                    crew.overtime = 0
                else:
                    crew.overtime = (crew.drop_time - crew.last_time).seconds / 60.0

    def objective_function_value(self):

        """Returns total objective function value
        :return: float
        """

        obj_value = 0
        for crew in self.crews:
            obj_value += sum([order.waiting_time * order.weight for order in crew.route])
        return obj_value

    def total_cost(self):

        """Return total cost
        :return: float
        """
        cost = 0

        # Outsource cost - Lateness cost

        for order in self.orders:
            if order.is_outsource:
                cost += Solution.outsourcing_cost
            else:
                cost += order.lateness * Solution.unit_lateness_cost

        # Overtime cost

        for crew in self.crews:
            cost += crew.overtime * Solution.unit_overtime_cost

        # Travelling cost

        for crew in self.crews:
            for index, order in enumerate(crew.route):
                if index < len(crew.route) - 1:
                    order_ = crew.route[index+1]
                    cost += utils_.get_travel_cost((order.x_coor, order.y_coor), (order_.x_coor, order_.y_coor))

        return cost

    def is_feasible(self):

        """Returns whether the solution is feasible or not

        :return: boolean
        """

        flag = True

        # Budget Limit

        if self.total_cost() > Solution.budget:
            flag = False

        # Crews cannot work after the end of the day

        if flag:
            for crew in self.crews:
                if crew.drop_time > Solution.final_of_day:
                    flag = False
                    break

        # A crew must be capable of achieving the orders assigned to it

        if flag:
            for order in self.orders:
                if not order.is_outsource:
                    its_crew = None
                    for crew in self.crews:
                        if crew.id_ == order.which_crew:
                            its_crew = crew
                            break
                    for skill in order.req_skill:
                        if skill not in its_crew.skills:
                            flag = False
                            break

        # Every order must be completed either by outsourcing or a crew

        if flag:
            count = 0
            for order in self.orders:
                if order.is_outsource or order.which_crew is not None:
                    count += 1
            if count < len(self.orders):
                flag = False

        # Orders assigned to a crew must be completed before its deadline

        if flag:
            for order in self.orders:
                if not order.is_outsource:
                    if order.completion_time > order.deadline:
                        flag = False
                        break

        return flag
